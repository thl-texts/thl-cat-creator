# thl-kama-cat-creator

Python "module" to create an XML catalog in the Tibetan & Himalayan Library format for the _Kama Gyéba_ (_bka' ma rgyas pa_).
The central script `thlKamaCat.py` will take a CSV file of data with one text per line and convert it into:

#. A catalog XML file
#. A collection of volume XML files
#. A collection of text XML files

This was written to deal with the Kama data but with an eye toward ultimate generalization and systematization 
so that it could be applicable to any Tibetan canonical collection, provided the CSV spreadsheet conforms to the
specifications.

- Nathaniel Grove (THL, Shanti, CSC)
