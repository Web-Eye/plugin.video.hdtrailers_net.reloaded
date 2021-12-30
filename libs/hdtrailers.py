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
except ImportError:
    import libs.emu.xbmc as xbmc

try:
    import xbmcplugin
except ImportError:
    import libs.emu.xbmcplugin as xbmcplugin

try:
    import xbmcgui
except ImportError:
    import libs.emu.xbmcgui as xbmcgui

try:
    import xbmcaddon
except ImportError:
    import libs.emu.xbmcaddon as xbmcaddon

try:
    import xbmcvfs
except ImportError:
    import libs.emu.xbmcvfs as xbmcvfs

from libs.hdtrailers_api import HDTrailerAPI

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
NAVIGATIONS = 'navigations'

# -- logger -----------------------------------------------
logger = logging.getLogger("plugin.video.hdtrailers.reloaded.api")

# -- Settings -----------------------------------------------
addon = xbmcaddon.Addon(id=ADDON_ID)
quality_id = addon.getSetting('quality')
start_page_id = addon.getSetting('start_page')


quality = ['480p', '720p', '1080p', 'Best'][int(quality_id)]
start_page = [HOME, LATEST, LIBRARY, MOST_WATCHED, TOP_MOVIES, OPENING_THIS_WEEK, COMING_SOON][int(start_page_id)]

# try:
language = addon.getLocalizedString
# except NameError:
#     def language(id):
#         return {
#             30100: 'Home',
#             30101: 'Latest',
#             30102: 'Library',
#             30103: 'Most Watched',
#             30104: 'Top Movies',
#             30105: 'Opening This Week',
#             30106: 'Coming Soon',
#             30107: 'Navigations'
#         }[id]

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


def add_item(title, args):
    pass
    # TODO AddItem


def add_directory(title, args, poster=None):
    url = 'plugin://' + ADDON_ID + '/?' + urllib.parse.urlencode(args)
    print(url)
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


def play_item(url):
    pass
    # TODO PlayItem


def set_item_view(url):
    url = urllib.parse.urljoin(BASE_URL, url)
    api = HDTrailerAPI(url, quality)
    item = api.parse_item_page()
    # TODO SetItemView
    # for item in items:
    #     AddItem(item.title, {poster: item.poster, plot: item.plot, method: 'play', url: item.url})


def set_list_most_watched_view(url):
    pass
    # TODO SetListMostWatchedView
    # items = parsemostwatched(url)
    # for item in items:
    #     AddDirectory(item.title, {method: 'list', url: item.url})


def set_list_library_view(url):
    pass
    # TODO SetListLibraryView
    # items = parselibrary(url)
    # for item in items:
    #     AddDirectory(item.title, {method: 'list', url: item.url})


def set_nav_view(url):
    if url is not None:
        items = json.loads(url)
        for item in items:
            add_directory(title=item.get('title'), args=build_args('list', item.get('url')))


def set_list_view(url):
    url = urllib.parse.urljoin(BASE_URL, url)
    api = HDTrailerAPI(url, quality)
    items, navigation = api.parse_items_page()

    if items is not None:
        for item in items:
            add_directory(title=item.get('title'), poster=item.get('poster'), args=build_args('item', item.get('url')))
    if navigation is not None:
        add_directory(title=translations[NAVIGATIONS], args=build_args('nav', navigation))


def build_args(method, url):
    return {
        'method': method,
        'url': url
    }


def set_home_view(url):
    add_directory(title=translations[LATEST], args=build_args('list', '/page/1/'))
    add_directory(title=translations[LIBRARY], args=build_args('list_library', '/library/0/'))
    add_directory(title=translations[MOST_WATCHED], args=build_args('list_most_watched', '/most-watched/'))
    add_directory(title=translations[TOP_MOVIES], args=build_args('list', '/top-movies/'))
    add_directory(title=translations[OPENING_THIS_WEEK], args=build_args('list', '/opening-this-week/'))
    add_directory(title=translations[COMING_SOON], args=build_args('list', '/coming-soon/'))


def get_query_args(s_args):
    args = urllib.parse.parse_qs(urllib.parse.urlparse(s_args).query)

    for key in args:
        args[key] = args[key][0]
    return args


def hd_trailers():

    args = get_query_args(sys.argv[2])
    if args is None or args.__len__() == 0:
        args = {
            HOME:
                lambda: build_args('home', ''),
            LATEST:
                lambda: build_args('list', '/page/1/'),
            LIBRARY:
                lambda: build_args('list_library', '/library/0/'),
            MOST_WATCHED:
                lambda: build_args('list_most_watched', '/most-watched/'),
            TOP_MOVIES:
                lambda: build_args('list', '/top-movies/'),
            OPENING_THIS_WEEK:
                lambda: build_args('list', '/opening-this-week/'),
            COMING_SOON:
                lambda: build_args('list', '/coming-soon/')
        }[start_page]()

    {
        'home': set_home_view,
        'list': set_list_view,
        'nav': set_nav_view,
        'list_library': set_list_library_view,
        'list_most_watched': set_list_most_watched_view,
        'item': set_item_view,
        'play': play_item
    }[args.get('method')](args.get('url'))

    xbmcplugin.endOfDirectory(int(sys.argv[1]))
