import sys
import time
import requests
import lxml
import expanddouban
from bs4 import BeautifulSoup
from selenium import webdriver


"""
return a string corresponding to the URL of douban movie lists given category and location.
"""


def get_movie_url(category, location):
    """ return a string corresponding to the URL of douban movie lists given category and location.
    arguments:
    category -- movie's category str()
    location -- movie's location str()
    """
    url = "https://movie.douban.com/tag/#/?sort=S&tags=电影"
    url += ",{},{}".format(category, location)
    return url


# html = expanddouban.getHtml(get_movie_url("喜剧", "大陆"), True)
# print(html)


class Movie(object):
    """ a movie class """
    __name = ""
    __rate = ""
    __category = ""
    __location = ""
    __info_link = ""
    __cover_link = ""

    def __init__(self, name, rate, location, category, info_link, cover_link):
        self.__name = name
        self.__rate = rate
        self.__location = location
        self.__category = category
        self.__info_link = info_link
        self.__cover_link = cover_link

    def get_name(self):
        """get name"""
        return self.__name

    def get_rate(self):
        """get rate"""
        return self.__rate

    def get_location(self):
        """get location"""
        return self.__location

    def get_category(self):
        """get category"""
        return self.__category

    def get_info_link(self):
        """get info_link"""
        return self.__info_link

    def get_cover_link(self):
        """get cover_link"""
        return self.__cover_link


# m = Movie("name", "rate", "location", "category", "info_link", "cover_link")
# print(m.get_name())


def get_movies(category, location):
    """get the movie list you want"""
    url = get_movie_url(category, location)
    html = expanddouban.getHtml(url)
    with open(sys.path[0] + "\\output.txt", "w", encoding="utf-8") as target:
        target.write(html)
    return []


get_movies("喜剧", "大陆")

# with open(sys.path[0] + "\\output.txt", "w", encoding="utf-8") as target:
#     target.write("测试")
