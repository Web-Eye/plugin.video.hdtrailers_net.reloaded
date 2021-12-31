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

try:
    import xbmc
    import xbmcplugin
    import xbmcgui
    import xbmcaddon
    import xbmcvfs
except ImportError:
    import libs.emu.xbmc as xbmc
    import libs.emu.xbmcplugin as xbmcplugin
    import libs.emu.xbmcgui as xbmcgui
    import libs.emu.xbmcaddon as xbmcaddon
    import libs.emu.xbmcvfs as xbmcvfs

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
MOST_WATCHED = 'most_watched'
TOP_MOVIES = 'top_movies'
OPENING_THIS_WEEK = 'opening_this_week'
COMING_SOON = 'coming_soon'
NAVIGATIONS = 'navigations'

# -- logger -----------------------------------------------
logger = logging.getLogger("plugin.video.hdtrailers.reloaded.api")

# -- Settings -----------------------------------------------
addon = xbmcaddon.Addon(id=ADDON_ID)
quality_id = addon.getSetting('quality')
start_page_id = addon.getSetting('start_page')

xbmcplugin.setContent(int(sys.argv[1]), 'movies')

quality = ['480p', '720p', '1080p', 'Best'][int(quality_id)]
start_page = [HOME, LATEST, LIBRARY, MOST_WATCHED, TOP_MOVIES, OPENING_THIS_WEEK, COMING_SOON][int(start_page_id)]


language = addon.getLocalizedString

translations = {
    HOME:               language(30100),
    LATEST:             language(30101),
    LIBRARY:            language(30102),
    MOST_WATCHED:       language(30103),
    TOP_MOVIES:         language(30104),
    OPENING_THIS_WEEK:  language(30105),
    COMING_SOON:        language(30106),
    NAVIGATIONS:        language(30107)
}


def addItem(title, plot, poster, trailer):

    if trailer is not None:
        link = trailer.get('link')
        if link is not None:

            tTitle = str(trailer.get('name'))
            date = trailer.get('date')
            url = link.get('url')
            size = link.get('size')

            li = xbmcgui.ListItem(tTitle)
            if poster is not None:
                li.setArt({'thumb': poster})
            else:
                li.setArt({'thumb': DEFAULT_IMAGE_URL})
            li.setProperty('Fanart_Image', FANART)
            li.setProperty('IsPlayable', 'true')

            li.setInfo(type="Video", infoLabels={"Title": tTitle,
                                                 "Plot": str(plot),
                                                 "Size": size,
                                                 "Date": date,
                                                 "Aired": date})

            xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]), url=url, listitem=li, isFolder=False)


def addDirectory(title, args, poster=None):
    url = 'plugin://' + ADDON_ID + '/?' + urllib.parse.urlencode(args)
    try:
        li = xbmcgui.ListItem(str(title))
        if poster is not None:
            li.setArt({'thumb': poster})
        else:
            li.setArt({'thumb': DEFAULT_IMAGE_URL})
        li.setProperty('Fanart_Image', FANART)
        xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]), url=url, listitem=li, isFolder=True)
    except NameError:
        pass


def setItemView(url, tag=None):
    url = urllib.parse.urljoin(BASE_URL, url)
    API = HDTrailerAPI(url, quality)
    item = API.getItem()

    trailers = item.get('trailers')

    if trailers is not None:
        title = item.get('title')
        plot = item.get('plot')
        poster = item.get('poster')

        for trailer in trailers:
            addItem(title, plot, poster, trailer)


def setListMostWatchedView(url, tag=None):
    pass
    # TODO setItemView
    # items = parsemostwatched(url)
    # for item in items:
    #     AddDirectory(item.title, {method: 'list', url: item.url})


def setListLibraryView(url, tag=None):
    pass
    # TODO SetListLibraryView
    # items = parselibrary(url)
    # for item in items:
    #     AddDirectory(item.title, {method: 'list', url: item.url})


def setNavView(url=None, tag=None):
    if tag is not None:
        items = json.loads(tag)
        for item in items:
            addDirectory(title=item.get('title'), args=buildArgs('list', item.get('url')))


def setListView(url, tag=None):
    url = urllib.parse.urljoin(BASE_URL, url)
    API = HDTrailerAPI(url, quality)
    items = API.getItems()

    if items is not None:
        for item in items:
            addDirectory(title=item.get('title'), poster=item.get('poster'), args=buildArgs('item', item.get('url')))

    navigation = API.getNavigation()
    if navigation is not None:
        addDirectory(title=translations[NAVIGATIONS], poster=NAVART, args=buildArgs('nav', tag=navigation))


def buildArgs(method, url=None, tag=None):
    return {
        'method': method,
        'url': url,
        'tag': tag
    }


def setHomeView(url, tag=None):
    addDirectory(title=translations[LATEST], poster=ADDONTHUMB, args=buildArgs('list', '/page/1/'))
    addDirectory(title=translations[LIBRARY], poster=ADDONTHUMB, args=buildArgs('list_library', '/library/0/'))
    addDirectory(title=translations[MOST_WATCHED], poster=ADDONTHUMB, args=buildArgs('list_most_watched', '/most-watched/'))
    addDirectory(title=translations[TOP_MOVIES], poster=ADDONTHUMB, args=buildArgs('list', '/top-movies/'))
    addDirectory(title=translations[OPENING_THIS_WEEK], poster=ADDONTHUMB, args=buildArgs('list', '/opening-this-week/'))
    addDirectory(title=translations[COMING_SOON], poster=ADDONTHUMB, args=buildArgs('list', '/coming-soon/'))


def get_query_args(s_args):
    args = urllib.parse.parse_qs(urllib.parse.urlparse(s_args).query)

    for key in args:
        args[key] = args[key][0]
    return args


def hd_trailers():

    xbmcplugin.setPluginFanart(int(sys.argv[1]), FANART)

    args = get_query_args(sys.argv[2])

    if args is None or args.__len__() == 0:
        args = buildArgs('home')
        # args = {
        #     HOME:
        #         lambda: buildArgs('home', ''),
        #     LATEST:
        #         lambda: buildArgs('list', '/page/1/'),
        #     LIBRARY:
        #         lambda: buildArgs('list_library', '/library/0/'),
        #     MOST_WATCHED:
        #         lambda: buildArgs('list_most_watched', '/most-watched/'),
        #     TOP_MOVIES:
        #         lambda: buildArgs('list', '/top-movies/'),
        #     OPENING_THIS_WEEK:
        #         lambda: buildArgs('list', '/opening-this-week/'),
        #     COMING_SOON:
        #         lambda: buildArgs('list', '/coming-soon/')
        # }[start_page]()

    method = args.get('method')
    url = args.get('url')
    tag = args.get('tag')

    {
        'home': setHomeView,
        'list': setListView,
        'nav': setNavView,
        'list_library': setListLibraryView,
        'list_most_watched': setListMostWatchedView,
        'item': setItemView
    }[method](url, tag)

    xbmcplugin.endOfDirectory(int(sys.argv[1]))
