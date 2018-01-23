#!/usr/bin/python3
from sys import argv
from datetime import datetime
from multiprocessing import Process
from functions_3177 import getSummary, writeRecords
'''
Author: David Zhu (P1703177)
Class: DISM/FT/1A/21
'''

def main():
    if len(argv) != 2:
        print('Usage: {} <sales data file>'.format(argv[0]))
        return
    try:
        fp1 = open(argv[1], 'r')
        fp2 = open(argv[1], 'r')
    except FileNotFoundError:
        print("Invalid data file. Operation aborted.")
        return
    else:
        print(datetime.now().strftime("%a %b %d %X"))
        p1 = Process(target=writeRecords, args=(fp1,))
        p2 = Process(target=getSummary, args=(fp2,))
        # Start processes
        p1.start()
        p2.start()
        # Wait for processes to finish
        p1.join()
        p2.join()
        # Close file pointers
        fp1.close()
        fp2.close()
        print(datetime.now().strftime("%a %b %d %X"))

if __name__ == '__main__':
    main()
