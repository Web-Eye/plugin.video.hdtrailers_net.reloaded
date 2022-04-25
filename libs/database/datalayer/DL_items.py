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
                 f'   FROM viewItems' \
                 f'   WHERE {whereClause}' \
                 f'   ORDER BY subitem_id ASC;'
                 # f'   ORDER BY si_tag ASC, broadCastOn_date DESC;'

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


