#! /usr/bin/env python

"""
The ThlVol class is the controller for a single catalog volume. It contains many common properties as well as a list
of texts contained in the volume
"""
import html

from thlBase import ThlBase

class ThlVol(ThlBase):

    def __init__(self, row, catsig='km', edsig='t'):
        tnum, title, vnum, vlet, vlet2, vseq, pgs, stpg, enpg, doxcat = row
        self.catsig = catsig
        self.edsig = edsig
        self.type = 'vol'
        self.title = ''
        self.vnum = vnum
        self.vlet = vlet
        self.vlet2 = vlet2
        self.texts = []
        self.doxcats = []
        self.tibbibl = None
        self.setxml()
        self.settitle()
        self.setnum()

    def getfilename(self):
        return "{}-{}-v{}-bib.xml".format(self.catsig, self.edsig, str(self.vnum).zfill(3))

    def settitle(self, title=None):
        if title is None:
            title = "Volume {}".format(self.vnum)
        tel = self.findel('/div/bibl/title[@type="main"]/title[1]')
        tel.text = title
        self.title = title

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
        self.settext('/div/bibl/extent[@class="texts"]', len(self.texts))
        extent = self.findel('/div/bibl/extent[@class="text"]')
        extent[0].set('value', stnm)
        extent[0].text = stnm
        extent[1].set('value', endnm)
        extent[1].text = endnm

        for txt in self.texts:
            self.root.append(txt.root)

    def writebib(self, vbib, doxcat, presides, outdir):
        vbib.settxt('//titledecl[@n="titlepage"]/title[@type="normalized"]',
                    "Volume {} (<hi rend=\"tib\">{}</hi>)".format(self.vnum, self.vlet))
        vbib.settxt('//divdecl[@type="texts"]/divcount[@class="total"]', len(self.texts))
        vbib.settxt('//extentdecl[@type="text"]/extent[@class="first"]', self.texts[0].tnum)
        vbib.settxt('//extentdecl[@type="text"]/extent[@class="last"]', self.texts[-1].tnum)
        totalpgs = self.texts[-1].enpg
        if "." not in totalpgs:
            totalpgs += ".0"
        vbib.settxt('//extentdecl[@type="sides"]/extent[@class="total"]', int(float(totalpgs)))
        vbib.settxt('/tibbibl/physdecl/pagination/rs[@n="end"]/num', self.texts[-1].enpg)
        vbib.settxt('//intelldecl/doxography[@type="category"]', doxcat)
        vbib.settxt('//extentdecl[@type="sides"]/extent[@class="sides-before-1a"]', presides)

        # Add dox cats from text margins
        margdox = []
        for t in self.texts:
            if t.doxcat is not None and t.doxcat != '':
                margdox.append(t.doxcat)
        margdox = set(margdox)  # get unique values
        intdecl = vbib.findel('//intelldecl')
        for dox in margdox:
            intdecl.append(
                self.create_element('doxography', dox, {"type": "category", "lang": "tib", "subtype": "margin"}))

        vbib.writeme(outdir + vbib.filename)


if __name__ == "__main__":
    myrow = ['51', u'Sometext name', '2', 'kha', 'a', '23', '456', '1', '456', 'somdoxcat']
    volme = ThlVol(myrow)
    tmpel = volme.load_template('vol-bibl', True)
    tibid = tmpel.findel('//tibiddecl/tibid')
    print(volme.xstr(tibid))


