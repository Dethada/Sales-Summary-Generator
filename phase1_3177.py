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
else:
    print(datetime.datetime.now().strftime("%A %b %d %X"))
    parsedContent = []
    line = f.readline()
    while line:
        tmp = line.split("\t")
        if len(tmp) != 6:
            line = f.readline()
            continue
        parsedContent.append(tmp)
        line = f.readline()
    f.close()
    if not parsedContent:
        print("Invalid data file. Operation aborted.2")
        sys.exit()

    report = Report(parsedContent)
    report.printSummary()
    report.writeRecords()
    print(datetime.datetime.now().strftime("%A %b %d %X"))