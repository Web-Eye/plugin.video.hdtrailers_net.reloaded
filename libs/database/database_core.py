import mysql.connector


class databaseCore:

    @staticmethod
    def executeReader(cnx, query, parameters=None):

        try:
            cursor = cnx.cursor()
            cursor.execute(query, parameters)
            return cursor

        except mysql.connector.Error as e:
            print(f"Error connecting to mysqlDB Platform: {e}")
            return None

    @staticmethod
    def executeScalar(cnx, query, parameters=None):
        retValue = None

        try:
            cursor = cnx.cursor()
            cursor.execute(query, parameters)
            row = cursor.fetchone()
            retValue = None
            if row is not None:
                retValue = row[0]

            cursor.close()
        except mysql.connector.Error as e:
            print(f"Error connecting to MariaDB Platform: {e}")

        return retValue
