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

import sys, urllib, urllib.parse, logging
import xbmc, xbmcplugin, xbmcgui, xbmcaddon, xbmcvfs

from libs.hdtrailers_api import parseItemPage

# -- Constants ----------------------------------------------
ADDON_ID = 'plugin.video.hdtrailers_net.reloaded'
BASE_URL = 'http://www.hd-trailers.net/'

FANART = ''  # xbmcvfs.translatePath('special://home/addons/' + ADDON_ID + '/resources/assets/fanart.jpg')
DEFAULT_IMAGE_URL = ''

HOME = 'home'
LATEST = 'latest'
LIBRARY = 'library'
MOST_WATCHED = 'most_watched'
TOP_MOVIES = 'top_movies'
OPENING_THIS_WEEK = 'opening_this_week'
COMING_SOON = 'coming_soon'

# -- logger -----------------------------------------------
logger = logging.getLogger("plugin.video.hdtrailers.reloaded.api")

# -- Settings -----------------------------------------------
addon = xbmcaddon.Addon(id=ADDON_ID)
quality_id = addon.getSetting('quality')
quality = ['480p', '720p', '1080p'][int(quality_id)]
start_page_id = addon.getSetting('start_page')

language = addon.getLocalizedString
translations = {
    HOME:               language(30100),
    LATEST:             language(30101),
    LIBRARY:            language(30102),
    MOST_WATCHED:       language(30103),
    TOP_MOVIES:         language(30104),
    OPENING_THIS_WEEK:  language(30105),
    COMING_SOON:        language(30106),
}

def AddItem(title, args):
    print("AddItem")


def AddDirectory(title, args, poster=None):
    url = 'plugin://' + ADDON_ID + '/?' + urllib.parse.urlencode(args)
    print(url)
    li = xbmcgui.ListItem(str(title))
    if poster is not None:
        li.setArt({'thumb': poster})
    else:
        li.setArt({'thumb': DEFAULT_IMAGE_URL})
    li.setProperty('Fanart_Image', FANART)
    xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]), url=url, listitem=li, isFolder=True)


def PlayItem(url):
    print("PlayItem")


def SetItemView(url):
    print("SetItemView")
    # items = parseitems(url)
    # for item in items:
    #     AddItem(item.title, {poster: item.poster, plot: item.plot, method: 'play', url: item.url})


def SetListMostWatchedView(url):
    print("SetListMostWatchedView")
    # items = parsemostwatched(url)
    # for item in items:
    #     AddDirectory(item.title, {method: 'list', url: item.url})


def SetListLibraryView(url):
    print("SetListLibraryView")
    # items = parselibrary(url)
    # for item in items:
    #     AddDirectory(item.title, {method: 'list', url: item.url})


def SetListView(url):
    url = urllib.parse.urljoin(BASE_URL, url)
    items, navigation = parseItemPage(url)
    # for item in items:
    #     AddDirectory(title=item.title, poster=item.poster, args=BuildArgs('item', item.url))
    # if navigation is not None:
    #     pass


def BuildArgs(method, url):
    return {
        'method': method,
        'url': url
    }


def SetHomeView(url):
    AddDirectory(title=translations[LATEST], args=BuildArgs('list', '/page/1/'))
    AddDirectory(title=translations[LIBRARY], args=BuildArgs('list_library', '/library/0/'))
    AddDirectory(title=translations[MOST_WATCHED], args=BuildArgs('list_most_watched', '/most-watched/'))
    AddDirectory(title=translations[TOP_MOVIES], args=BuildArgs('list', '/top-movies/'))
    AddDirectory(title=translations[OPENING_THIS_WEEK], args=BuildArgs('list', '/opening-this-week/'))
    AddDirectory(title=translations[COMING_SOON], args=BuildArgs('list', '/coming-soon/'))


def get_query_args(sargs):
    args = urllib.parse.parse_qs(urllib.parse.urlparse(sargs).query)

    for key in args:
        args[key] = args[key][0]
    return args


def hdtrailers():
    start_page = HOME

    args = get_query_args(sys.argv[2])
    if args is None or args.__len__() == 0:
        args = {
            HOME:
                lambda: BuildArgs('home', ''),
            LATEST:
                lambda: BuildArgs('list', '/page/1/'),
            LIBRARY:
                lambda: BuildArgs('list_library', '/library/0/'),
            MOST_WATCHED:
                lambda: BuildArgs('list_most_watched', '/most-watched/'),
            TOP_MOVIES:
                lambda: BuildArgs('list', '/top-movies/'),
            OPENING_THIS_WEEK:
                lambda: BuildArgs('list', '/opening-this-week/'),
            COMING_SOON:
                lambda: BuildArgs('list', '/coming-soon/')
        }[start_page]()

    {
        'home': SetHomeView,
        'list': SetListView,
        'list_library': SetListLibraryView,
        'list_most_watched': SetListMostWatchedView,
        'item': SetItemView,
        'play': PlayItem
    }[args.get('method')](args.get('url'))

    xbmcplugin.endOfDirectory(int(sys.argv[1]))
