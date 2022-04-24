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
