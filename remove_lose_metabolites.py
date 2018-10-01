#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import xml.etree.ElementTree as ET
import copy
import glob
import pandas as pd

def remove_lose_metabolites(root):

	all_compounds = []

	for child in root:
			if (child.attrib["type"] == "compound"):
				all_compounds.append(child.attrib["id"])


	
	print(len(all_compounds))
	x = list(set(all_compounds))
	print(len(x))
	all_connected_metabolites = []

	for child in root:
		if (child.attrib["type"] == "reversible") or (child.attrib["type"] == "irreversible"):
			all_connected_metabolites.append(child.attrib["id"])
			for underchild in child:
				all_connected_metabolites.append(underchild.attrib["id"])


	print(len(all_connected_metabolites))
	y = list(set(all_connected_metabolites))
	print(len(y))

	connected = []
	for thing in all_compounds:
		if thing in all_connected_metabolites:
			connected.append(thing)

	print(len(connected))
	print(connected)

	for child in root:
		if (child.attrib["type"] == "compound") and (child.attrib["id"] not in connected):
			root.remove(child)

"""

	def ortholog_remover(root):
	number = 0;
	for child in root:
		if (child.attrib["type"] == "ortholog"):
			number += 1
	for child in root:
		if (child.attrib["type"] == "ortholog"):
			root.remove(child)
	if (number > 0):
		ortholog_remover(root)
"""

def main():
	#tree = ET.parse('/Users/profile/Documents/GitHub/cell-lines/changed_name/testmappe/changed_name_hsa00564.xml')
	tree = ET.parse('/Users/profile/Documents/GitHub/cell-lines/changed_name/testmappe/changed_name_hsa00564.xml')
	root = tree.getroot()
	remove_lose_metabolites(root)
	tree.write("outfile_testfile_compoundremover_564.xml")



if __name__ == '__main__':
	main()
