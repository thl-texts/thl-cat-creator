#! /usr/bin/env python

"""
The ThlBase class is the base class for all the Python classes in this package
It provides basic XML functionality through LXML and catalog specific functions used by all types,
such as "formatsig", "getwylie", "gettibetan", etc.
"""
from lxml import etree
from html import unescape as htmlunesc
from urllib import parse as urlparse
from urllib3 import PoolManager

WYCONVURL = u'http://www.thlib.org/cgi-bin/thl/lbow/wylie.pl?plain=true&conversion=uni2wyl&input='
TIBCONVURL = u'http://www.thlib.org/cgi-bin/thl/lbow/wylie.pl?plain=true&conversion=wy2uni&input='

class ThlBase:

    def __init__(self):
        self.type = None
        self.xml = None
        self.root = None

    def findel(self, xpath, num=0):
        if self.root is not None:
            res = self.root.xpath(xpath)
            if type(res) == list:
                if num == 'all':
                    return res
                elif num < len(res):
                    return res[num]
        return None

    def getid(self):
        pass

    def getfilename(self):
        pass

    def printme(self):
        return self.xstr(self.root)

    def settxt(self, xpath, txtval):
        txtval = str(txtval)
        el = self.findel(xpath)
        if el is not None:
            el.text = txtval

    def setxml(self):
        try:
            xml = self.load_template(self.type)
            self.xml = xml
            self.root = xml.getroot()
        except AttributeError:
            print("Error: None etree set to set_xml function")

    def writeme(self, outfile):
        xmltxt = self.printme()
        with open(outfile, 'w') as outf:
            outf.write(xmltxt)

    @staticmethod
    def create_comment(txt):
        return etree.Comment(txt)

    @staticmethod
    def create_element(nm, txt, atts={}):
        el = etree.Element(nm)
        el.text = txt
        for n, v in atts.items():
            el.set(n, v)
        return el

    @staticmethod
    def formatsig(sig, style="id"):
        if style == 'print' and len(sig) > 0:
            return sig[0].upper() + sig[1:]
        else:
            return sig

    @staticmethod
    def getwylie(tibtxt):
        http = PoolManager()
        url = WYCONVURL + urlparse.quote(tibtxt)
        req = http.request('GET', url)
        if req.status == 200:
            return req.data.decode('utf-8')
        return False

    @staticmethod
    def gettib(wytxt):
        http = PoolManager()
        url = TIBCONVURL + wytxt.replace(' ', '%20')
        req = http.request('GET', url)
        if req.status == 200:
            return req.data.decode('utf-8')
        return False

    @staticmethod
    def load_template(ttype, return_root=False):
        tpath = './templates/thl-{}.tpl.xml'.format(ttype)
        ttree = False

        try:
            with open(tpath, 'r') as tmpin:
                ttree = etree.parse(tmpin)
        except IOError:
            pass

        if return_root:
            return ttree.getroot()
        else:
            return ttree

    @staticmethod
    def page_split(pgln, is_end=False):
        pgln = str(pgln)
        pg = ""
        ln = ""
        if len(pgln) > 0:
            pts = str(pgln).split(".")
            pg = pts[0]
            if len(pts) > 1:
                ln = pts[1]
            elif is_end:
                ln = "?"
            else:
                ln = "1"
        return pg, ln

    @staticmethod
    def xstr(xmlel):
        xstr = etree.tostring(xmlel)
        xstr = htmlunesc(xstr.decode('unicode_escape'))
        return xstr


if __name__ == '__main__':
    print("in main")
    wyl = "gting skyes"
    tib = ThlBase.gettib(wyl)
    print(tib)