"""
get the movie list on movie.douban.com.
"""
import sys
import requests
import csv
from bs4 import BeautifulSoup
import expanddouban


def get_movie_url(category="", location=""):
    """ return a string corresponding to the URL of douban movie lists given category and location.
    arguments:
    category -- movie's category str()
    location -- movie's location str()
    """
    url = "https://movie.douban.com/tag/#/?sort=S&range=9,10&tags=电影"
    if category.__ne__(""):
        url += ",{}".format(category)
    if location.__ne__(""):
        url += ",{}".format(location)
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

    def __init__(self, name="", rate="", location="", category="", info_link="", cover_link=""):
        self.__name = name
        self.__rate = rate
        self.__location = location
        self.__category = category
        self.__info_link = info_link
        self.__cover_link = cover_link

    def get_name(self):
        """get name"""
        return self.__name

    def set_name(self, name):
        """set name"""
        self.__name = name

    def get_rate(self):
        """get rate"""
        return self.__rate

    def set_rate(self, rate):
        """set rate"""
        self.__rate = rate

    def get_location(self):
        """get location"""
        return self.__location

    def set_location(self, location):
        """set location"""
        self.__location = location

    def get_category(self):
        """get category"""
        return self.__category

    def set_category(self, category):
        """set category"""
        self.__category = category

    def get_info_link(self):
        """get info_link"""
        return self.__info_link

    def set_info_link(self, info_link):
        """set info_link"""
        self.__info_link = info_link

    def get_cover_link(self):
        """get cover_link"""
        return self.__cover_link

    def set_cover_link(self, cover_link):
        """set cover_link"""
        self.__cover_link = cover_link

# m = Movie("name", "rate", "location", "category", "info_link", "cover_link")
# print(m.get_name())


def get_movies(category="", location=""):
    """get the movie list you want"""
    movie_list = []
    movie = None

    url = get_movie_url(category, location)
    html = expanddouban.getHtml(url, loadmore=True)
    soup = BeautifulSoup(html, "html.parser")
    tag_list = soup.find(id="content").find(class_="list-wp").find_all("a")

    for tag in tag_list:
        movie = Movie()
        movie.set_name(str(tag.p.find(class_="title").string))
        movie.set_rate(str(tag.p.find(class_="rate").string))
        movie.set_info_link(str(tag.get("href")))
        movie.set_cover_link(str(tag.find("img").get("src")))
        movie.set_category(category)
        movie.set_location(location)
        movie_list.append(movie)

    return movie_list


with open(sys.path[0] + "\\movies.csv", "w", encoding="utf-8", newline="") as target:
    for m in get_movies("喜剧"):
        spamwriter = csv.writer(target, delimiter=',',
                                quotechar='|', quoting=csv.QUOTE_MINIMAL)
        spamwriter.writerow([m.get_name(), m.get_rate(), m.get_location(),
                             m.get_category(), m.get_info_link(), m.get_cover_link()])

    for m in get_movies("剧情"):
        spamwriter = csv.writer(target, delimiter=',',
                                quotechar='|', quoting=csv.QUOTE_MINIMAL)
        spamwriter.writerow([m.get_name(), m.get_rate(), m.get_location(),
                             m.get_category(), m.get_info_link(), m.get_cover_link()])

    for m in get_movies("动作"):
        spamwriter = csv.writer(target, delimiter=',',
                                quotechar='|', quoting=csv.QUOTE_MINIMAL)
        spamwriter.writerow([m.get_name(), m.get_rate(), m.get_location(),
                             m.get_category(), m.get_info_link(), m.get_cover_link()])
