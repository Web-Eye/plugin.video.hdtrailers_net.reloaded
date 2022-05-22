# -*- coding: utf-8 -*-
# Copyright 2022 WebEye
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

import xbmcplugin
import xbmcgui
import xbmc

import urllib.parse


def getScreenHeight():
    return xbmcgui.getScreenHeight()


def getScreenWidth():
    return xbmcgui.getScreenWidth()


class GuiManager:

    SORT_METHOD_NONE = xbmcplugin.SORT_METHOD_NONE
    SORT_METHOD_DATE = xbmcplugin.SORT_METHOD_DATE
    SORT_METHOD_DURATION = xbmcplugin.SORT_METHOD_DURATION
    SORT_METHOD_TITLE = xbmcplugin.SORT_METHOD_TITLE

    def __init__(self, argv, addon_id, default_image_url, fanart):
        self._argv = int(argv)
        self._addon_id = addon_id
        self._default_image_url = default_image_url
        self._fanart = fanart

        xbmcplugin.setPluginFanart(self._argv, self._fanart)

    def setContent(self, content):
        xbmcplugin.setContent(self._argv, content)

    def __setEntity(self, title, url, art, _property, _type, infolabels, isFolder):
        li = xbmcgui.ListItem(str(title))
        if art is not None:
            li.setArt(art)

        if _property is not None:
            for key, value in _property.items():
                li.setProperty(key, value)

        if _type is not None and infolabels is not None:
            li.setInfo(type=_type, infoLabels=infolabels)

        xbmcplugin.addDirectoryItem(handle=self._argv, url=url, listitem=li, isFolder=isFolder)

    def addDirectory(self, title, poster=None, fanArt=None, _type=None, infoLabels=None, args=None):
        art = {}
        _property = {}

        if poster is not None:
            art['thumb'] = poster
        else:
            art['thumb'] = self._default_image_url

        if fanArt is not None:
            _property['Fanart_Image'] = fanArt
        elif self._fanart is not None:
            _property['Fanart_Image'] = self._fanart

        url = 'plugin://' + self._addon_id + '/?' + urllib.parse.urlencode(args)
        self.__setEntity(title, url, art, _property, _type, infoLabels, True)

    def addItem(self, title, url, poster=None, fanArt=None, _type=None, infoLabels=None):
        art = {}
        _property = {}

        if poster is not None:
            art['thumb'] = poster
        else:
            art['thumb'] = self._default_image_url

        if fanArt is not None:
            _property['Fanart_Image'] = fanArt
        elif self._fanart is not None:
            _property['Fanart_Image'] = self._fanart

        _property['IsPlayable'] = 'true'

        self.__setEntity(title, url, art, _property, _type, infoLabels, False)

    def addSortMethod(self, sortMethod):
        xbmcplugin.addSortMethod(self._argv, sortMethod)

    def endOfDirectory(self):
        xbmcplugin.endOfDirectory(self._argv)

    @staticmethod
    def setToastNotification(header, message, time=5000, image=None):
        xbmc.executebuiltin('Notification(%s, %s, %d, %s)' % (header, message, time, image))
