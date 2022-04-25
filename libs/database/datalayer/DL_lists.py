from libs.database.database_core import databaseCore
from libs.tools import tools


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
