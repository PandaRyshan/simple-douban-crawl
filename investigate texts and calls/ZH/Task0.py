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
任务0:
短信记录的第一条记录是什么？通话记录最后一条记录是什么？
输出信息:
"First record of texts, <incoming number> texts <answering number> at time <time>"
"Last record of calls, <incoming number> calls <answering number> at time <time>, lasting <during> seconds"
"""
text_1 = texts[0]
call_1 = calls[-1]
print("First record of texts, " +
      text_1[0] + " texts " + text_1[1] + " at time " + text_1[2])
print("Last record of calls, {} calls {} at time {}, lasting {} seconds"
      .format(call_1[0], call_1[1], call_1[2], call_1[3]))
