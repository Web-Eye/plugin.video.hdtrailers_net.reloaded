import math

import mysql.connector
import json
from libs.database.datalayer.DL_items import DL_items


class DBAPI:

    def __init__(self, db_config, tag):
        self._cnx = None
        self._pageNumber = tag['pageNumber']
        self._pageSize = tag['pageSize']

        self._cnx = mysql.connector.Connect(**db_config)

    def __del__(self):
        if self._cnx is not None:
            self._cnx.close()

    def getItems(self):
        query = {
            'project': 'HDTRAILERS',
            'page': self._pageNumber,
            'pageSize': self._pageSize
        }

        return DL_items.getItems(self._cnx, query)

    def getNavigation(self):
        lst_nav_items = []

        # if self._pageNumber > 1:
        #     lst_nav_items.append({'title': 'First', 'tag': 1})
        #
        # if self._pageNumber > 2:
        #     lst_nav_items.append({'title': 'Previous', 'tag': self._pageNumber - 1})

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

        # if currentPage < firstPage + 2:
        #     firstPage = None

        if currentPage == lastPage:
            nextPage = None

        # if currentPage > lastPage - 2:
        #     lastPage = None

        if minPage < firstPage:
            minPage = firstPage

        if minPage == currentPage:
            minPage = None

        if maxPage > lastPage:
            maxPage = lastPage

        if maxPage == currentPage:
            maxPage = None

        if minPage == firstPage:
            firstPage = None

        if maxPage == lastPage:
            lastPage = None

        if firstPage == currentPage:
            firstPage = None

        if lastPage == currentPage:
            lastPage = None

        t = 0

        # minPage = self._pageNumber - 4
        # if minPage < 2:
        #     minPage = 2
        # if minPage >= self._pageNumber:
        #     minPage = self._pageNumber




        if len(lst_nav_items) > 0:
            return json.dumps(lst_nav_items)

        return None

