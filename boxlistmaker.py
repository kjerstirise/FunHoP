#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Linja rett over er her bare for å la oss skrive æøå i python-fila

import xml.etree.ElementTree as ET
import glob
import os

def boxlistmaker(innfil, aleneliste, duplikatliste):
	tree = ET.parse(innfil)
	root = tree.getroot()
	out = []

	for child in root:
		if (child.attrib["type"] == "gene"):
			navn = child.attrib["name"]
			antall = navn.split()
			if len(antall) > 1:
				for underchild in child:
					check = underchild.attrib["name"]
					test = check.split(" ")
					print(test)

					length = len(test)
					print length
					newnamefront = test[0].replace(',', '').replace(';', '')
					newnameback = 'B' + str(length)
					newname = newnamefront + '-' + newnameback
					print (newname)
					if newname not in aleneliste:
						aleneliste.append(newname)
					else: 
						duplikatliste.append(newname)






def main():
	mappesti = '/Users/Kjersti/phd/kode/'
	innfil = 'fikset_hsa00340_jan17.xml'

	duplikatliste = []
	aleneliste = []

	testfil = os.path.join(mappesti, innfil)

	boxlistmaker(testfil, aleneliste, duplikatliste)

	print(aleneliste)
	print(duplikatliste)

if __name__ == '__main__':
	main()