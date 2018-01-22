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
任务1：
短信和通话记录中一共有多少电话号码？每个号码只统计一次。
输出信息：
"There are <count> different telephone numbers in the records."
"""
phone_num_count = set()

for line in texts:
    phone_num_count.add(line[0])
    phone_num_count.add(line[1])

for line in calls:
    phone_num_count.add(line[0])
    phone_num_count.add(line[1])

print("There are {} different telephone numbers in the records.".format(len(phone_num_count)))
