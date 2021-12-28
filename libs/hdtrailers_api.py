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

import logging, requests, json
from bs4 import BeautifulSoup

# -- logger -----------------------------------------------
logger = logging.getLogger("plugin.video.hdtrailers.reloaded.api")


class HDTrailerAPI:

    @staticmethod
    def __getcontent(url):
        page = requests.get(url)
        return BeautifulSoup(page.content, 'html.parser')

    def parseItemsPage(self, url):
        content = self.__getcontent(url)

        lst_items = []
        items = content.find_all('td', class_='indexTableTrailerImage')
        if items is not None:
            for item in items:
                link = item.find('a')
                image = link.find('img', class_='indexTableTrailerImage')
                lst_items.append({'title':  image['title'], 'poster': image['src'], 'url': link['href']})

        lst_nav_items = []
        navigation = content.find('div', class_='libraryLinks nav-links-top')
        if navigation is not None:
            navItems = navigation.find_all('a', class_='startLink')
            if navItems is not None:
                for navItem in navItems:
                    page = navItem.getText()
                    if page.isnumeric():
                        page = 'Page ' + page
                    lst_nav_items.append({'title': page, 'url': navItem['href']})

        return lst_items, json.dumps(lst_nav_items)

    def parseItemPage(self, url):
        content = self.__getcontent(url)

        info = content.find('td', class_='topTableInfo')
        if info is not None:
            Title = info.find('h1', class_='previewTitle').getText()
            PlotBlock = info.find('p', class_='previewDescription')
            if PlotBlock is not None:
                Plot = PlotBlock.find('span').getText()
            Poster = info.find('img')['src']

        links = content.find('table', class_='bottomTable')
        test = links.find_all('td', class_='bottomTableName')



        # links
        # infolabels.video
            # title
            # plot (plotoutline)
            # size
            # date
            # aired
