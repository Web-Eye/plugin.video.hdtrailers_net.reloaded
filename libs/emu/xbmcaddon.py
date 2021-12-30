class Addon:

    def __init__(self, id):
        pass

    def getSetting(self, name):

        if name == 'quality':
            return 2
        elif name == 'start_page':
            return 1

    def getLocalizedString(self, id):
        return {
            30100: 'Home',
            30101: 'Latest',
            30102: 'Library',
            30103: 'Most Watched',
            30104: 'Top Movies',
            30105: 'Opening This Week',
            30106: 'Coming Soon',
            30107: 'Navigations'
        }[id]

