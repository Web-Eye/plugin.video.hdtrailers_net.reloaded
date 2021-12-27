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

import logging  # , requests
# from bs4 import BeautifulSoup

# -- logger -----------------------------------------------
logger = logging.getLogger("plugin.video.hdtrailers.reloaded.api")


def parseItemPage(url):
    # page = requests.get(url)
    # content = BeautifulSoup(page.content, 'html.parser')
    # items = content.find_all('td', class_='indexTableTrailerImage')
    # for item in items:
    #     link = item.find('a')
    #     image = link.find('img', class_='indexTableTrailerImage')

    #     trailer_url = link['href']
    #     title = image['title']
    #     poster = image['src']

    return None, None