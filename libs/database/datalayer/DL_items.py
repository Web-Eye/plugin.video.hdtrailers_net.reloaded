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
from libs.tools import tools


class DL_items:

    @staticmethod
    def getItems(cnx, query):
        items = []
        innerWhereClause = 'project = %s'
        parameter = (query['project'],)

        minItem = (query['page'] - 1) * query['pageSize'] + 1
        maxItem = minItem + query['pageSize'] - 1
        parameter += (minItem, maxItem, )

        sQuery = f'   SELECT * FROM (' \
                 f'      SELECT ROW_NUMBER() OVER (ORDER BY order_date DESC, item_id ASC) AS rowNumber' \
                 f'            ,viewItems.item_id ,viewItems.title, viewItems.plot, viewItems.poster_url' \
                 f'      FROM viewItems' \
                 f'      WHERE {innerWhereClause}' \
                 f'   ) AS t' \
                 f'   WHERE t.rowNumber BETWEEN %s AND %s;'

        cursor = databaseCore.executeReader(cnx, sQuery, parameter)
        if cursor is not None:
            rows = cursor.fetchall()
            for row in rows:
                items.append({
                    'item_id': int(row[1]),
                    'title': str(row[2]),
                    'plot': str(row[3]),
                    'poster': str(row[4])
                })

            cursor.close()
        return items

    @staticmethod
    def getCount(cnx, query):
        whereClause = 'project = %s'
        parameter = (query['project'],)

        tag = query.get('tag')
        if tag is not None:
            if tag == '0':
                whereClause += ' AND title REGEXP \'^[a-z]+\' = 0'
            else:
                whereClause += ' AND title LIKE %s'
                parameter += (tag + '%',)

        sQuery = f'SELECT COUNT(*) FROM viewItems WHERE {whereClause};'

        return databaseCore.executeScalar(cnx, sQuery, parameter)

    @staticmethod
    def getItem(cnx, query):
        trailers = []
        whereClause = 'project = %s AND item_id = %s'
        parameter = (query['project'], query['item_id'], )

        if query['best_quality']:
            whereClause += ' AND best_quality = 1'
        else:
            whereClause += ' AND quality = %s'
            parameter += (query['quality'], )

        sQuery = f'SELECT title, plot, poster_url, si_title, si_tag, broadcastOn_date, quality, hoster, size, url ' \
                 f'   FROM viewItemLinks' \
                 f'   WHERE {whereClause}' \
                 f'   ORDER BY subitem_id ASC;'

        cursor = databaseCore.executeReader(cnx, sQuery, parameter)
        if cursor is not None:
            rows = cursor.fetchall()
            for row in rows:
                trailers.append({
                    'title': tools.estr(row[0]),
                    'plot': tools.estr(row[1]),
                    'poster':  tools.estr(row[2]),
                    'trailer_title':  tools.estr(row[3]),
                    'trailer_tag':  tools.estr(row[4]),
                    'broadcastOn_date':  tools.estr(row[5]),
                    'quality':  tools.estr(row[6]),
                    'hoster':  tools.estr(row[7]),
                    'size':  tools.eint(row[8]),
                    'url':  tools.estr(row[9])
                })

            cursor.close()
        return trailers

    @staticmethod
    def getLibraryItems(cnx, query):
        items = []
        innerWhereClause = 'project = %s'
        parameter = (query['project'],)

        tag = query.get('tag')
        if tag == '0':
            innerWhereClause += ' AND title REGEXP \'^[a-z]+\' = 0'
        else:
            innerWhereClause += ' AND title LIKE %s'
            parameter += (tag + '%',)

        minItem = (query['page'] - 1) * query['pageSize'] + 1
        maxItem = minItem + query['pageSize'] - 1
        parameter += (minItem, maxItem,)

        sQuery = f'   SELECT * FROM (' \
                 f'      SELECT ROW_NUMBER() OVER (ORDER BY title ASC) AS rowNumber, viewItems.item_id' \
                 f'            ,viewItems.title, viewItems.plot, viewItems.poster_url' \
                 f'      FROM viewItems' \
                 f'      WHERE {innerWhereClause}' \
                 f'   ) AS t' \
                 f'   WHERE t.rowNumber BETWEEN %s AND %s;'

        cursor = databaseCore.executeReader(cnx, sQuery, parameter)
        if cursor is not None:
            rows = cursor.fetchall()
            for row in rows:
                items.append({
                    'item_id': int(row[1]),
                    'title': str(row[2]),
                    'plot': str(row[3]),
                    'poster': str(row[4])
                })

            cursor.close()
        return items
