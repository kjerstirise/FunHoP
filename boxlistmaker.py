#!/usr/bin/env python
# -*- coding: utf-8 -*-


import xml.etree.ElementTree as ET
import glob
import os

vi trenger at denne skjønner hvordan den skal returnere ting

def boxlistmaker(pathway):
	tree = ET.parse(pathway)
	root = tree.getroot()
	out = []

	list_of_singles = []
	list_of_duplicates = []

	for child in root:
		if (child.attrib["type"] == "gene"):
			name = child.attrib["name"]
			split_name = name.split()
			if len(split_name) > 1:
				for underchild in child:
					namestring = underchild.attrib["name"]
					split_namestring = namestring.split(" ")
					print(split_namestring)

					length = len(split_namestring)
					print length
					newnamefront = test[0].replace(',', '').replace(';', '')
					newnameback = 'B' + str(length)
					newname = newnamefront + '-' + newnameback
					print (newname)
					if newname not in list_of_singles:
						list_of_singles.append(newname)
					else: 
						list_of_duplicates.append(newname)






def main():
	mappesti = '/Users/Kjersti/phd/kode/'
	innfil = 'fikset_hsa00340_jan17.xml'

	

	testfil = os.path.join(mappesti, innfil)

	boxlistmaker(testfil, aleneliste, duplikatliste)

	print(aleneliste)
	print(duplikatliste)

if __name__ == '__main__':
	main()

	