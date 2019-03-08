#! /usr/bin/env python

import html

from thlBase import ThlBase

class ThlKamaText(ThlBase):

    def __init__(self, row, catsig='km'):
        sigla, tnum, title, vnum, vlet, vseq, stpg, enpg, doxcat = row
        self.catsig = catsig
        self.type = 'txt'
        self.sigla = sigla
        self.tnum = tnum
        self.title = title.strip()
        self.wytitle = self.getwylie(self.title)
        self.vnum = vnum
        self.vlet = vlet
        self.vseq = vseq
        self.stpg = stpg
        self.enpg = enpg
        self.doxcat = doxcat
        self.setxml()

    def getid(self, type='default'):
        if type == 'full':
            return "{}-{}-{}".format(self.catsig.lower(), self.sigla.lower(), self.tnum)
        else:
            return "{}.{}".format(self.sigla, self.tnum)

    def create_record(self):
        self.root.set('id', self.getid('full'))
        titlel = self.findel('/div/bibl/title[@type="main"]')
        if titlel is not None:
            titlel[0].text = self.title
            titlel[1].text = self.wytitle

        self.settxt('/div/bibl/idno[@type="vol"]', self.vnum.zfill(3))
        self.settxt('/div/bibl/idno[@type="text"]', self.tnum.zfill(4))
        self.settxt('//rs[@type="pagination" and @n="start"]/num[@type="page"]', self.stpg)
        self.settxt('//rs[@type="pagination" and @n="end"]/num[@type="page"]', self.enpg)


if __name__ == "__main__":
    print("here")
    myrow = ['T', '2', u'སྐྱབས་འགྲོ་ཡན་ལག་དྲུག་པ་སློབ་དཔོན་ཆེན་པོ་དྲི་མེད་བཤེས་གཉེན་གྱིས་མཛད་པ་ ', '3', 'a', '1', '1.1', '4.5', 'somdoxcat']
    mytext = ThlKamaText(myrow)
    mytext.create_record()
    print(mytext.printme())

