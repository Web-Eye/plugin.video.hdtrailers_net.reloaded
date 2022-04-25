import math

import mysql.connector
import json
from libs.database.datalayer.DL_items import DL_items
from libs.database.datalayer.DL_lists import DL_lists


class DBAPI:

    def __init__(self, db_config, tag):
        self._cnx = None
        if 'list' in tag:
            self._list_id = tag['list']
        if 'pageNumber' in tag:
            self._pageNumber = tag['pageNumber']
        if 'pageSize' in tag:
            self._pageSize = tag['pageSize']
        if 'item_id' in tag:
            self._item_id = tag['item_id']
        if 'quality_id' in tag:
            self._quality_id = tag['quality_id']

        self._cnx = mysql.connector.Connect(**db_config)

    def __del__(self):
        if self._cnx is not None:
            self._cnx.close()

    def getItems(self):
        return {
            'LATEST': self._getLatest,
            'TOPTEN': self._getList,
            'OPENING': self._getList,
            'COMING_SOON': self._getList,
            'MOSTWATCHEDWEEK': self._getList,
            'MOSTWATCHEDTODAY': self._getList
        }[self._list_id](self._list_id)

    def _getLatest(self):
        query = {
            'project': 'HDTRAILERS',
            'page': self._pageNumber,
            'pageSize': self._pageSize
        }

        return DL_items.getItems(self._cnx, query)

    def _getList(self, list_id):
        list_id = 'HDT_' + list_id
        query = {
            'project': 'HDTRAILERS',
            'list': list_id,
            'page': self._pageNumber,
            'pageSize': self._pageSize
        }

        return DL_lists.getItems(self._cnx, query)

    def getNavigation(self):
        lst_nav_items = []

        query = {
            'project': 'HDTRAILERS'
        }

        itemCount = DL_items.getCount(self._cnx, query)

        currentPage = self._pageNumber
        firstPage = 1
        prevPage = currentPage - 1
        nextPage = currentPage + 1
        lastPage = int(math.ceil(float(itemCount / self._pageSize)))
        minPage = currentPage - 4
        maxPage = currentPage + 4

        if currentPage == firstPage:
            prevPage = None

        if currentPage == lastPage:
            nextPage = None

        if minPage < firstPage:
            minPage = firstPage

        if minPage == currentPage:
            minPage = currentPage + 1

        if maxPage > lastPage:
            maxPage = lastPage

        if maxPage == currentPage:
            maxPage = currentPage - 1

        if minPage == firstPage:
            firstPage = None

        if maxPage == lastPage:
            lastPage = None

        if firstPage == currentPage:
            firstPage = None

        if lastPage == currentPage:
            lastPage = None

        if firstPage is not None:
            lst_nav_items.append({'title': 'First', 'tag': firstPage})

        if prevPage is not None:
            lst_nav_items.append({'title': 'Previous', 'tag': prevPage})

        if minPage is not None and maxPage is not None:
            for i in range(minPage, maxPage + 1):
                if i != currentPage:
                    lst_nav_items.append({'title': f'Page {i}', 'tag': i})

        if nextPage is not None:
            lst_nav_items.append({'title': 'Next', 'tag': nextPage})

        if lastPage is not None:
            lst_nav_items.append({'title': 'Last', 'tag': lastPage})

        if len(lst_nav_items) > 0:
            return json.dumps(lst_nav_items)

        return None

    def getItem(self):
        query = {
            'project': 'HDTRAILERS',
            'item_id': self._item_id,
            'quality': ['480p', '720p', '1080p', 'Best'][self._quality_id],
            'best_quality': self._quality_id == 3
        }

        trailers = DL_items.getItem(self._cnx, query)
        if trailers is not None and len(trailers) > 0:
            trailer_collection = []
            for trailer in trailers:
                trailer_collection.append({
                    'name': trailer['trailer_title'],
                    'date': trailer['broadcastOn_date'],
                    'trailer_type': trailer['trailer_tag'],
                    'link': {
                        'name': None,
                        'url': trailer['url'],
                        'size': trailer['size']
                    }
                })

            return {
                'title': trailers[0]['title'],
                'plot': trailers[0]['plot'],
                'poster': trailers[0]['poster'],
                'trailers': trailer_collection
            }




