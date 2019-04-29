#! /usr/bin/env python

"""
The ThlText class is the controller for a single text in the catalog
"""
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
        self.wytitle = self.getwylie(self.title).replace("---", '\-\-\-').replace('--', '\-\-')
        self.vnum = vnum
        self.vlet = vlet
        self.vlet2 = vlet2
        self.vseq = vseq
        self.pgs = pgs
        self.stpg = stpg
        self.enpg = enpg
        self.doxcat = doxcat
        self.errors = []
        self.setxml()
        self.finalize()

    def getfilename(self):
        return "{}-bib.xml".format(self.getid("full"))

    def getid(self, type='default'):
        # Get the text id in differen formats
        if type == 'full':
            return "{}-{}-{}".format(self.catsig.lower(), self.edsig.lower(), str(self.tnum).zfill(4))
        else:
            return "{}.{}".format(self.formatsig(self.edsigla, "print"), self.tnum)

    def finalize(self):
        # Fill out the information in the XML object
        # This is for the DIV that is in the table of contents or -cat.xml file

        # Do Id and Titles
        self.root.set('id', self.getid('full'))
        titlel = self.findel('/div/bibl/title[@type="main"]')
        if titlel is not None:
            titlel[0].text = self.title
            titlel[1].text = self.wytitle

        # Do Vol and Text Numbs
        self.settxt('/div/bibl/idno[@type="vol"]', self.vnum.zfill(3))
        self.settxt('/div/bibl/idno[@type="text"]', self.tnum.zfill(4))

        # Do Start Page
        pg, ln = self.page_split(self.stpg)
        self.settxt('//rs[@type="pagination" and @n="start"]/num[@type="page"]', pg)
        self.settxt('//rs[@type="pagination" and @n="start"]/num[@type="line"]', ln)

        # Do End Page
        pg, ln = self.page_split(self.enpg)
        self.settxt('//rs[@type="pagination" and @n="end"]/num[@type="page"]', pg)
        self.settxt('//rs[@type="pagination" and @n="end"]/num[@type="line"]', ln)


    def writebib(self, tbib, outdir):
        # Write the stand-alone TIBBIBL XML record for the text
        # Pagination and pages
        pg, ln = self.page_split(self.stpg)
        tbib.settxt('/tibbibl/physdecl/pagination/rs[@n="start"]/num[@type="page"]', pg)
        tbib.settxt('/tibbibl/physdecl/pagination/rs[@n="start"]/num[@type="line"]', ln)
        pg, ln = self.page_split(self.enpg)
        tbib.settxt('/tibbibl/physdecl/pagination/rs[@n="end"]/num[@type="page"]', pg)
        tbib.settxt('/tibbibl/physdecl/pagination/rs[@n="end"]/num[@type="line"]', ln)
        tbib.settxt('/tibbibl/physdecl/extentdecl[@type="sides"]/extent[@class="total"]', self.pgs)

        # Doxcat
        tbib.settxt('/tibbibl/intelldecl/doxography[@type="category" and @subtype="margin"]', self.doxcat)

        #title
        titel = tbib.findel('/tibbibl/titlegrp/titledecl/title[@lang="tib" and @type="edition-title"]')
        print(self.wytitle)
        comm = self.create_comment(self.wytitle)
        titel.append(comm)
        comm.tail = self.title

        tbib.writeme(outdir + tbib.filename)


if __name__ == "__main__":
    myrow = ['T', '2', u'སྐྱབས་འགྲོ་ཡན་ལག་དྲུག་པ་སློབ་དཔོན་ཆེན་པོ་དྲི་མེད་བཤེས་གཉེན་གྱིས་མཛད་པ་ ', '3', 'a', '1', '1.1', '4.5', 'somdoxcat']
    mytext = ThlText(myrow)
    mytext.finalize()
    print(mytext.printme())

