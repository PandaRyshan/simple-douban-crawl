"""
get the movie list on movie.douban.com.
"""
import sys
import csv
from bs4 import BeautifulSoup
import expanddouban
from operator import itemgetter


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
    """ movie class """
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
    """get the movie list you want
    category -- movie's category str()
    location -- movie's location str()
    """
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


def get_all_locations():
    """get all available locations"""
    location_list = []
    html = expanddouban.getHtml("https://movie.douban.com/tag")
    soup = BeautifulSoup(html, "html.parser")
    category_tag_list = soup.find(id="content").find(class_="tags").contents[2].contents
    for index in range(1, len(category_tag_list)):
        location_list.append(str(category_tag_list[index].span.string))
    return location_list


def build_movie_dict():
    """build two movie subtotal dict"""
    movie_list = []
    with open(sys.path[0] + "\\movies.csv", "r", encoding="utf-8", newline="") as target:
        reader = csv.reader(target, delimiter=',',
                            quotechar='|', quoting=csv.QUOTE_MINIMAL)
        # translate all data to the Movie object list
        movie = None
        for row in reader:
            movie = Movie(row[0], row[1], row[2], row[3])
            movie_list.append(movie)

    # group movies by category, calculate subtotal
    category_dict = {}

    # group movies by category & location, calculate subtotal
    category_location_dict = {}
    category = ""
    location = ""

    for movie in movie_list:
        category = movie.get_category()
        location = movie.get_location()

        if category in category_dict:
            category_dict[category] += 1
        else:
            category_dict[category] = 1

        if category in category_location_dict:
            if location in category_location_dict[category]:
                category_location_dict[category][location] += 1
            else:
                category_location_dict[category][location] = 1
        else:
            category_location_dict[category] = {location: 1}

    return (category_dict, category_location_dict)


def analyse_data(tuple_of_dict):
    """analyse the data
    统计你所选取的每个电影类别中，数量排名前三的地区有哪些，分别占此类别电影总数的百分比为多少
    将你的结果输出文件 `output.txt`
    """
    category_dict, category_location_dict = tuple_of_dict
    items = category_location_dict.items()

    with open(sys.path[0] + "\\output.txt", "w", encoding="utf-8", newline="") as target:
        for item in items:
            location_dict = item[1]
            # print(sorted(location_dict.items(), key=itemgetter(1), reverse=True))
            # print(sorted(location_dict.items(), key=lambda t: t[1], reverse=True))
            # 这里如果不使用这两种方法，如何给sort方法传递合适的key呢？

            item_num = category_dict.get(item[0])
            target.write(str(item[0]) + ": ")
            result_list = sorted(location_dict.items(), key=lambda t: t[1], reverse=True)
            result_list = result_list[0:3]
            for r in result_list:
                target.write("({}, {}, {}%)".format(
                    str(r[0]), str(r[1]), round(r[1] / item_num * 100, 2)))
            target.write("\n")


def start_fetch(category_list, location_list):
    """ fetch data and write data to the csv file
    argument:
    category_list -- [str, str, ...]
    """
    with open(sys.path[0] + "\\movies.csv", "w", encoding="utf-8", newline="") as target:
        for category in category_list:
            for location in location_list:
                for m in get_movies(category, location):
                    spamwriter = csv.writer(target, delimiter=',',
                                            quotechar='|', quoting=csv.QUOTE_MINIMAL)
                    spamwriter.writerow([m.get_name(), m.get_rate(), m.get_location(),
                                         m.get_category(), m.get_info_link(), m.get_cover_link()])


# start_fetch(["喜剧", "剧情", "动作"], get_all_locations())
analyse_data(build_movie_dict())
