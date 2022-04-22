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

