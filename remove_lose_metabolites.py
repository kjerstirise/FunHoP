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

	return(connected)




def remove_unconnected_metabolites(root, connected_metabolites):
	number_of_unconnected = 0
	for child in root:
		if (child.attrib["type"] == "compound") and (child.attrib["id"] not in connected_metabolites):
			number_of_unconnected += 1
			root.remove(child)
			if (number_of_unconnected > 0):
				remove_unconnected_metabolites(root, connected_metabolites)




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
	connected_metabolites = remove_lose_metabolites(root)
	remove_unconnected_metabolites(root, connected_metabolites)
	tree.write("changed_name_removed_compounds.xml")



if __name__ == '__main__':
	main()
