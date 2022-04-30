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

import mysql.connector


class databaseCore:

    @staticmethod
    def executeReader(cnx, query, parameters=None):

        try:
            cursor = cnx.cursor()
            cursor.execute(query, parameters)
            return cursor

        except mysql.connector.Error as e:
            print(f"Error connecting to mysqlDB Platform: {e}")
            return None

    @staticmethod
    def executeScalar(cnx, query, parameters=None):
        retValue = None

        try:
            cursor = cnx.cursor()
            cursor.execute(query, parameters)
            row = cursor.fetchone()
            retValue = None
            if row is not None:
                retValue = row[0]

            cursor.close()
        except mysql.connector.Error as e:
            print(f"Error connecting to MariaDB Platform: {e}")

        return retValue
