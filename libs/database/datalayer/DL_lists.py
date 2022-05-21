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

from libs.database.database_core import databaseCore


class DL_lists:

    @staticmethod
    def getItems(cnx, query):
        items = []
        innerWhereClause = 'l.identifier = %s'
        parameter = (query['list'],)

        minItem = (query['page'] - 1) * query['pageSize'] + 1
        maxItem = minItem + query['pageSize'] - 1
        parameter += (minItem, maxItem,)

        sQuery = f'   SELECT item_id, title, plot, poster_url FROM (' \
                 f'      SELECT ROW_NUMBER() OVER (ORDER BY order_id ASC) AS rowNumber, i.item_id' \
                 f'            ,i.title, i.plot, i.poster_url' \
                 f'      FROM lists AS l' \
                 f'      LEFT JOIN items AS i ON l.item_id = i.item_id' \
                 f'      WHERE {innerWhereClause} ' \
                 f'   ) AS t' \
                 f'   WHERE t.rowNumber BETWEEN %s AND %s'

        cursor = databaseCore.executeReader(cnx, sQuery, parameter)
        if cursor is not None:
            rows = cursor.fetchall()
            for row in rows:
                items.append({
                    'item_id': int(row[0]),
                    'title': str(row[1]),
                    'plot': str(row[2]),
                    'poster': str(row[3])
                })

            cursor.close()
        return items

    @staticmethod
    def getCount(cnx, query):
        whereClause = 'identifier = %s'
        parameter = (query['list'],)

        sQuery = f'SELECT COUNT(*) FROM lists WHERE {whereClause};'

        return databaseCore.executeScalar(cnx, sQuery, parameter)
