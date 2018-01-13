#!/usr/bin/python3
import datetime, sys
from Report_3177 import *
'''
Author: David Zhu (P1703177)
Class: DISM/FT/1A/21
0 for date
1 for time
2 for city
3 for category
4 for sales
5 for payment
16s execution time
'''

if len(sys.argv) != 2:
    print('Usage: {} <sales data file>'.format(sys.argv[0]))
    sys.exit()
try:
    f = open(sys.argv[1], 'r')
except FileNotFoundError:
    print("Invalid data file. Operation aborted.")
    sys.exit()
else:
    print(datetime.datetime.now().strftime("%A %b %d %X"))
    content = f.readlines()
    f.close()
    parsedContent = [line.split("\t") for line in content]

report = Report(parsedContent)
report.printSummary()
report.writeRecords()
print(datetime.datetime.now().strftime("%A %b %d %X"))