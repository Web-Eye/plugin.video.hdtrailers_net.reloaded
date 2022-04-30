import time
from datetime import datetime


class tools:

    @staticmethod
    def eint(value, default=0):
        if value is not None:
            return int(value)

        return default

    @staticmethod
    def estr(value, default=''):
        if value is not None:
            return str(value)

        return default

    @staticmethod
    def getDateTime(strDateTime, strFormat):
        return datetime(*(time.strptime(strDateTime, strFormat)[0:6]))

    @staticmethod
    def datetimeToString(dt, dstFormat):
        return dt.strftime(dstFormat)

    @staticmethod
    def convertDateTime(strDateTime, srcFormat, dstFormat):

        try:
            dt = tools.getDateTime(strDateTime, srcFormat)
            if dt is not None:
                return dt.strftime(dstFormat)

        except ValueError:
            return None

