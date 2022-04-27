import math

import mysql.connector
import json
from libs.database.datalayer.DL_items import DL_items
from libs.database.datalayer.DL_lists import DL_lists


class DBAPI:

    def __init__(self, db_config, tag):
        self._cnx = None
        if tag is not None:
            self._list_id = tag.get('list')
            self._pageNumber = tag.get('pageNumber')
            self._pageSize = tag.get('pageSize')
            self._item_id = tag.get('item_id')
            self._quality_id = tag.get('quality_id')
            self._tag = tag.get('tag')

        self._cnx = mysql.connector.Connect(**db_config)

    def __del__(self):
        if self._cnx is not None:
            self._cnx.close()

    def getItems(self):
        return {
            'LATEST': self._getLatest,
            'LIBRARY': self._getLibrary,
            'TOPTEN': self._getList,
            'OPENING': self._getList,
            'COMINGSOON': self._getList,
            'MOSTWATCHEDWEEK': self._getList,
            'MOSTWATCHEDTODAY': self._getList
        }[self._list_id](self._list_id)

    def _getLatest(self, tag):
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
            'project': 'HDTRAILERS',
            'list': 'HDT_' + self._list_id,
            'tag': self._tag
        }

        if self._list_id == 'LATEST' or self._list_id == 'LIBRARY':
            itemCount = DL_items.getCount(self._cnx, query)
        else:
            itemCount = DL_lists.getCount(self._cnx, query)

        if itemCount == 0:
            return None

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

        # TODO add self._tag to returnvalue

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

    def getLibraryLinks(self):
        return [{'title': '#', 'tag': '0'}, {'title': 'A', 'tag': 'a'}, {'title': 'B', 'tag': 'b'},
                {'title': 'C', 'tag': 'c'}, {'title': 'D', 'tag': 'd'}, {'title': 'E', 'tag': 'e'},
                {'title': 'F', 'tag': 'f'}, {'title': 'G', 'tag': 'g'}, {'title': 'H', 'tag': 'h'},
                {'title': 'I', 'tag': 'i'}, {'title': 'J', 'tag': 'j'}, {'title': 'K', 'tag': 'k'},
                {'title': 'L', 'tag': 'l'}, {'title': 'M', 'tag': 'm'}, {'title': 'N', 'tag': 'n'},
                {'title': 'O', 'tag': 'o'}, {'title': 'P', 'tag': 'p'}, {'title': 'Q', 'tag': 'q'},
                {'title': 'R', 'tag': 'r'}, {'title': 'S', 'tag': 's'}, {'title': 'T', 'tag': 't'},
                {'title': 'U', 'tag': 'u'}, {'title': 'V', 'tag': 'v'}, {'title': 'W', 'tag': 'w'},
                {'title': 'X', 'tag': 'x'}, {'title': 'Y', 'tag': 'y'}, {'title': 'Z', 'tag': 'z'}]

    def _getLibrary(self, tag):
        query = {
            'project': 'HDTRAILERS',
            'page': self._pageNumber,
            'pageSize': self._pageSize,
            'tag': self._tag
        }

        return DL_items.getLibraryItems(self._cnx, query)
