#!/usr/bin/env python
# -*- coding: utf-8 -*-

import itertools
import pandas as pd
import numpy as np
import xml.etree.ElementTree as ET
import glob 

"""	
The readcounter code is made for extracting the gene names in the pathways, in order to create a list 
of all of the genes. This file also contains functions for working with other files, such as Prensners file 
of genes and read counts. 


"""


def boxGeneLists(filnavn):
	"""
	This is the only function in this entire thing that was actually used in the end (because we didn't really 
		want to use the average of the reads....)
	Anyway! This function takes in the root of an xml-file, and goes through every child and underchild, to 
	find all the genes and boxes, and writes them to files. 
	"""

	# Read XML file
	tree = ET.parse(filnavn)

	# Get root node
	root = tree.getroot()

	genliste = []
	middle = root.attrib['org']
	final = root.attrib["number"]
	start = "----"
	utstreng = start + middle + final
	print(utstreng)
	for child in root:
		if (child.attrib["type"] == "gene"):
			for underchild in child:
				if ("," in underchild.attrib['name']):
					remove = underchild.attrib['name'].split(",")
					remove2 = remove[0].replace(";", "")
					if remove2 not in genliste: 
						genliste.append(remove2)
					
				if (not "," in underchild.attrib["name"]):
					without = underchild.attrib["name"].replace(";", "")
					if without not in genliste:
						genliste.append(without)
				
	
	
	for element in genliste:
		print(element)


	
def main():
	g = glob.glob('/Users/Profile/phd/testmappe/*.xml')
	

	for filnavn in g:
		boxGeneLists(filnavn)
		


if __name__ == '__main__':
	main()

