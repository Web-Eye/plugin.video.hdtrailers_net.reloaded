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

def addDirectoryItem(handle, url, listitem, isFolder):
    print(f'addDirectoryItem({handle}, {url}, {listitem}, {isFolder})')


def endOfDirectory(arg):
    print(f'endOfDirectory({arg})')


def setContent(arg, value):
    print(f'setContent({arg}, {value})')


def setPluginFanart(arg, value):
    print(f'setPluginFanart({arg}, {value})')


