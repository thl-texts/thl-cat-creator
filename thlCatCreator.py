#! /usr/bin/env python

from thlBase import ThlBase
from csvDoc import CsvDoc
from thlVol import ThlVol
from thlText import ThlText

class ThlCatCreator(ThlBase):

    def __init__(self, datapath, catsig, edsig):
        self.type = 'cat'
        self.datapath = datapath
        self.catsig = catsig
        self.edsig = edsig
        self.vols = []
        self.texts = []
        self.data = None
        self.setxml()
        self.load_data()
        self.process_data()

    def load_data(self):
        # Load the CSV document with the catalog data
        self.data = CsvDoc(self.datapath)

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

    def write_cat(self, outfile):
        # write out the root document, the full XML catalog
        with open(outfile, 'w') as outf:
            outf.write(self.printme())

    def write_volsum(self, outfile):
        with open(outfile, 'w') as outf:
            for vol in self.vols:
                row = '"{}","{}","{}","{}","{}"'.format(vol.vnum, vol.title, len(vol.texts), vol.texts[0].tnum, vol.texts[-1].tnum) + "\n"
                outf.write(row)

    def get_errors(self):
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


    def write_cat_files(self, catoutnm, voloutnm):
        self.build_cat()
        self.write_cat(catoutnm)
        self.write_volsum(voloutnm)
        self.get_errors()
        print("\n{} texts and {} vols".format(len(self.texts), len(self.vols)))

    def write_vol_bibls(self, outdir):
        for v in self.vols:
            vxml = self.load_template('vol-bibl')



if __name__ == '__main__':
    mycat = ThlCatCreator('../data/testcatdata.csv', 'km', 't')
    # mycat.write_cat_files('../out/km-t-cat.xml', '../data/km-t-volsum-test.csv')

