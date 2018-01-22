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
任务2: 哪个电话号码的通话总时间最长? 不要忘记，用于接听电话的时间也是通话时间的一部分。
输出信息:
"<telephone number> spent the longest time, <total time> seconds, on the phone during
September 2016.".

提示: 建立一个字典，并以电话号码为键，通话总时长为值。
这有利于你编写一个以键值对为输入，并修改字典的函数。
如果键已经存在于字典内，为键所对应的值加上对应数值；
如果键不存在于字典内，将此键加入字典，并将它的值设为给定值。
"""


def duration_counts(call_list):
    result_list = []
    call_dict = {}
    max_time = 0

    for call in call_list:
        if call[0] in call_dict:
            call_dict[call[0]] += int(call[3])
        else:
            call_dict[call[0]] = int(call[3])

        if call[1] in call_dict:
            call_dict[call[1]] += int(call[3])
        else:
            call_dict[call[1]] = int(call[3])

    for phone_number in call_dict:
        if call_dict[phone_number] > max_time:
            max_time = call_dict[phone_number]
            result_list.clear()
            result_list.append(phone_number)
        elif call_dict[phone_number] == max_time:
            result_list.append(phone_number)

    result_list.append(max_time)

    return result_list


desc_str = "{} spent the longest time, {} seconds, on the phone during September 2016."
results = duration_counts(calls)
if results != None:
    phone_str = ""
    for i in range(len(results) - 1):
        if i == 0:
            phone_str += results[i]
        else:
            phone_str += ", " + results[i]
    print(desc_str.format(phone_str, results[-1]))
