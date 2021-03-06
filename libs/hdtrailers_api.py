# -*- coding: utf-8 -*-
# Copyright 2021 WebEye
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#

import json
import logging
import requests
import urllib.parse
from decimal import Decimal, InvalidOperation
from bs4 import BeautifulSoup

# -- logger -----------------------------------------------
logger = logging.getLogger('plugin.video.hdtrailers.reloaded.api')


def _getContent(url):
    page = requests.get(url)
    return BeautifulSoup(page.content, 'html.parser')


def _getSize(value):
    if 'MB' in value:
        value = value.replace('MB', '')
        try:
            d = Decimal(value)
            return int(d * 1024 * 1024)
        except InvalidOperation:
            return 0


class HDTrailerAPI:

    def __init__(self, url, quality_id=None):
        self.__content = _getContent(url)
        if quality_id is not None:
            self.__quality = ['480p', '720p', '1080p', 'Best'][int(quality_id)]

    def __getItems(self, content):
        lst_items = []
        items = content.find_all('td', class_='indexTableTrailerImage')
        if items is not None:
            for item in items:
                link = item.find('a')
                image = link.find('img', class_='indexTableTrailerImage')
                if image is not None:
                    poster = urllib.parse.urljoin("http:", image['src'])
                    lst_items.append({'title': image['title'], 'poster': poster, 'url': link['href']})

        return lst_items

    def getItems(self):
        return self.__getItems(self.__content)

    def getNavigation(self):
        lst_nav_items = []
        navigation = self.__content.find('div', class_='libraryLinks nav-links-top')
        if navigation is not None:
            nav_items = navigation.find_all('a', class_='startLink')
            if nav_items is not None:
                for navItem in nav_items:
                    page = navItem.getText()
                    if page.isnumeric():
                        page = 'Page ' + page
                    elif 'Prev' in page:
                        page = 'Previous'
                    elif 'Next' in page:
                        page = 'Next'
                    lst_nav_items.append({'title': page, 'url': navItem['href']})

        if len(lst_nav_items) > 0:
            return json.dumps(lst_nav_items)

        return None

    def __getPlot(self, info):
        if info is not None:
            plot_block = info.find('p', class_='previewDescription')
            if plot_block is not None:
                return plot_block.find('span').getText()

    def getPlot(self):
        info = self.__content.find('td', class_='topTableInfo')
        return self.__getPlot(info)

    def getItem(self):
        title = ''
        plot = ''
        poster = ''

        info = self.__content.find('td', class_='topTableInfo')
        if info is not None:
            title = info.find('h1', class_='previewTitle').getText()
            plot = self.__getPlot(info)
            poster = urllib.parse.urljoin("http:", info.find('img')['src'])

        link_block = self.__content.find('table', class_='bottomTable')
        link_content = link_block.find_all(lambda tag: (tag.name == 'tr' and tag.has_attr('itemprop') and tag['itemprop'] == 'trailer') or
                                                       (tag.name == 'td' and tag.has_attr('class') and tag['class'][0] == 'bottomTableSet') or
                                                       (tag.name == 'td' and tag.has_attr('class') and tag['class'][0] == 'bottomTableFileSize')
                                          )

        trailer_type = 'Trailers'
        trailer_name = ''
        trailer_date = ''
        trailer_collection = []
        link_collection = []
        i = 0

        for link in link_content:
            if link.name == 'td' and link.has_attr('class') and link['class'][0] == 'bottomTableSet':
                trailer_type_block = link.find('h2')
                if trailer_type_block is not None:
                    trailer_type = trailer_type_block.getText()

            elif link.name == 'tr' and link.has_attr('itemprop') and link['itemprop'] == 'trailer':
                if len(link_collection) > 0:

                    link_item = None
                    link_collection = list(filter(lambda item: 'yahoo-redir.php' not in item['url'] and
                                                               'www.youtube.com' not in item['url'] and
                                                               'cdn.videos.dolimg.com' not in item['url'] and
                                                               'avideos.5min.com' not in item['url'], link_collection))

                    if self.__quality != 'Best':
                        link_collection = list(filter(lambda item: item['name'] == self.__quality, link_collection))
                    else:
                        link_collection.reverse()

                    if link_collection is not None and len(link_collection) != 0:
                        link_item = link_collection[0]

                    if link_item is not None:
                        trailer_collection.append({'name': trailer_name, 'date': trailer_date, 'trailer_type': trailer_type, 'link': link_item})

                link_collection = []
                i = 0

                trailer_name_block = link.find('td', class_='bottomTableName')
                if trailer_name_block is not None:
                    span_tag = trailer_name_block.find('span')
                    if span_tag is not None:
                        trailer_name = span_tag.getText()

                trailer_date_block = link.find('td', class_='bottomTableDate')
                if trailer_date_block is not None:
                    trailer_date = trailer_date_block.getText()

                links = link.find_all('td', class_='bottomTableResolution')
                for trailer_link in links:
                    a_tag = trailer_link.find('a')
                    if a_tag is not None:
                        link_collection.append({'name': a_tag.getText(), 'url': a_tag['href']})

            elif link.name == 'td' and link.has_attr('class') and link['class'][0] == 'bottomTableFileSize':
                size = _getSize(link.getText())
                if size is not None:
                    link_collection[i]['size'] = size
                    i += 1

        if len(link_collection) > 0:
            link_item = None
            link_collection = list(filter(lambda item: 'yahoo-redir.php' not in item['url'], link_collection))

            if self.__quality != 'Best':
                link_collection = list(filter(lambda item: item['name'] == self.__quality, link_collection))
            else:
                link_collection.reverse()

            if link_collection is not None and len(link_collection) != 0:
                link_item = link_collection[0]

            if link_item is not None:
                trailer_collection.append({'name': trailer_name, 'date': trailer_date, 'trailer_type': trailer_type, 'link': link_item})

        movie_item = {'title': title, 'plot': plot, 'poster': poster, 'trailers': trailer_collection}
        return movie_item

    def getMostWatched(self, _tag):
        lst_items = []
        indexTable = self.__content.find('table', class_='indexTable')
        if indexTable is not None:
            trItems = indexTable.find_all(lambda tag: tag.name == 'tr')
            if trItems is not None:
                matched = False
                for trItem in trItems:
                    if trItem.find('th', class_='mainHeading'):
                        if not matched:
                            divBlock = trItem.find(lambda tag: tag.name == 'div' and _tag in tag.getText())
                            matched = (divBlock is not None)
                        else:
                            break

                    elif matched:
                        lst_items.extend(self.__getItems(trItem))

        return lst_items

    def getLibraryLinks(self):
        lst_items = []
        item = self.__content.find('div', class_='libraryLinks')
        if item is not None:
            items = item.find_all(lambda tag: tag.name == 'a' and tag.getText() != 'On' and tag.getText() != 'Off')
            if items is not None:
                for link in items:
                    lst_items.append({'title': link.getText(), 'url': link['href']})

        return lst_items

