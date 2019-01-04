#!/usr/bin/python
# -*- coding: utf-8 -*-


import xml.etree.ElementTree as ET
import glob
import os

def boxlistmaker(pathway, list_of_singles, list_of_duplicates):
	tree = ET.parse(pathway)
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
					#print(test)

					length = len(test)
					#print(length)
					newnamefront = test[0].replace(',', '').replace(';', '')
					newnameback = 'B' + str(length)
					newname = newnamefront + '-' + newnameback
					#print (newname)
					if newname not in list_of_singles:
						list_of_singles.append(newname)
					else: 
						list_of_duplicates.append(newname)






def boxlistmaker(pathway_path):
	"""
	mappesti = '/Users/profile/Documents/GitHub/cell-lines/changed_name/'
	innfil = 'changed_name_hsa00010.xml'
	

	"""
	duplikatliste = []
	aleneliste = []
	
	g = glob.glob(os.path.join(pathway_path, '*.xml')

	for file in g:
		boxlistmaker(file, aleneliste, duplikatliste)

	#testfil = os.path.join(mappesti, innfil)

	#boxlistmaker(testfil, aleneliste, duplikatliste)
	
	for ting in aleneliste:
		print(ting)
	
	for ting in duplikatliste:
		print(ting)

if __name__ == '__main__':
	boxlistmaker(pathway_path)