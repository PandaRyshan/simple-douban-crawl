"""
get the movie list on movie.douban.com.
"""
import sys
import csv
from bs4 import BeautifulSoup
import expanddouban
# from operator import itemgetter


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
        spamwriter = csv.writer(target, delimiter=',')
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


def analyse_data(category_list, location_list):
    """read data from movies.csv, build two movie subtotal dict"""
    def percent(total_by_loc, total_by_cat):
        """get percent"""
        pct = "%.2f%%" % (total_by_loc / total_by_cat * 100)
        return pct

    with open(sys.path[0] + "\\movies.csv", "r", encoding="utf-8", newline="") as target:
        reader = csv.reader(target, delimiter=',')
        movie_list = list(reader)

    msg = "{}电影数量排名前三的地区是{},{},{}, 分别占此类电影总数的百分比为{},{},{}. \n"

    with open(sys.path[0] + "\\output.txt", "w", encoding="utf-8", newline="") as f:
        for cat in category_list:
            temp = []
            total_by_cat = 0
            for loc in location_list:
                total_by_loc = 0
                for movie in movie_list:
                    if movie[3] == cat and movie[2] == loc:
                        total_by_cat += 1
                        total_by_loc += 1
                temp.append((loc, total_by_loc))
                temp = sorted(temp, key=lambda t: t[1], reverse=True)

            ratio = []
            for i in range(3):
                ratio.append(percent(temp[i][1], total_by_cat))
            print(msg.format(cat, temp[0][0], temp[1]
                             [0], temp[2][0], ratio[0], ratio[1], ratio[2]))
            f.write(msg.format(cat, temp[0][0], temp[1]
                               [0], temp[2][0], ratio[0], ratio[1], ratio[2]))

    # for movie in movie_list:
    #     category = movie.category
    #     location = movie.location

    #     if category in category_dict:
    #         category_dict[category] += 1
    #     else:
    #         category_dict[category] = 1

    #     if category in category_location_dict:
    #         if location in category_location_dict[category]:
    #             category_location_dict[category][location] += 1
    #         else:
    #             category_location_dict[category][location] = 1
    #     else:
    #         category_location_dict[category] = {location: 1}

    # items = category_location_dict.items()
    # location_num_dict = {}
    # result_list = []
    # item_num = 0
    # with open(sys.path[0] + "\\output.txt", "w", encoding="utf-8", newline="") as target:
    #     for item in items:
    #         location_num_dict = item[1]
    #         item_num = category_dict.get(item[0])
    #         target.write(str(item[0]) + ": ")
    #         result_list = sorted(location_num_dict.items(),
    #                              key=lambda t: t[1], reverse=True)
    #         result_list = result_list[0:3]
    #         for r in result_list:
    #             target.write("({}, {}, {}%)".format(
    #                 str(r[0]), str(r[1]), round(r[1] / item_num * 100, 2)))
    #         target.write("\n")


locations = get_all_locations()
categories = ["喜剧", "剧情", "动作"]
# locations = ['大陆', '美国', '香港', '台湾', '日本', '韩国', '英国', '法国', '德国', '意大利',
#              '西班牙', '印度', '泰国', '俄罗斯', '伊朗', '加拿大', '澳大利亚', '爱尔兰', '瑞典', '巴西', '丹麦']
getMovies(categories, locations)
analyse_data(categories, locations)
