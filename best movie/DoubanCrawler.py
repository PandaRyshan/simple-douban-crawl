"""
get the movie list on movie.douban.com.
"""
import sys
import csv
from bs4 import BeautifulSoup
import expanddouban
from operator import itemgetter


def getMovieUrl(category="", location=""):
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


class Movie(object):
    def __init__(self, name, rate, location, category, info_link, cover_link):
        self.name = name
        self.rate = rate
        self.location = location
        self.category = category
        self.info_link = info_link
        self.cover_link = cover_link

    def printData(self):
        return "{},{},{},{},{},{}".format(self.name, self.rate, self.location, self.category, self.info_link, self.cover_link)


def getMovies(category_list="", location_list=""):
    """get the movie list you want
    category -- movie's category str()
    location -- movie's location str()
    """
    with open(sys.path[0] + "\\movies.csv", "w", encoding="utf-8", newline="") as target:
        spamwriter = csv.writer(target, delimiter=',',
                                quotechar='|', quoting=csv.QUOTE_MINIMAL)
        for cat in category_list:
            for loc in location_list:
                html = expanddouban.getHtml(getMovieUrl(cat, loc), True)
                soup = BeautifulSoup(html, 'html.parser')
                content_a = soup.find(
                    class_='list-wp').find_all('a', recursive=False)
                for element in content_a:
                    m_name = element.find(class_='title').string
                    m_rate = element.find(class_='rate').string
                    m_location = loc
                    m_category = cat
                    m_info_link = element.get('href')
                    m_cover_link = element.find('img').get('src')
                    spamwriter.writerow(
                        [m_name, m_rate, m_location, m_category,
                         m_info_link, m_cover_link, m_cover_link])


def get_all_locations():
    """get all available locations"""
    location_list = []
    html = expanddouban.getHtml("https://movie.douban.com/tag")
    soup = BeautifulSoup(html, "html.parser")
    category_tag_list = soup.find(id="content").find(
        class_="tags").contents[2].contents
    for index in range(1, len(category_tag_list)):
        location_list.append(str(category_tag_list[index].span.string))
    return location_list


def build_movie_dict():
    """read data from movies.csv, build two movie subtotal dict"""
    movie_list = []
    with open(sys.path[0] + "\\movies.csv", "r", encoding="utf-8", newline="") as target:
        reader = csv.reader(target, delimiter=',',
                            quotechar='|', quoting=csv.QUOTE_MINIMAL)
        # translate all data to the Movie object list
        movie = None
        for row in reader:
            movie = Movie(row[0], row[1], row[2], row[3], row[4], row[5])
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
    """analyse the data"""
    category_num_dict, category_location_dict = tuple_of_dict
    items = category_location_dict.items()
    location_num_dict = None
    result_list = None
    item_num = 0
    with open(sys.path[0] + "\\output.txt", "w", encoding="utf-8", newline="") as target:
        for item in items:
            location_num_dict = item[1]
            item_num = category_num_dict.get(item[0])
            target.write(str(item[0]) + ": ")
            result_list = sorted(location_num_dict.items(),
                                 key=lambda t: t[1], reverse=True)
            result_list = result_list[0:3]
            for r in result_list:
                target.write("({}, {}, {}%)".format(
                    str(r[0]), str(r[1]), round(r[1] / item_num * 100, 2)))
            target.write("\n")


getMovies(["喜剧", "剧情", "动作"], get_all_locations())
analyse_data(build_movie_dict())
