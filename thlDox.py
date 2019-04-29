#! /usr/bin/env python

"""
The ThlDox class is the controller for a single catalog doxographical category.
"""
import html

from thlBase import ThlBase

class ThlDox(ThlBase):

    def __init__(self, title, catsig='km', edsig='t', level='1', id='#', type='wyl'):
        self.catsig = catsig
        self.edsig = edsig
        self.type = 'dox'
        if type is 'tib':
            self.title = title
            self.wytitle = self.getwylie(self.title).replace("---", '\-\-\-').replace('--', '\-\-')
        else:
            self.wytitle = title
            self.title = self.gettib(self.wytitle)
        self.level = level
        self.id = id
        self.doxcats = {}
        self.vols = []
        self.setxml()


    def finalize(self):
        self.root.set('id', "{}-{}-{}".format(self.catsig, self.edsig, self.id))
        self.root.set('n', self.level)
        self.settxt('//bibl[@n="dox"]/title[@type="main"]/title[@lang="tib" and not(@rend="wyl")]', self.title)
        self.settxt('//bibl[@n="dox"]/title[@type="main"]/title[@lang="tib" and @rend="wyl"]', self.wytitle)
        for vol in self.vols:
            if vol is not None:
                for txt in vol.texts:
                    self.root.append(txt.root)
