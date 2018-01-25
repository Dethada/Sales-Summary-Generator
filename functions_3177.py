from os import path, makedirs
from shutil import rmtree
from heapq import nlargest, nsmallest
'''
Author: David Zhu (P1703177)
Class: DISM/FT/1A/21
'''

class InvalidFormat(Exception):
    def __init__(self, code):
        self.code = code
    def __str__(self):
        return repr(self.code)

''' takes in a single split line returns the sales value of the line
returns none if no valid float value is found or line format is wrong'''
def lineValidation(splitline):
    if len(splitline) != 6: # skip line if it has invalid format
        raise InvalidFormat(1)
    try:
        return float(splitline[4])
    except ValueError: # skip line if it has invalid data
        raise InvalidFormat(2)

'''reference: https://stackoverflow.com/questions/273192/how-can-i-create-a-directory-if-it-does-not-exist
https://stackoverflow.com/questions/6996603/how-to-delete-a-file-or-folder
Takes in file pointer as parameter
Writes indivial city purchase records out to disk'''
def writeRecords(fp):
    cityFiles = {}
    folder = 'reports'
    if path.exists(folder):
        rmtree(folder) # empty and remove directory if directory already exisits
    makedirs(folder) # create reports directory
    for line in fp:
        tmp = line.split("\t")
        try:
            lineValidation(tmp) # skip line if it has invalid format
        except InvalidFormat:
            continue
        try:
            cityFiles.get(tmp[2]).write(line)
        except AttributeError:
            cityfp = open('{}/{}.txt'.format(folder, tmp[2]), 'w')
            cityfp.write(line)
            cityFiles[tmp[2]] = cityfp
    for f in cityFiles.values(): # close file pointers
        f.close()
    print('records done')

'''reference: https://www.w3resource.com/python-exercises/dictionary/python-data-type-dictionary-exercise-22.php
takes in a dictonary and n as parameter where n is number of top values
returns top n keys with values from dict'''
def getTop(dictionary, n):
    top = nlargest(n, dictionary, key=dictionary.get) # get n keys with highest values
    for i in range(n):
        top[i] = '{:<23}{:23.2f}'.format(top[i], dictionary[top[i]])
    return top

''' takes in a dictonary and n as parameter where n is number of lowest values
returns bottom n keys with values from dict '''
def getBottom(dictionary, n):
    btm = nsmallest(n, dictionary, key=dictionary.get) # get n keys with lowest values
    btm.reverse()
    for i in range(n):
        btm[i] = '{:<23}{:23.2f}'.format(btm[i], dictionary[btm[i]])
    return btm

''' takes in citySales, category sales and total sales amt as parameters
prints out the sales summary for all cities and categories '''
def printSummary(citySales, catSales, totalSale):
    noCities = len(citySales)
    noCats = len(catSales)
    if noCities == 0 or noCats == 0:
        print("Invalid data file. Operation aborted.")
        return
    avgCitySale = totalSale / noCities
    avgCatSale = totalSale / noCats
    divider = '=' * 46
    print("Total Sales of the year is {:.2f}\n".format(totalSale))
    print("The Average Sales From {} Cities:\n{:46.2f}\n".format(noCities, avgCitySale))
    if noCities > 3:
        print("Top Three Cities\n{}".format(divider))
        for city in getTop(citySales, 3):
            print(city)
        print("{0}\n\nBottom Three Cities\n{0}".format(divider))
        for city in getBottom(citySales, 3):
            print(city)
    else: # different format for 3 or less cities
        print("Sales Figures by Cities\n{}".format(divider))
        for city in getTop(citySales, noCities):
            print(city)
    print("{}\n\nThe Average Sales From {} Item Categories:\n{:46.2f}\n".format(divider, noCats, avgCatSale))
    if noCats > 3:
        print("Top Three Item Categories\n{}".format(divider))
        for cat in getTop(catSales, 3):
            print(cat)
        print("{0}\n\nBottom Three Item Categories\n{0}".format(divider))
        for cat in getBottom(catSales, 3):
            print(cat)
    else: # different format for 3 or less categories
        print("Sales Figures by Item Categories\n{}".format(divider))
        for cat in getTop(catSales, noCats):
            print(cat)
    print('{}\n'.format(divider))

''' takes in a filepointer as parameter
prints summary of the purchases records'''
def getSummary(fp):
    citySales, catSales = {}, {}
    totalSale = 0
    for line in fp:
        splitline = line.split("\t")
        try:
            salesAmt = lineValidation(splitline)
        except InvalidFormat:
            continue
        totalSale += salesAmt # calculate total sales amount
        city, cat = splitline[2], splitline[3]
        try:
            citySales[city] += salesAmt # calculate city sales amount
        except KeyError:
            citySales[city] = salesAmt # add city to dictionary
        try:
            catSales[cat] += salesAmt # calculate category sales amount
        except KeyError:
            catSales[cat] = salesAmt # add category to dictionary
    printSummary(citySales, catSales, totalSale)
