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

import logging
import xmbcaddon


# -- Constants ----------------------------------------------
ADDON_ID = 'plugin.video.hdtrailers_net.reloaded'
BASE_URL = 'http://www.hd-trailers.net/'
LATEST_PATH = 'page'
LIBRARY_PATH = 'library'
MOST_WATCHED_PATH = 'most-watched'
TOP10_PATH = 'top-movies'
OPENING_PATH = 'opening-this-week'
COMING_SOON_PATH = 'coming-soon'

# -- Settings -----------------------------------------------
logger = logging.getLogger("plugin.video.hdtrailers_net.reloaded")

# -- Settings -----------------------------------------------
addon = xbmcaddon.Addon(id=ADDON_ID)
quality_id = addon.getSetting('quality')
quality = ['480p', '720p', '1080p'][int(quality_id)]
start_page_id = addon.getsetting('start_page')


def hdtrailers():
    pass

