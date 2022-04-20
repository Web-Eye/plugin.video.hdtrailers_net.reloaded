import mysql.connector
# from libs.database.datalayer.dl_items import DL_items


class DBAPI:

    def __init__(self, db_config, tag):
        self._cnx = mysql.connector.Connect(**db_config)

    def __del__(self):
        self._cnx.close()

