#!/usr/bin/python3
import datetime, sys, os, shutil
from heapq import nlargest, nsmallest
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

''' Stores data reguarding the purchase records '''
class Report():
    ''' takes in list of parsed purchase records as param 
    initalizes the Report object '''
    def __init__(self, data):
        self.data = data
        self.cities = set()
        self.categories = set()
        self.citySales = {}
        self.catSales = {}
        self.totalSale = 0
        for line in self.data:
            self.totalSale += float(line[4])
            if line[2] not in self.cities:
                self.cities.add(line[2]) # get all cities
            if line[3] not in self.categories:
                self.categories.add(line[3]) # get all categories
        for city in self.cities:
            self.citySales[city] = 0 # initalize citySales dict
        for cat in self.categories:
            self.catSales[cat] = 0 # initalize catSales dict
        for line in self.data:
            self.citySales[line[2]] += float(line[4]) # add sales value to city dict
            self.catSales[line[3]] += float(line[4]) # add sales value to cat dict
        self.noCities = len(self.cities)
        self.avgCitySale = self.totalSale / self.noCities
        self.noCats = len(self.categories)
        self.avgCatSale = self.totalSale / self.noCats

    '''reference: https://stackoverflow.com/questions/273192/how-can-i-create-a-directory-if-it-does-not-exist
    https://stackoverflow.com/questions/6996603/how-to-delete-a-file-or-folder
    Writes indivial city purchase records out to disk'''
    def writeRecords(self):
        if os.path.exists('reports'):
            shutil.rmtree('reports')
        os.makedirs('reports')
        output = {}
        for city in self.cities:
            output[city] = [] # initalize output dict
        for line in self.data:
            output.get(line[2]).append('\t'.join(line)) # add values to output dict
        for city, lines in output.items():
            with open('reports/'+city+'.txt', 'w') as f:
                for line in lines:
                    f.write(line)

    '''reference: https://www.w3resource.com/python-exercises/dictionary/python-data-type-dictionary-exercise-22.php
    returns top three keys with highest values from dict'''
    def getTopThree(self, dictionary):
        topThree = nlargest(3, dictionary, key=dictionary.get)
        for i in range(3):
            topThree[i] = '{:<23}{:23.2f}'.format(topThree[i], dictionary[topThree[i]])
        return topThree

    # returns bottom three keys with highest values from dict
    def getBottomThree(self, dictionary):
        btmThree = nsmallest(3, dictionary, key=dictionary.get)
        btmThree.reverse()
        for i in range(3):
            btmThree[i] = '{:<23}{:23.2f}'.format(btmThree[i], dictionary[btmThree[i]])
        return btmThree

    # prints out the sales summary for all cities and categories
    def printSummary(self):
        print("Total Sales of the year is {:.2f}\n".format(self.totalSale))
        print("The Average Sales From {} Cities:\n{:46.2f}\n".format(self.noCities, self.avgCitySale))
        print("Top Three Cities\n{}".format('=' * 46))
        for city in self.getTopThree(self.citySales):
            print(city)
        print('=' * 46 + '\n')
        print("Bottom Three Cities\n{}".format('=' * 46))
        for city in self.getBottomThree(self.citySales):
            print(city)
        print('=' * 46 + '\n')
        print("The Average Sales From {} Item Categories:\n{:46.2f}\n".format(self.noCats, self.avgCatSale))
        print("Top Three Item Categories\n{}".format('=' * 46))
        for cat in self.getTopThree(self.catSales):
            print(cat)
        print('=' * 46 + '\n')
        print("Bottom Three Item Categories\n{}".format('=' * 46))
        for cat in self.getBottomThree(self.catSales):
            print(cat)
        print('=' * 46 + '\n')

if __name__== "__main__":
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