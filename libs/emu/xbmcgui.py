class ListItem:

    def __init__(self, title):
        self.__title = title

    def setArt(self, value):
        print(f'listItem "{self.__title}": setArt({value})')

    def setProperty(self, property, value):
        print(f'listItem "{self.__title}": setProperty({property}, {value})')

    def setInfo(self, type, infoLabels):
        print(f'listItem "{self.__title}": setInfo({type}, {infoLabels})')

