#!/usr/bin/python3
import datetime, sys, os, shutil
from heapq import nlargest, nsmallest
'''
0 for date
1 for time
2 for city
3 for category
4 for sales
5 for payment
16s execution time
'''
class Report():
    def __init__(self, data):
        self.data = data
        self.cities = set()
        self.categories = set()
        for i in self.data:
            if i[2] not in self.cities:
                self.cities.add(i[2]) # get all cities
            if i[3] not in self.categories:
                self.categories.add(i[3]) # get all categories
        self.citySales = {}
        self.catSales = {}
        for city in self.cities:
            self.citySales[city] = 0 # initalize citySales dict
        for cat in self.categories:
            self.catSales[cat] = 0 # initalize catSales dict
        for line in self.data:
            self.citySales[line[2]] += float(line[4]) # add sales value to city dict
            self.catSales[line[3]] += float(line[4]) # add sales value to cat dict

    """reference: https://stackoverflow.com/questions/273192/how-can-i-create-a-directory-if-it-does-not-exist
    https://stackoverflow.com/questions/6996603/how-to-delete-a-file-or-folder"""
    def writeReports(self):
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

    def getTotalSale(self):
        total = 0
        for i in self.data:
            total += float(i[4])
        return total

    '''reference: https://www.w3resource.com/python-exercises/dictionary/python-data-type-dictionary-exercise-22.php'''
    def getTopCities(self):
        topThree = nlargest(3, self.citySales, key=self.citySales.get)
        for i in range(3):
            topThree[i] = '{:<23}{:23.2f}'.format(topThree[i], self.citySales[topThree[i]])
        return topThree

    def getBottomCities(self):
        btmThree = nsmallest(3, self.citySales, key=self.citySales.get)
        btmThree.reverse()
        for i in range(3):
            btmThree[i] = '{:<23}{:23.2f}'.format(btmThree[i], self.citySales[btmThree[i]])
        return btmThree

    def getTopCats(self):
        topThree = nlargest(3, self.catSales, key=self.catSales.get)
        for i in range(3):
            topThree[i] = '{:<23}{:23.2f}'.format(topThree[i], self.catSales[topThree[i]])
        return topThree

    def getBottomCats(self):
        btmThree = nsmallest(3, self.catSales, key=self.catSales.get)
        btmThree.reverse()
        for i in range(3):
            btmThree[i] = '{:<23}{:23.2f}'.format(btmThree[i], self.catSales[btmThree[i]])
        return btmThree

    def summary(self):
        totalSale = self.getTotalSale()
        noCities = len(self.cities)
        avgCitySale = totalSale / noCities
        noCats = len(self.categories)
        avgCatSale = totalSale / noCats
        print("Total Sales of the year is {:.2f}\n".format(totalSale))
        print("The Average Sales From {} Cities:\n{:46.2f}\n".format(noCities, avgCitySale))
        print("Top Three Cities\n{}".format('=' * 46))
        for i in self.getTopCities():
            print(i)
        print('=' * 46 + '\n')
        print("Bottom Three Cities\n{}".format('=' * 46))
        for i in self.getBottomCities():
            print(i)
        print('=' * 46 + '\n')
        print("The Average Sales From {} Item Categories:\n{:46.2f}\n".format(noCats, avgCatSale))
        print("Top Three Item Categories\n{}".format('=' * 46))
        for i in self.getTopCats():
            print(i)
        print('=' * 46 + '\n')
        print("Bottom Three Item Categories\n{}".format('=' * 46))
        for i in self.getBottomCats():
            print(i)
        print('=' * 46 + '\n')

if __name__== "__main__":
    if len(sys.argv) != 2:
        print('Usage: {} <sales data file>'.format(sys.argv[0]))
        sys.exit()
    fileName = sys.argv[1]
    try:
        with open(fileName, 'r') as f:
            content = f.readlines()
    except FileNotFoundError:
        print("Invalid data file. Operation aborted.")
        sys.exit()
    else:
        print(datetime.datetime.now().strftime("%A %b %d %X"))
        parsedContent = [x.split("\t") for x in content]

    report = Report(parsedContent)
    report.summary()
    report.writeReports()
    print(datetime.datetime.now().strftime("%A %b %d %X"))