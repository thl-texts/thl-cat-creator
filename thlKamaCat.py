#! /usr/bin/env python

from thlBase import ThlBase
from csvDoc import CsvDoc

class ThlKamaCat(ThlBase):

    def __init__(self, path, sigla, vols, texts):

        self.type = 'cat'
        self.path = path
        self.sigla = sigla
        self.volnum = vols
        self.textnum = texts
        self.data = None
        self.tree = self.load_template('cat')
        if self.tree:
            self.root = self.tree.getroot()

    def load_data(self, csvpath):
        self.data = CsvDoc(csvpath)

    def process_data(self):
        pass


if __name__ == '__main__':
    mycat = ThlKamaCat('./test-cat-out.xml', 'tc', 4, 45)
    print(mycat.root)
    csvp = "../../testdoc.csv"
    mycat.load_data(csvp)

    tib = u'སྒྲོལ་མ་མཎྜལ་བཞི་པའི་ཆོ་ག་ཀླུ་དབང་དགོངས་རྒྱན་རིག་འཛིན་འཇིགས་མེད་གླིང་པ'
    wyl = ThlKamaCat.getwylie(tib)
    print(wyl)
