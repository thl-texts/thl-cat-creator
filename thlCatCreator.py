#! /usr/bin/env python
"""
The ThlCatCreator class is the main class of the package. It is the controller of all other classes.
The __MAIN__ function here is the code that initiates and does the creation of all docs
Calling on and using the other classes.

This class itself holds the main universal information about the catalog, including who cataloged it and when, the edition
name that is currently being created, the wylie name for the edition, etc.

This routine/class does not create the catalog bibl file itself so information such as the catalog's fullname is not required.
The catalog bibl file needs to be created by hand.

This routine/class will create the catalog toc file, all the volbibls, and all the text bibls.

It contains among other things a list of all its volumes and a list of all its texts
"""
from thlBase import ThlBase
from csvDoc import CsvDoc
from thlVol import ThlVol
from thlDox import ThlDox
from thlText import ThlText
from thlBibl import ThlBibl

class ThlCatCreator(ThlBase):

    def __init__(self, datapath, catsig, edsig, cataloger="", catdate="", edname="", edwyl=""):
        # Cataloging Info
        self.type = 'cat'
        self.catsig = catsig
        self.edsig = edsig
        self.cataloger = cataloger
        self.catdate = catdate
        self.edname = edname
        self.edwyl = edwyl
        self.edtib = self.gettib(edwyl) if edwyl != "" else ""

        # Data Paths and Arrays
        self.datapath = datapath
        self.data = None
        self.voldata = None
        self.voloffset = None
        self.doxtoc = None

        # Lists of Content Items
        self.vols = []
        self.texts = []

        self.setxml()
        self.load_data()
        self.process_data()

    def getfilename(self):
        return "{}-{}-cat.xml".format(self.catsig, self.edsig)

    def getvol(self, vnum):
        for vol in self.vols:
            if vol.getnum == int(vnum):
                return vol
        return None

    def load_data(self, datatype="cat", otherdatapath=None):
        if datatype == "cat":
            # Load the CSV document with the catalog data
            self.data = CsvDoc(self.datapath)
        elif datatype == "vol":
            self.voldata = CsvDoc(otherdatapath)
        elif datatype == "voloffset":
            self.voloffset = CsvDoc(otherdatapath)

    def process_data(self):
        # Process the CSV file into arrays of texts and volumes which also have arrays of texts
        ct = 0
        for row in self.data:
            ct += 1
            print("\rDoing row {}              ".format(ct), end='')
            row = row[0:10]  # trim to 10 columns only
            # Create a THL text object and add it to the list
            self.texts.append(ThlText(row, self.catsig, self.edsig))
            # Check to see if its a new volume
            if len(self.vols) == 0 or self.vols[-1].vnum != self.texts[-1].vnum:
                # If so, create the vol and add it to the vol list
                self.vols.append(ThlVol(row, self.catsig, self.edsig))
            # Add the last text in our text list to the last volume in the volume list
            self.vols[-1].add_text(self.texts[-1])

    def build_cat(self):
        # put all the info together into a single LXML doc
        self.root.set('id', "{}-{}-cat".format(self.catsig, self.edsig)) # need to change the template to have root as TEI.2
        extvols = self.findel('/div/bibl/extent[@class="volumes"]')
        extvols[0].text = self.vols[0].vnum
        extvols[1].text = self.vols[-1].vnum
        exttxt = self.findel('/div/bibl/extent[@class="texts"]')
        exttxt[0].text = self.texts[0].tnum
        exttxt[1].text = self.texts[-1].tnum
        for vol in self.vols:
            vol.finalize()
            self.root.append(vol.root)

    def build_dox_cat(self):
        # build a toc based on doxographical info from volumes
        tsadox = ThlDox("rtsa ba'i chos sde", self.catsig, self.edsig, '1', 'rtsa')
        gyabdox = ThlDox("rgyab chos bstan bcos", self.catsig, self.edsig, '1', 'rgyab')
        for row in self.voldata:
            dox = row[5].strip()
            volnum = row[0].strip()

            if int(volnum) < 42:
                if dox not in tsadox.doxcats:
                    tsadox.doxcats[dox] = [volnum]
                else:
                    tsadox.doxcats[dox].append(volnum)
            elif dox not in gyabdox.doxcats:
                    gyabdox.doxcats[dox] = [volnum]
            else:
                gyabdox.doxcats[dox].append(volnum)

        tsadox.finalize()
        ct = 0
        for dox, vnums in tsadox.doxcats.items():
            ct += 1
            doxcat = ThlDox(dox, self.catsig, self.edsig, '2', ct, 'tib')
            for vn in vnums:
                doxcat.vols.append(self.getvol(vn))
            doxcat.finalize()
            tsadox.root.append(doxcat.root)
        self.root.append(tsadox.root)

        gyabdox.finalize()
        ct = 0
        for dox, vnums in gyabdox.doxcats.items():
            ct += 1
            doxcat = ThlDox(dox, self.catsig, self.edsig, '2', ct, 'tib')
            for vn in vnums:
                doxcat.vols.append(self.getvol(vn))
            doxcat.finalize()
            gyabdox.root.append(doxcat.root)
        self.root.append(gyabdox.root)


    # def write_cat(self, outfile):
    #     # write out the root document, the full XML catalog
    #     with open(outfile, 'w') as outf:
    #         outf.write(self.printme())


    def write_volsum(self, outfile):
        # Writes a summary of volume information gleaned from the catalog into a csv doc named outfile.csv
        with open(outfile, 'w') as outf:
            for vol in self.vols:
                row = '"{}","{}","{}","{}","{}"'.format(vol.vnum, vol.title, len(vol.texts), vol.texts[0].tnum, vol.texts[-1].tnum) + "\n"
                outf.write(row)

    def get_errors(self):
        # Retrieved the errors from each text and prints them out together
        errs = {}
        for txt in self.texts:
            for err in txt.errors:
                if err not in errs:
                    errs[err] = [txt.tnum]
                else:
                    errs[err].append(txt.tnum)

        print("\n\n")
        for errnm, tlist in errs.items():
            if isinstance(tlist, list) and len(tlist) > 0:
                print("{} texts with {}: \n{}\n\n".format(len(tlist), errnm, ', '.join(tlist)))


    def write_cat_files(self, catoutdir, voldir, textdir, writecatfile=True):
        # Write all catalog files: the catalog xml, the vol bibs, the text bibs, and prints out errors
        """
        :param catoutdir:
        :param voldir:
        :param textdir:
        :param writecatfile:  A Boolean that determines whether to write vol and cat files.

        :return:
        """

        if catoutdir[-1] != "/":
            catoutdir += "/"
        catoutnm = catoutdir + self.getfilename()
        voldir = catoutdir + voldir + '/'
        textdir = catoutdir + textdir + '/'
        if writecatfile:
            self.write_cat(catoutnm)
            self.write_vol_bibls(voldir)
        self.write_text_bibls(textdir)
        self.get_errors()
        print("\n{} texts and {} vols".format(len(self.texts), len(self.vols)))

    def write_vol_bibls(self, outdir):
        for v in self.vols:
            vbib = ThlBibl('vol-bibl', self.catsig, self.edsig, v.vnum)
            vbib.set_resp(self.cataloger, self.catdate)
            vbib.set_tibid(self.edname, self.edwyl, self.formatsig(self.edsig, 'print'),
                           v.vnum, v.vlet, v.vlet2)
            vdr = self.voldata.findrow(0, str(v.vnum))
            doxcat = str(vdr[5]) if vdr is not None else ""
            vosr = self.voloffset.findrow(0, str(v.vnum))
            presides = str(vosr[3]) if vosr is not None else ""
            v.writebib(vbib, doxcat, presides, outdir)

    def write_text_bibls(self, outdir):
        for t in self.texts:
            print("Writing text: {}".format(t.tnum))
            tbib = ThlBibl('txt-bibl', self.catsig, self.edsig, t.tnum)
            tbib.set_resp(self.cataloger, self.catdate)
            tbib.set_tibid(self.edname, self.edwyl, self.formatsig(self.edsig, 'print'),
                           t.vnum, t.vlet, t.vlet2, t.tnum, t.vseq)
            t.writebib(tbib, outdir)


if __name__ == '__main__':
    # Create cat object by loading csv and assigning variables
    datafile = '../data/km-t-vol1-2.csv'
    write_the_cat = False  # Whether to write the catalog ...-cat.xml file

    # Create the catalog objects
    mycat = ThlCatCreator(datafile, 'km', 't',
                          'Naomi Worth', '2017-03-22',
                          "Tse ring rgya mtsho", "tse ring rgya mtsho ")
    # Load extra vol data
    mycat.load_data('vol', '../data/km-vol-data-naomi.csv')
    mycat.load_data('voloffset', '../data/km-vol-offset.csv')

    # print out the files
    # mycat.write_cat_files('../out/', 'volbibs', 'textbibs', write_the_cat)

    mycat.build_dox_cat()
    mycat.writeme('../out/km-t-dox-toc.xml')

