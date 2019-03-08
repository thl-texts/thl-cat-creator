#! /usr/bin/env python

import os
import csv

class CsvDoc:

    def __init__(self, path, ishead=True):
        ext = path.split('.').pop()
        if os.path.isfile(path) and ext == 'csv':
            self.path = path
            self.heads = list()
            self.data = list()
            self.num = 0
            self.loaddoc(ishead)
        else:
            print("{} is not a valid csv file".format(path))

    def __iter__(self):
        return self

    def __next__(self):
        num = self.num
        if num < len(self):
            self.num += 1
            return self.data[num]
        else:
            raise StopIteration

    def __len__(self):
        return len(self.data)

    def loaddoc(self, ishead):
        with open(self.path, newline='', encoding='utf-8') as csvfile:
            reader = csv.reader(csvfile)
            if ishead:
                self.heads = reader.__next__()
                self.heads[0] = self.heads[0].replace(u'\ufeff', '') # strip zero-width non-breaking space off of first cell
            for row in reader:
                try:
                    if int(row[0]):
                        self.data.append(row)
                except ValueError:
                    pass

    def getheads(self):
        return self.heads

    def gethead(self, index):
        if index < len(self.heads):
            return self.heads[index]
        else:
            return False

    def getrow(self, rown):
        if rown < len(self.data):
            return self.data[rown]
        return False

    def getrowdict(self, rown):
        row = self.getrow(rown)
        rdict = {}
        if row:
            c = -1
            for head in self.heads:
                c += 1
                rdict[head] = row[c]

            return rdict

    def getcell(self, r, c):
        r -= 1
        c -= 1
        row = self.getrow(r)
        if row and c < len(row):
            return row[c]
        return False

    def getcellwithlabel(self, r, c):
        cell = self.getcell(r, c)
        label = self.heads[c - 1] if len(self.heads) >= c else ''
        return {'value': cell, 'label': label}

if __name__ == '__main__':
    fnm = '../Nyingma Kama Digital Edition Catalog.csv'
    catdoc = CsvDoc(fnm)
    row = catdoc.getrowdict(2)
    print(row)