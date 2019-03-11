#! /usr/bin/env python

import html

from thlBase import ThlBase

class ThlText(ThlBase):

    def __init__(self, row, catsig='km', edsig='t'):
        tnum, title, vnum, vlet, vlet2, vseq, pgs, stpg, enpg, doxcat = row
        self.catsig = catsig
        self.edsig = edsig
        self.type = 'txt'
        self.tnum = tnum
        self.title = title.strip()
        self.wytitle = self.getwylie(self.title)
        self.vnum = vnum
        self.vlet = vlet
        self.vlet2 = vlet2
        self.vseq = vseq
        self.pgs = pgs
        self.stpg = stpg
        self.enpg = enpg
        self.doxcat = doxcat
        self.setxml()
        self.finalize()

    def getid(self, type='default'):
        # Get the text id in differen formats
        if type == 'full':
            return "{}-{}-{}".format(self.catsig.lower(), self.edsig.lower(), str(self.tnum).zfill(4))
        else:
            return "{}.{}".format(self.edsigla, self.tnum)

    def finalize(self):
        # Fill out the information in the XML object
        self.root.set('id', self.getid('full'))
        titlel = self.findel('/div/bibl/title[@type="main"]')
        if titlel is not None:
            titlel[0].text = self.title
            titlel[1].text = self.wytitle

        self.settxt('/div/bibl/idno[@type="vol"]', self.vnum.zfill(3))
        self.settxt('/div/bibl/idno[@type="text"]', self.tnum.zfill(4))
        pts = self.stpg.split('.')
        self.settxt('//rs[@type="pagination" and @n="start"]/num[@type="page"]', pts[0])
        self.settxt('//rs[@type="pagination" and @n="start"]/num[@type="line"]', pts[1])
        pts = self.enpg.split('.')
        self.settxt('//rs[@type="pagination" and @n="end"]/num[@type="page"]', pts[0])
        self.settxt('//rs[@type="pagination" and @n="end"]/num[@type="line"]', pts[1])


if __name__ == "__main__":
    myrow = ['T', '2', u'སྐྱབས་འགྲོ་ཡན་ལག་དྲུག་པ་སློབ་དཔོན་ཆེན་པོ་དྲི་མེད་བཤེས་གཉེན་གྱིས་མཛད་པ་ ', '3', 'a', '1', '1.1', '4.5', 'somdoxcat']
    mytext = ThlText(myrow)
    mytext.finalize()
    print(mytext.printme())

