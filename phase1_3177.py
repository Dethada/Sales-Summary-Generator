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
    with open(sys.argv[1], 'r') as f:
        content = f.readlines()
except FileNotFoundError:
    print("Invalid data file. Operation aborted.")
else:
    parsedContent = parsePurchaseRecords(content)
    if parsedContent == None:
        print("Invalid data file. Operation aborted.")
        sys.exit()

    print(datetime.datetime.now().strftime("%A %b %d %X"))
    report = Report(parsedContent)
    report.printSummary()
    report.writeRecords()
    print(datetime.datetime.now().strftime("%A %b %d %X"))