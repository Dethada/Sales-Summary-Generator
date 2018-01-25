#!/usr/bin/python3
from sys import argv
from datetime import datetime
from functions_3177 import parsePurchases
'''
Author: David Zhu (P1703177)
Class: DISM/FT/1A/21
'''

def main():
    if len(argv) != 2:
        print('Usage: {} <sales data file>'.format(argv[0]))
        return
    try:
        fp = open(argv[1], 'r')
    except FileNotFoundError:
        print("Invalid data file. Operation aborted.")
        return
    else:
        print(datetime.now().strftime("%a %b %d %X"))
        parsePurchases(fp)
        fp.close()
        print(datetime.now().strftime("%a %b %d %X"))

if __name__ == '__main__':
    main()
