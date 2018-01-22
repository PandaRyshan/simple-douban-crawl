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
任务3:
(080)是班加罗尔的固定电话区号。
固定电话号码包含括号，
所以班加罗尔地区的电话号码的格式为(080)xxxxxxx。

第一部分: 找出被班加罗尔地区的固定电话所拨打的所有电话的区号和移动前缀（代号）。
 - 固定电话以括号内的区号开始。区号的长度不定，但总是以 0 打头。
 - 移动电话没有括号，但数字中间添加了
   一个空格，以增加可读性。一个移动电话的移动前缀指的是他的前四个
   数字，并且以7,8或9开头。
 - 电话促销员的号码没有括号或空格 , 但以140开头。

输出信息:
"The numbers called by people in Bangalore have codes:"
 <list of codes>
代号不能重复，每行打印一条，按字典顺序排序后输出。

第二部分: 由班加罗尔固话打往班加罗尔的电话所占比例是多少？
换句话说，所有由（080）开头的号码拨出的通话中，
打往由（080）开头的号码所占的比例是多少？

输出信息:
"<percentage> percent of calls from fixed lines in Bangalore are calls
to other fixed lines in Bangalore."
注意：百分比应包含2位小数。
"""


def get_number_prefix(calls_list):
    """
    param: list. Your calls list.
    return: list. The prefix list.
    """
    result = set()
    number_type = None
    caller = None
    called = None
    for call in calls_list:
        caller = str(call[0])
        called = str(call[1])
        number_type = number_type_filter(called)
        if caller.startswith("(080)"):
            if number_type == "telephone":
                result.add(called[1:4])
            elif (number_type == "mobile") or (number_type == "sales"):
                result.add(called[:4])
    if result is not None:
        result = list(result)
        result.sort()
        return result
    else:
        return None


def number_type_filter(phone_number):
    """
    filte the phone_number's type

    param: string. Your phone number
    return: string. "telephone", "mobile", "sales"
    """
    if str(phone_number).startswith("(0"):
        return "telephone"
    elif " " in str(phone_number) and (
            str(phone_number).startswith("7") or
            str(phone_number).startswith("8") or
            str(phone_number).startswith("9")
    ):
        return "mobile"
    elif str(phone_number).startswith("140"):
        return "sales"
    return None


def print_anwser1():
    """ print the Q1 """
    print("The numbers called by people in Bangalore have codes:")
    for prefix in get_number_prefix(calls):
        print(prefix)


def count_ratio(calls_list):
    """ count the ratio """
    count_all = len(calls_list)
    count_condition = 0
    caller = None
    called = None
    for call in calls_list:
        caller = str(call[0])
        called = str(call[1])
        if caller.startswith("(080)") and called.startswith("(080)"):
            count_condition += 1
    return round(count_condition / count_all, 2)


print_anwser1()
print(count_ratio(calls))
