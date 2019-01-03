#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import xml.etree.ElementTree as ET
import copy
import glob
import pandas as pd
import os

"""
This code deals with loose metabolites. These metabolites means more work when looking at a pathway file for the first time, 
as the user must remove them manually. Along with fix_coordinates, this code is made purely to make the experience better when looking at 
the networks. Consists of two functions: find_unconnected_metabolites and removed_unconnected_metabolites. 

"""

def find_unconnected_metabolites(root):
	#First, identify all children of type compound
	
	all_compounds = []
	print(root.attrib["title"])
	for child in root:
		
		if (child.attrib["type"] == "compound"):
			all_compounds.append(child.attrib["id"])

	x = list(set(all_compounds))
	#print(len(x))
	#print(x)

	#Second, identify all compounds found among the relations. 
	#These will be the compounds that are connected to the pathway
	
	all_connected_metabolites = []

	for child in root:
		if (child.attrib["type"] == "reversible") or (child.attrib["type"] == "irreversible"):
			#all_connected_metabolites.append(child.attrib["id"])
			for underchild in child:
				all_connected_metabolites.append(underchild.attrib["id"])


	y = list(set(all_connected_metabolites))
	#print(len(y))
	#print(y)
	
	#return(all_connected_metabolites)
	
	#Third, compare the two lists, to find the compounds that are found in both. 
	#This step could have been skipped, as the all_connected_metabolites would have been enough, 
	#but was kept for verification. 
	connected = []

	for compound in all_compounds:
		if compound in all_connected_metabolites:
			connected.append(compound)

	
	#print(len(connected))
	#print(connected)
	return(connected)



def remove_unconnected_metabolites(root, connected_metabolites):
	#Using the list of compounds that are connected, the compounds that does not have any connections are removed. 
	#Recursion is used to make sure the entire xmls are checked. 
	number_of_unconnected = 0
	for child in root:
		if (child.attrib["type"] == "compound") and (child.attrib["id"] not in connected_metabolites):
			number_of_unconnected += 1
			root.remove(child)
			if (number_of_unconnected > 0):
				remove_unconnected_metabolites(root, connected_metabolites)



def remove_loose_metabolites(pathway_path, outfile_path):
	#tree = ET.parse('/Users/profile/Documents/GitHub/cell-lines/changed_name/testmappe/changed_name_hsa00564.xml')
	#g = glob.glob('/Users/profile/Documents/GitHub/cell-lines/changed_name/*.xml')
	g = glob.glob(os.path.join(pathway_path,'*.xml'))
	
	for file in g:
		print(file)
		filename = file.split("/")
		out_file_name = outfile_path + "removed_lose_" + filename[8]
		
		tree = ET.parse(file)
		root = tree.getroot()
		connected_metabolites = find_unconnected_metabolites(root)
		remove_unconnected_metabolites(root, connected_metabolites)
		tree.write(out_file_name)
		



if __name__ == '__main__':
	remove_loose_metabolites(pathway_path, outfile_path)
