#! /usr/bin/env python

from lxml import etree
from html import unescape as htmlunesc
from urllib import parse as urlparse
from urllib3 import PoolManager

WYCONVURL = u'http://www.thlib.org/cgi-bin/thl/lbow/wylie.pl?plain=true&conversion=uni2wyl&input='

class ThlBase:

    def __init__(self):
        self.type = None
        self.xml = None
        self.root = None

    def setxml(self):
        try:
            xml = self.load_template(self.type)
            self.xml = xml
            self.root = xml.getroot()
        except AttributeError:
            print("Error: None etree set to set_xml function")

    def getid(self):
        pass

    def findel(self, xpath, num=0):
        if self.root is not None:
            res = self.root.xpath(xpath)
            if type(res) == list:
                if num == 'all':
                    return res
                elif num < len(res):
                    return res[num]
        return None

    def settxt(self, xpath, txtval):
        el = self.findel(xpath)
        if el is not None:
            el.text = txtval

    def printme(self):
        return self.xstr(self.root)

    @staticmethod
    def xstr(xmlel):
        xstr = etree.tostring(xmlel)
        xstr = htmlunesc(xstr.decode('unicode_escape'))
        return xstr

    @staticmethod
    def getwylie(tibtxt):
        http = PoolManager()
        url = WYCONVURL + urlparse.quote(tibtxt)
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