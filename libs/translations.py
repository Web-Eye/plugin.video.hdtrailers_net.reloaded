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

HOME = 'home'
LATEST = 'latest'
LIBRARY = 'library'
MOST_WATCHED_WEEK = 'most_watched_week'
MOST_WATCHED_TODAY = 'most_watched_today'
TOP_MOVIES = 'top_movies'
OPENING_THIS_WEEK = 'opening_this_week'
COMING_SOON = 'coming_soon'
NAVIGATIONS = 'navigations'


class Translations:

    def __init__(self, addon):
        self._language = addon.getLocalizedString

    def getString(self, name):

        return {
            HOME:                   self._language(30100),
            LATEST:                 self._language(30101),
            LIBRARY:                self._language(30102),
            MOST_WATCHED_WEEK:      self._language(30103),
            MOST_WATCHED_TODAY:     self._language(30104),
            TOP_MOVIES:             self._language(30105),
            OPENING_THIS_WEEK:      self._language(30106),
            COMING_SOON:            self._language(30107),
            NAVIGATIONS:            self._language(30108)
        }[name]
