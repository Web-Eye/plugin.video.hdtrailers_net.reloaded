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
import sys
import urllib
import urllib.parse
import mysql.connector

from urllib.parse import urljoin

from libs.kodion.addon import Addon
from libs.database.database_api import DBAPI
from libs.kodion.gui_manager import *
from libs.tools import tools
from libs.translations import *
from libs.hdtrailers_api import HDTrailerAPI


class HDTrailers:

    def __init__(self):

        # -- Constants ----------------------------------------------
        self._ADDON_ID = 'plugin.video.hdtrailers_net.reloaded'

        width = getScreenWidth()
        addon = Addon(self._ADDON_ID)

        self._NAME = addon.getAddonInfo('name')
        self._FANART = addon.getAddonInfo('fanart')
        self._ICON = addon.getAddonInfo('icon')
        self._NAVART = addon.getAddonInfo('navart')
        self._BASE_URL = 'http://www.hd-trailers.net/'
        self._POSTERWIDTH = int(width / 3)
        self._DEFAULT_IMAGE_URL = ''
        self._t = Translations(addon)

        # -- settings ----------------------------------------------
        self._quality_id = int(addon.getSetting('quality'))
        self._extract_plot = (addon.getSetting('extract_plot') == 'true')
        self._page_itemCount = int(addon.getSetting('page_itemCount'))

        self._db_enabled = (addon.getSetting('database_enabled') == 'true')
        self._db_config = None
        if self._db_enabled:
            self._db_config = {
                'host': addon.getSetting('db_host'),
                'port': int(addon.getSetting('db_port')),
                'user': addon.getSetting('db_username'),
                'password': addon.getSetting('db_password'),
                'database': 'KodiWebGrabber'
            }
            self._extract_plot = False

        self._guiManager = GuiManager(sys.argv[1], self._ADDON_ID, self._DEFAULT_IMAGE_URL, self._FANART)
        self._guiManager.setContent('movies')

    def addItem(self, plot, poster, trailer):

        if trailer is not None:
            link = trailer.get('link')
            if link is not None:

                title = str(trailer.get('name'))
                date = tools.convertDateTime(trailer.get('date'), '%Y-%m-%d %H:%M:%S', '%Y-%m-%d')

                infoLabels = {
                    'Title': title,
                    'Plot': str(plot),
                    'Size': link.get('size'),
                    'Date': date,
                    'Aired': date
                }

                self._guiManager.addItem(title=title, url=link.get('url'), poster=poster, _type='video',
                                         infoLabels=infoLabels)

    def addDirectory(self, title, args, poster=None, plot=None):
        try:
            if poster is None:
                poster = self._DEFAULT_IMAGE_URL

            infoLabels = {
                'Title': title
            }

            if plot is not None:
                infoLabels['Plot'] = str(plot)

            self._guiManager.addDirectory(title=title, poster=poster, fanArt=self._FANART, _type='Video',
                                          infoLabels=infoLabels, args=args)

        except NameError:
            pass

    def setItemView(self, **kwargs):
        param = kwargs.get('param')
        tag = kwargs.get('tag')

        if not self._db_enabled and param == 'URL':
            url = self._getUrl(tag)
            API = HDTrailerAPI(url, self._quality_id)

        elif self._db_enabled and param == 'DB':
            _tag = {
                'item_id': tag,
                'quality_id': self._quality_id
            }
            try:
                API = DBAPI(self._db_config, _tag)
            except mysql.connector.Error as e:
                self._guiManager.setToastNotification(self._NAME, e.msg, image=self._ICON)
                return
        else:
            return

        item = API.getItem()

        trailers = item.get('trailers')
        plot = item.get('plot')
        poster = item.get('poster')

        if trailers is not None:
            for trailer in trailers:
                self.addItem(plot, poster, trailer)

    def setListMostWatchedView(self, **kwargs):
        param = kwargs.get('param')

        if not self._db_enabled:
            _param = {
                'MOSTWATCHEDWEEK': 'WEEK',
                'MOSTWATCHEDTODAY': 'TODAY'
            }[param]

            url = self._getUrl('/most-watched/')
            API = HDTrailerAPI(url)

            items = API.getMostWatched(_param)
            if items is not None:
                for item in items:
                    plot = None
                    if self._extract_plot:
                        url = self._getUrl(item.get('url'))
                        API = HDTrailerAPI(url)
                        plot = API.getPlot()

                    self.addDirectory(title=item.get('title'),
                                      poster=item.get('poster'),
                                      plot=plot, args=self._buildArgs(method='item', param='URL', tag=item.get('url')))

        else:
            _param = {
                'WEEK': 'MOSTWATCHEDWEEK',
                'TODAY': 'MOSTWATCHEDTODAY'
            }[param]

            self.setListView(param=_param, page=1)

    def setListLibraryView(self, **kwargs):

        if not self._db_enabled:
            url = self._getUrl('/poster-library/0/')
            API = HDTrailerAPI(url)
        else:
            try:
                API = DBAPI(self._db_config, None)
            except mysql.connector.Error as e:
                self._guiManager.setToastNotification(self._NAME, e.msg, image=self._ICON)
                return

        items = API.getLibraryLinks()
        if items is not None:
            for item in items:
                self.addDirectory(title=item.get('title'),
                                  args=self._buildArgs(method='list', param='LIBRARY', tag=item.get('tag')))

    def setNavView(self, **kwargs):
        param = kwargs.get('param')
        tag = kwargs.get('tag')
        nav = kwargs.get('navigation')
        if param is not None and nav is not None:
            items = json.loads(nav)
            for item in items:
                self.addDirectory(title=item.get('title'),
                                  args=self._buildArgs(method='list', param=param, tag=tag, page=item.get('tag')))

    def setListView(self, **kwargs):
        param = kwargs.get('param')
        page = kwargs.get('page')
        tag = kwargs.get('tag')
        if page is None:
            page = 1
        if not self._db_enabled:
            if 'MOSTWATCHED' not in param:
                url = self._getListUrl(param, page, tag)
                API = HDTrailerAPI(url)
            else:
                self.setListMostWatchedView(**kwargs)
                return
        else:
            _tag = {
                'list': param,
                'pageNumber': int(page),
                'pageSize': self._page_itemCount,
                'tag': tag
            }
            try:
                API = DBAPI(self._db_config, _tag)
            except mysql.connector.Error as e:
                self._guiManager.setToastNotification(self._NAME, e.msg, image=self._ICON)
                return

        items = API.getItems()

        if items is not None:
            for item in items:
                plot = None
                if not self._db_enabled:
                    if self._extract_plot and param != 'LIBRARY':
                        _url = self._getUrl(item.get('url'))
                        _API = HDTrailerAPI(_url)
                        plot = _API.getPlot()

                    self.addDirectory(title=item.get('title'), poster=item.get('poster'), plot=plot,
                                      args=self._buildArgs(method='item', param='URL', tag=item.get('url')))
                else:
                    self.addDirectory(title=item.get('title'), poster=item.get('poster'), plot=item.get('plot'),
                                      args=self._buildArgs(method='item', param='DB', tag=item.get('item_id')))

        navigation = API.getNavigation()
        if navigation is not None:
            self.addDirectory(title=self._t.getString(NAVIGATIONS),
                              poster=self._NAVART,
                              args=self._buildArgs(method='nav', param=param, tag=tag, navigation=navigation))

    def setHomeView(self, **args):
        self._guiManager.addDirectory(title=self._t.getString(LATEST), poster=self._ICON,
                                      args=self._buildArgs(method='list', param='LATEST'))
        self._guiManager.addDirectory(title=self._t.getString(LIBRARY), poster=self._ICON,
                                      args=self._buildArgs(method='list_library'))
        self._guiManager.addDirectory(title=self._t.getString(MOST_WATCHED_WEEK), poster=self._ICON,
                                      args=self._buildArgs(method='list', param='MOSTWATCHEDWEEK'))
        self._guiManager.addDirectory(title=self._t.getString(MOST_WATCHED_TODAY), poster=self._ICON,
                                      args=self._buildArgs(method='list', param='MOSTWATCHEDTODAY'))
        self._guiManager.addDirectory(title=self._t.getString(TOP_MOVIES), poster=self._ICON,
                                      args=self._buildArgs(method='list', param='TOPTEN'))
        self._guiManager.addDirectory(title=self._t.getString(OPENING_THIS_WEEK), poster=self._ICON,
                                      args=self._buildArgs(method='list', param='OPENING'))
        self._guiManager.addDirectory(title=self._t.getString(COMING_SOON), poster=self._ICON,
                                      args=self._buildArgs(method='list', param='COMINGSOON'))

    def _getUrl(self, url):
        return urllib.parse.urljoin(self._BASE_URL, url)

    def _getListUrl(self, param, page, tag):
        return self._getUrl(
            {
                'LATEST': urljoin('/page/', str(page) + "/"),
                'LIBRARY': urljoin('/poster-library/', str(tag) + "/"),
                'NAV': urljoin('/page/', str(page) + "/"),
                'TOPTEN': '/top-movies/',
                'OPENING': '/opening-this-week/',
                'COMINGSOON': '/coming-soon/'
            }[param]
        )

    @staticmethod
    def _buildArgs(**kwargs):
        method = kwargs.get('method')
        param = kwargs.get('param')
        page = kwargs.get('page')
        tag = kwargs.get('tag')
        navigation = kwargs.get('navigation')

        args = {
            'method': method
        }

        if param is not None:
            args['param'] = param

        if page is not None:
            args['page'] = page

        if tag is not None:
            args['tag'] = tag

        if navigation is not None:
            args['navigation'] = navigation

        return args


    @staticmethod
    def _get_query_args(s_args):
        args = urllib.parse.parse_qs(urllib.parse.urlparse(s_args).query)

        for key in args:
            args[key] = args[key][0]
        return args

    def hd_trailers(self):

        args = self._get_query_args(sys.argv[2])

        if args is None or args.__len__() == 0:
            args = self._buildArgs(method='home')

        method = args.get('method')
        param = args.get('param')
        page = args.get('page')
        tag = args.get('tag')
        navigation = args.get('navigation')

        {
            'home': self.setHomeView,
            'list': self.setListView,
            'nav': self.setNavView,
            'list_library': self.setListLibraryView,
            'list_most_watched': self.setListMostWatchedView,
            'item': self.setItemView
        }[method](param=param, page=page, tag=tag, navigation=navigation)

        self._guiManager.endOfDirectory()
