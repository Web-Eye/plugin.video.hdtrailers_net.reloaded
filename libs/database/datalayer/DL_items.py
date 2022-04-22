from libs.database.database_core import databaseCore

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
                 f'      SELECT ROW_NUMBER() OVER (ORDER BY order_date DESC, item_id ASC) AS rowNumber, items.item_id' \
                 f'            ,items.title, items.plot, items.poster_url' \
                 f'      FROM items' \
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

        sQuery = f'SELECT COUNT(*) FROM items WHERE {whereClause};'

        return databaseCore.executeScalar(cnx, sQuery, parameter)
