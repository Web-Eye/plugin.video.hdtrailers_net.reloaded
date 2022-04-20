# -*- coding: utf-8 -*-
# Copyright 2021 WebEye
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#

import json
import logging
import sys
import urllib
import urllib.parse

from libs.database.database_api import DBAPI

import xbmc
import xbmcplugin
import xbmcgui
import xbmcaddon
import xbmcvfs


from libs.hdtrailers_api import HDTrailerAPI

# -- Constants ----------------------------------------------
ADDON_ID = 'plugin.video.hdtrailers_net.reloaded'
BASE_URL = 'http://www.hd-trailers.net/'

ADDONTHUMB = xbmcvfs.translatePath('special://home/addons/' + ADDON_ID + '/resources/assets/icon.png')
FANART = xbmcvfs.translatePath('special://home/addons/' + ADDON_ID + '/resources/assets/fanart.png')
NAVART = xbmcvfs.translatePath('special://home/addons/' + ADDON_ID + '/resources/assets/menu.png')
DEFAULT_IMAGE_URL = ''

HOME = 'home'
LATEST = 'latest'
LIBRARY = 'library'
MOST_WATCHED_WEEK = 'most_watched_week'
MOST_WATCHED_TODAY = 'most_watched_today'
TOP_MOVIES = 'top_movies'
OPENING_THIS_WEEK = 'opening_this_week'
COMING_SOON = 'coming_soon'
NAVIGATIONS = 'navigations'

# -- logger -----------------------------------------------
logger = logging.getLogger("plugin.video.hdtrailers.reloaded.api")

# -- Settings -----------------------------------------------
addon = xbmcaddon.Addon(id=ADDON_ID)
xbmcplugin.setContent(int(sys.argv[1]), 'movies')

quality_id = int(addon.getSetting('quality'))
extract_plot = (addon.getSetting('extract_plot') == 'true')
page_itemCount = int(addon.getSetting('page_itemCount'))

db_enabled = (addon.getSetting('database_enabled') == 'true')
db_config = None
if db_enabled:
    db_config = {
        'host': addon.getSetting('db_host'),
        'port': int(addon.getSetting('db_port')),
        'user': addon.getSetting('db_username'),
        'password': addon.getSetting('db_password'),
        'database': 'KodiWebGrabber'
    }
    extract_plot = False

language = addon.getLocalizedString

translations = {
    HOME:               language(30100),
    LATEST:             language(30101),
    LIBRARY:            language(30102),
    MOST_WATCHED_WEEK:  language(30103),
    MOST_WATCHED_TODAY: language(30104),
    TOP_MOVIES:         language(30105),
    OPENING_THIS_WEEK:  language(30106),
    COMING_SOON:        language(30107),
    NAVIGATIONS:        language(30108)
}

class HDTrailers:

    def __init__(self):
        pass

    def addItem(self, title, plot, poster, trailer):

        if trailer is not None:
            link = trailer.get('link')
            if link is not None:

                title = str(trailer.get('name'))
                date = trailer.get('date')
                url = link.get('url')
                size = link.get('size')

                li = xbmcgui.ListItem(title)
                if poster is not None:
                    li.setArt({'thumb': poster})
                else:
                    li.setArt({'thumb': DEFAULT_IMAGE_URL})
                li.setProperty('Fanart_Image', FANART)
                li.setProperty('IsPlayable', 'true')

                li.setInfo(type="Video", infoLabels={"Title": title,
                                                     "Plot": str(plot),
                                                     "Size": size,
                                                     "Date": date,
                                                     "Aired": date})

                xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]), url=url, listitem=li, isFolder=False)

    def addDirectory(self, title, args, poster=None, plot=None):
        url = 'plugin://' + ADDON_ID + '/?' + urllib.parse.urlencode(args)
        try:
            li = xbmcgui.ListItem(str(title))
            if poster is not None:
                li.setArt({'thumb': poster})
            else:
                li.setArt({'thumb': DEFAULT_IMAGE_URL})
            li.setProperty('Fanart_Image', FANART)

            if plot is not None:
                li.setInfo(type="Video", infoLabels={"Plot": str(plot)})

            xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]), url=url, listitem=li, isFolder=True)

        except NameError:
            pass

    def setItemView(self, url, tag=None):
        url = urllib.parse.urljoin(BASE_URL, url)
        API = HDTrailerAPI(url, quality_id)
        item = API.getItem()

        trailers = item.get('trailers')

        if trailers is not None:
            title = item.get('title')
            plot = item.get('plot')
            poster = item.get('poster')

            for trailer in trailers:
                addItem(title, plot, poster, trailer)

    def setListMostWatchedView(self, url, tag=None):
        url = urllib.parse.urljoin(BASE_URL, url)
        API = HDTrailerAPI(url)
        items = API.getMostWatched(tag)
        if items is not None:
            for item in items:
                plot = None
                if extract_plot == 'true' and tag != 'lbrary':
                    url = urllib.parse.urljoin(BASE_URL, item.get('url'))
                    API = HDTrailerAPI(url)
                    plot = API.getPlot()

                addDirectory(title=item.get('title'), poster=item.get('poster'), plot=plot, args=buildArgs('item', item.get('url')))

    def setListLibraryView(self, url, tag=None):
        if not db_enabled:
            url = urllib.parse.urljoin(BASE_URL, url)
            API = HDTrailerAPI(url)
            items = API.getLibraryLinks()
            if items is not None:
                for item in items:
                    addDirectory(title=item.get('title'), args=buildArgs('list', item.get('url'), 'library'))

    def setNavView(self, url=None, tag=None):
        if tag is not None:
            items = json.loads(tag)
            for item in items:
                addDirectory(title=item.get('title'), args=buildArgs('list', item.get('url')))

    def setListView(self, url, tag=None):
        if not db_enabled:
            url = urllib.parse.urljoin(BASE_URL, url)
            API = HDTrailerAPI(url)
        else:
            API = DBAPI(db_config, tag)

        items = API.getItems()

        if items is not None:
            for item in items:
                plot = None
                if extract_plot == 'true' and tag != 'library':
                    _url = urllib.parse.urljoin(BASE_URL, item.get('url'))
                    _API = HDTrailerAPI(_url)
                    plot = _API.getPlot()

                addDirectory(title=item.get('title'), poster=item.get('poster'), plot=plot, args=buildArgs('item', item.get('url')))

        navigation = API.getNavigation()
        if navigation is not None:
            addDirectory(title=translations[NAVIGATIONS], poster=NAVART, args=buildArgs('nav', tag=navigation))

    def buildArgs(self, method, url=None, tag=None):
        return {
            'method': method,
            'url': url,
            'tag': tag
        }

    def setHomeView(self, url, tag=None):
        if not db_enabled:
            addDirectory(title=translations[LATEST], poster=ADDONTHUMB, args=buildArgs('list', '/page/1/'))
            addDirectory(title=translations[LIBRARY], poster=ADDONTHUMB, args=buildArgs('list_library', '/poster-library/0/'))
            addDirectory(title=translations[MOST_WATCHED_WEEK], poster=ADDONTHUMB,
                         args=buildArgs('list_most_watched', '/most-watched/', 'Week'))
            addDirectory(title=translations[MOST_WATCHED_TODAY], poster=ADDONTHUMB,
                         args=buildArgs('list_most_watched', '/most-watched/', 'Today'))
            addDirectory(title=translations[TOP_MOVIES], poster=ADDONTHUMB, args=buildArgs('list', '/top-movies/'))
            addDirectory(title=translations[OPENING_THIS_WEEK], poster=ADDONTHUMB, args=buildArgs('list', '/opening-this-week/'))
            addDirectory(title=translations[COMING_SOON], poster=ADDONTHUMB, args=buildArgs('list', '/coming-soon/'))

        else:
            addDirectory(title=translations[LATEST], poster=ADDONTHUMB, args=buildArgs('list', 'LATEST', 1))
            addDirectory(title=translations[LIBRARY], poster=ADDONTHUMB,
                         args=buildArgs('list_library'))
            addDirectory(title=translations[MOST_WATCHED_WEEK], poster=ADDONTHUMB,
                         args=buildArgs('list', 'MOSTWATCHEDWEEK'))
            addDirectory(title=translations[MOST_WATCHED_TODAY], poster=ADDONTHUMB,
                         args=buildArgs('list', 'MOSTWATCHEDTODAY'))
            addDirectory(title=translations[TOP_MOVIES], poster=ADDONTHUMB, args=buildArgs('list', 'TOPTEN'))
            addDirectory(title=translations[OPENING_THIS_WEEK], poster=ADDONTHUMB,
                         args=buildArgs('list', 'OPENING'))
            addDirectory(title=translations[COMING_SOON], poster=ADDONTHUMB, args=buildArgs('list', 'COMINGSOON'))

    def get_query_args(self, s_args):
        args = urllib.parse.parse_qs(urllib.parse.urlparse(s_args).query)

        for key in args:
            args[key] = args[key][0]
        return args

    def hd_trailers(self):

        xbmcplugin.setPluginFanart(int(sys.argv[1]), FANART)

        args = self.get_query_args(sys.argv[2])

        if args is None or args.__len__() == 0:
            args = self.buildArgs('home')

        method = args.get('method')
        url = args.get('url')
        tag = args.get('tag')

        {
            'home': self.setHomeView,
            'list': self.setListView,
            'nav': self.setNavView,
            'list_library': self.setListLibraryView,
            'list_most_watched': self.setListMostWatchedView,
            'item': self.setItemView
        }[method](url, tag)

        xbmcplugin.endOfDirectory(int(sys.argv[1]))
