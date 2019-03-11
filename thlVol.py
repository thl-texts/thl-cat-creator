#! /usr/bin/env python

import html

from thlBase import ThlBase

class ThlVol(ThlBase):

    def __init__(self, row, catsig='km', edsig='t'):
        tnum, title, vnum, vlet, vlet2, vseq, pgs, stpg, enpg, doxcat = row
        self.catsig = catsig
        self.edsig = edsig
        self.type = 'vol'
        self.vnum = vnum
        self.vlet = vlet
        self.vlet2 = vlet2
        self.texts = []
        self.doxcats = []
        self.setxml()
        self.settitle()
        self.setnum()

    def settitle(self, title=None):
        if title is None:
            title = "Volume {}".format(self.vnum)
        tel = self.findel('/div/bibl/title[@type="main"]/title[1]')
        tel.text = title

    def setnum(self, num=None):
        if num is None:
            num = int(self.vnum)
        vnel = self.findel('/div/bibl/num[@type="volume"]')
        vnel.text = str(num)

    def add_text(self, atext):
        self.texts.append(atext)
        if atext.doxcat:
            self.doxcats.append(atext.doxcat)

    def get_current_text(self):
        if len(self.texts) > 0:
            return self.texts[-1]

    # When all the texts are added fill in the information
    def finalize(self):
        self.root.set('id', "{}-{}-v{}".format(self.catsig, self.edsig, str(self.vnum).zfill(3)))
        stnm = str(self.texts[0].tnum).zfill(4)
        endnm = str(self.texts[-1].tnum).zfill(4)
        extent = self.findel('/div/bibl/extent[@class="text"]')
        extent[0].set('value', stnm)
        extent[0].text = stnm
        extent[1].set('value', endnm)
        extent[1].text = endnm

        for txt in self.texts:
            self.root.append(txt.root)


if __name__ == "__main__":
    myrow = ['T', '2', u'སྐྱབས་འགྲོ་ཡན་ལག་དྲུག་པ་སློབ་དཔོན་ཆེན་པོ་དྲི་མེད་བཤེས་གཉེན་གྱིས་མཛད་པ་ ', '3', 'a', '1', '1.1', '4.5', 'somdoxcat']
    volme = ThlVol(myrow)


