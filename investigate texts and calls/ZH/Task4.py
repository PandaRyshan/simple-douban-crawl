"""
下面的文件将会从csv文件中读取读取短信与电话记录，
你将在以后的课程中了解更多有关读取文件的知识。
"""
import csv
import sys

with open(sys.path[0] + '\\texts.csv', 'r') as f:
    reader = csv.reader(f)
    texts = list(reader)

with open(sys.path[0] + '\\calls.csv', 'r') as f:
    reader = csv.reader(f)
    calls = list(reader)

"""
任务4:
电话公司希望辨认出可能正在用于进行电话推销的电话号码。
找出所有可能的电话推销员:
这样的电话总是向其他人拨出电话，
但从来不发短信、接收短信或是收到来电


请输出如下内容
"These numbers could be telemarketers: "
<list of numbers>
电话号码不能重复，每行打印一条，按字典顺序排序后输出。
"""


def filter_sales_number(texts_list, calls_list):
    """ filter the sales men's number """
    text_number_set = set()
    caller_set = set()
    called_set = set()
    sales_list = list()
    for text in texts_list:
        text_number_set.add(str(text[0]))
        text_number_set.add(str(text[1]))

    for call in calls_list:
        caller_set.add(str(call[0]))
        called_set.add(str(call[1]))

    for number in caller_set:
        if (number not in text_number_set) or (number not in called_set):
            sales_list.append(number)
    return sales_list


print("These numbers could be telemarketers: ")
for num in filter_sales_number(texts, calls):
    print(num)
