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

import time
from datetime import datetime


class tools:

    @staticmethod
    def eint(value, default=0):
        if value is not None:
            return int(value)

        return default

    @staticmethod
    def estr(value, default=''):
        if value is not None:
            return str(value)

        return default

    @staticmethod
    def getDateTime(strDateTime, strFormat):
        return datetime(*(time.strptime(strDateTime, strFormat)[0:6]))

    @staticmethod
    def datetimeToString(dt, dstFormat):
        return dt.strftime(dstFormat)

    @staticmethod
    def convertDateTime(strDateTime, srcFormat, dstFormat):

        try:
            dt = tools.getDateTime(strDateTime, srcFormat)
            if dt is not None:
                return dt.strftime(dstFormat)

        except ValueError:
            return None
