#! /usr/bin/env python

import datetime

from thlBase import ThlBase

class ThlBibl(ThlBase):

    def __init__(self, ttype, catsig='km', edsig='t', num=0, inits="ndg"):
        self.id = ''
        self.filename = ''
        self.type = ttype
        self.catsig = catsig
        self.edsig = edsig
        self.num = num
        self.inits = inits
        self.catname = ''
        self.edname = ''
        dt = datetime.datetime.now()
        self.now = dt.strftime("%Y-%m-%d")
        self.errors = []
        self.setxml()
        if int(self.num) > 0:
            self.set_ids()

    def getid(self):
        return self.id

    def set_ids(self):
        if self.num == 0:
            print("Warning: In {} class creating ID string, no id number has be set. Will use 0.".format(self.type))
        myid = "{}-{}".format(self.catsig, self.edsig)
        if self.type == 'vol-bibl':
            myid += "-v{}".format(str(self.num).zfill(3))
        elif self.type == 'txt-bibl':
            myid += "-{}".format(str(self.num).zfill(4))
        self.id = myid
        self.settxt('/tibbibl/controlinfo/sysid', self.id)
        self.filename = myid + '-bib.xml'
        self.root.set('id', self.filename)

    def set_resp(self, cataloger, datecat):
        self.settxt('/tibbibl/controlinfo/date', datecat)
        self.settxt('/tibbibl/controlinfo/respStmt/resp', "Cataloger")
        self.settxt('/tibbibl/controlinfo/respStmt/name', cataloger)
        self.settxt('/tibbibl/controlinfo/revisionDesc/change/date', self.now)
        self.settxt('/tibbibl/controlinfo/revisionDesc/change/respStmt/name', self.inits)

    def set_tibid(self, ednm, edwy, edsig, vnum, vlet):
        tibid = self.findel('//tibiddecl/tibid')
        if tibid is not None:
            tibid.text = self.catsig
            edtibid = tibid[0]
            edtibid.text = ednm

            # Add alt ed id
            edalt = edtibid[0]
            edtib = self.gettib(edwy)
            comm = self.create_comment(edwy)
            edalt.append(comm)
            comm.tail = edtib

            # Do vol info
            edsigel = edtibid[1]
            edsigel.text = edsig
            voltibid = edsigel[0]
            voltibid.text = str(vnum).zfill(2)
            valtid = voltibid[0]
            comm = self.create_comment(vlet)
            valtid.append(comm)
            comm.tail = vlet
        else:
            print("Can't find tibid in template")

    def get_ed_tibid(self):
        el = self.findel('//tibidecl//tibid[@type="edition" and @system="sigla"]')
        return el

    def get_filename(self):
        fnm = self.id + '-bib.xml'

    def finalize(self):
        # use if needed to finalize before exporting to xml
        pass


if __name__ == "__main__":
    outfl = '../out/txt-bibl-text.xml'
    me = ThlBibl('txt-bibl', 'km', 't', 3)
    me.set_resp('kaw', '2017-05-12')
    # me.writeme(outfl)
    tibid = me.findel('//tibiddecl/tibid')
    tibid.text = "hola"
    edtib = tibid[0]
    edtib.text = "halo"
    edalt = edtib[0]
    wyl = "gting skyes"
    tib = me.gettib(wyl)
    comm = me.create_comment(wyl)
    edalt.append(comm)
    comm.tail = tib
    print(me.xstr(tibid))



