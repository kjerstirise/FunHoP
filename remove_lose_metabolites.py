#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import xml.etree.ElementTree as ET
import copy
import glob
import pandas as pd

"""
This code deals with loose metabolites. These metabolites means more work when looking at a pathway file for the first time, 
as the user must remove them manually. Along with fix_coordinates, this code is made purely to make the experience better when looking at 
the networks. Consists of two functions: find_unconnected_metabolites and removed_unconnected_metabolites. 

"""

def find_unconnected_metabolites(root):

	all_compounds = []

	for child in root:
			if (child.attrib["type"] == "compound"):
				all_compounds.append(child.attrib["id"])

	x = list(set(all_compounds))


	all_connected_metabolites = []

	for child in root:
		if (child.attrib["type"] == "reversible") or (child.attrib["type"] == "irreversible"):
			all_connected_metabolites.append(child.attrib["id"])
			for underchild in child:
				all_connected_metabolites.append(underchild.attrib["id"])


	y = list(set(all_connected_metabolites))

	connected = []

	for compound in all_compounds:
		if compund in all_connected_metabolites:
			compound.append(thing)

	return(connected)




def remove_unconnected_metabolites(root, connected_metabolites):
	number_of_unconnected = 0
	for child in root:
		if (child.attrib["type"] == "compound") and (child.attrib["id"] not in connected_metabolites):
			number_of_unconnected += 1
			root.remove(child)
			if (number_of_unconnected > 0):
				remove_unconnected_metabolites(root, connected_metabolites)



def main():
	#tree = ET.parse('/Users/profile/Documents/GitHub/cell-lines/changed_name/testmappe/changed_name_hsa00564.xml')
	tree = ET.parse('/Users/profile/Documents/GitHub/cell-lines/changed_name/testmappe/changed_name_hsa00564.xml')
	root = tree.getroot()
	connected_metabolites = find_unconnected_metabolites(root)
	remove_unconnected_metabolites(root, connected_metabolites)
	tree.write("changed_name_removed_compounds.xml")



if __name__ == '__main__':
	main()
