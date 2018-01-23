#!/usr/bin/python3
import datetime, sys, os
from shutil import rmtree
from heapq import nlargest, nsmallest
'''
Author: David Zhu (P1703177)
Class: DISM/FT/1A/21
11s execution time
'''

'''reference: https://stackoverflow.com/questions/273192/how-can-i-create-a-directory-if-it-does-not-exist
https://stackoverflow.com/questions/6996603/how-to-delete-a-file-or-folder
Takes in citySales dictionary and original file pointer as parameters
Writes indivial city purchase records out to disk'''
def writeRecords(citySales, ogfp):
    folder = 'reports'
    if os.path.exists(folder):
        rmtree(folder) # empty and remove directory if directory already exisits
    os.makedirs(folder) # create reports directory
    for city in citySales: # create file pointer for all cities
        citySales[city] = open(folder + '/'+city+'.txt', 'w')
    line = ogfp.readline()
    while line:
        tmp = line.split("\t")
        if len(tmp) != 6: # skip line if it has invalid format
            line = ogfp.readline()
            continue
        citySales.get(tmp[2]).write(line) # write line out to respective city file
        line = ogfp.readline()
    for fp in citySales.values(): # close file pointers
        fp.close()

'''reference: https://www.w3resource.com/python-exercises/dictionary/python-data-type-dictionary-exercise-22.php
takes in a dictonary and n as parameter where n is number of top values
returns top three keys with values from dict'''
def getTop(dictionary, n):
    topThree = nlargest(n, dictionary, key=dictionary.get) # get n keys with highest values
    for i in range(n):
        topThree[i] = '{:<23}{:23.2f}'.format(topThree[i], dictionary[topThree[i]])
    return topThree

''' takes in a dictonary and n as parameter where n is number of top values
returns bottom three keys with values from dict '''
def getBottom(dictionary, n):
    btmThree = nsmallest(n, dictionary, key=dictionary.get) # get n keys with lowest values
    btmThree.reverse()
    for i in range(n):
        btmThree[i] = '{:<23}{:23.2f}'.format(btmThree[i], dictionary[btmThree[i]])
    return btmThree

''' 
takes in citySales, category sales and total sales amt as parameters
prints out the sales summary for all cities and categories '''
def printSummary(citySales, catSales, totalSale):
    noCities = len(citySales)
    noCats = len(catSales)
    avgCitySale = totalSale / noCities
    avgCatSale = totalSale / noCats
    print("Total Sales of the year is {:.2f}\n".format(totalSale))
    print("The Average Sales From {} Cities:\n{:46.2f}\n".format(noCities, avgCitySale))
    if noCities > 3:
        print("Top Three Cities\n{}".format('=' * 46))
        for city in getTop(citySales, 3):
            print(city)
        print('=' * 46 + '\n')
        print("Bottom Three Cities\n{}".format('=' * 46))
        for city in getBottom(citySales, 3):
            print(city)
    else:
        print("Sales Figures by Cities\n{}".format('=' * 46))
        for city in getTop(citySales, noCities):
            print(city)
    print('=' * 46 + '\n')
    print("The Average Sales From {} Item Categories:\n{:46.2f}\n".format(noCats, avgCatSale))
    if noCats > 3:
        print("Top Three Item Categories\n{}".format('=' * 46))
        for cat in getTop(catSales, 3):
            print(cat)
        print('=' * 46 + '\n')
        print("Bottom Three Item Categories\n{}".format('=' * 46))
        for cat in getBottom(catSales, 3):
            print(cat)
    else:
        print("Sales Figures by Item Categories\n{}".format('=' * 46))
        for cat in getTop(catSales, noCats):
            print(cat)
    print('=' * 46 + '\n')

def main():
    if len(sys.argv) != 2:
        print('Usage: {} <sales data file>'.format(sys.argv[0]))
        return
    try:
        f = open(sys.argv[1], 'r')
    except FileNotFoundError:
        print("Invalid data file. Operation aborted.")
        return
    else:
        print(datetime.datetime.now().strftime("%a %b %d %X"))
        citySales = {}
        catSales = {}
        totalSale = 0
        line = f.readline()
        while line:
            tmp = line.split("\t")
            if len(tmp) != 6: # skip line if it has invalid format
                line = f.readline()
                continue
            try:
                salesAmt = float(tmp[4])
            except ValueError: # skip line if it has invalid data
                line = f.readline()
                continue
            totalSale += salesAmt # calculate total sales amount
            if tmp[2] not in citySales:
                citySales[tmp[2]] = salesAmt # add city to dictionary
            else:
                citySales[tmp[2]] += salesAmt # calculate city sales amount
            if tmp[3] not in catSales:
                catSales[tmp[3]] = salesAmt # add categories to dictionary
            else:
                catSales[tmp[3]] += salesAmt # calculate city sales amount
            line = f.readline()

        printSummary(citySales, catSales, totalSale)
        f.seek(0, 0) # reset filepointer
        writeRecords(citySales, f)
        f.close()
        print(datetime.datetime.now().strftime("%a %b %d %X"))

if __name__ == '__main__':
    main()
