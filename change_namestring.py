#!/usr/bin/env python
# -*- coding: utf-8 -*-

import xml.etree.ElementTree as ET
import glob
import os

"""
hsa:x = IDs created by KEGG for all genes in the KEGG database. 

The stringfixer code is the first code file of FunHoP. 
Consists of three functions: string_list, string_changer, and ortholog_remover. 
Alters the namestrings for each child in the XML files to include the names for all the genes that are found within the child. 
This is neccessary in order to create the gene nodes, as the gene name strings only contains the name of the first hsa:x, followed 
by paralog names for other species.  

"""

def string_list(hsalist_path):
	"""
	Opens the list of hsa:x and belonging gene names, and creates a list with hsa:x and only one corresponding name. 
	Requires a downloaded version of all hsa:x IDs from KEGG.
	List is found at: http://rest.kegg.jp/list/hsa
	Returns the finished list of one name for each ID. 

	"""
	names = {}
	with open(hsalist_path, 'r') as searchfile:
		lines = searchfile.readlines()
		for line in lines:
			n = line.replace(";", "")
			t = n.split()
			names[t[0]] = t[1].split(',')[0]

	return names


def string_changer(root, names):
	"""
	Alters the XML files to contain the name for all genes found in a node/child. 
	Takes in the root of the XML and the namelist created by string_list().
	
	"""
	number = []

	for child in root:
		new_string = []
		if (child.attrib["type"] == "gene"):
			check_string = child.attrib["name"]
			if (check_string.startswith("hsa:")):
				namestring = check_string.split()
				if(len(namestring) > 1):
					number.append(len(namestring))
					for underchild in child:
						for name in namestring:
							new_string.append(names[name])
							finished_namestring = " ".join(new_string)
							underchild.attrib['name'] = finished_namestring
						



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


def change_namestring(pathway_path, genelist_path):
	names = string_list(hsalist_path = '/Users/profile/Documents/GitHub/cell-lines/hsalist_july18.txt')
	g = glob.glob(os.path.join(pathway_path,'*.xml'))

	for file in g:
		filename = file.split("/")
		out_file_name = "changed_name_" + filename[7]
		print(filename)
		tree = ET.parse(file)
		root = tree.getroot()
		ortholog_remover(root)
		
		string_changer(root, names)
	
		tree.write(out_file_name)
		

	
	

if __name__ == '__main__':
	change_namestring(pathway_path = '/Users/Profile/Documents/GitHub/cell-lines/pathways')
