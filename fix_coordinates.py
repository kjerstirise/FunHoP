#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import xml.etree.ElementTree as ET
import copy
import glob
import pandas as pd
import os
"""
This code tries to improve the outputfiles, making it easier for the user to view and work with the files with extended 
nodes in Cytoscape. Fix_y changes the coordinates of all nodes below a node that is extended, making the number of overlapping 
nodes smaller. 

"""

def fix_coords(root):

	nodes = []

	#Extract the genes and compounds 
	for child in root:
		for underchild in child:
			if (child.attrib["type"] == "gene") or (child.attrib["type"] == "compound"):
				namestring = underchild.attrib["name"]
				if "," in namestring:
					length = 1
				else:
					split_namestring = namestring.split(" ")
					length = len(split_namestring)
				nodes.append((int(child.attrib["id"]), int(length), int(underchild.attrib["y"])))

	# Change to Pandas Dataframe to sort the whole thing
	nodes_df = pd.DataFrame(nodes)
	nodes_df.columns = ["ID", "length", "y"]
	nodes_df.sort_values(by = ['y'], ascending = True, inplace = True)
	nodes_df = nodes_df.apply(pd.to_numeric, errors = 'ignore')

	# Back to list mode
	nodes_list = nodes_df.values.tolist()
	
	# Discover the y-coordinates 
	y = 0
	counter = 0
	for row in nodes_list:
		#print(row)
		counter = counter + 1
		if row[2] > y:
			y = row[2]

		# Find the number of genes
		gene_count = row[1]
		if gene_count > 1:
			value = gene_count * 17
			#print(type(value))

			for i in range(counter, len(nodes_list)):	
				#print(nodes_list[i])
				nodes_list[i][2] = nodes_list[i][2] + value

	# Find and replace y-coordinates
	new_y = {}
	for line in nodes_list:
		new_y[line[0]] = line[2]

	#print(new_y) 
	
	for child in root:
		if (child.attrib["type"] == "gene") or (child.attrib["type"] == "compound"):
			id_child = child.attrib["id"]
			for underchild in child:
				new_y_insert = new_y[int(id_child)]
				underchild.attrib["y"] = str(new_y_insert)

						

def fix_coordinates(pathway_path, outfile_path):
	#g = glob.glob('/Users/profile/Documents/GitHub/cell-lines/changed_name_and_removed/*.xml')
	g = glob.glob(os.path.join(pathway_path,'*.xml'))

	for file in g:
		filename = file.split("/")
		out_file_name = outfile_path + "fixed_coords_" + filename[8] 
		tree = ET.parse(file)
		root = tree.getroot()
		fix_coords(root)
		tree.write(out_file_name)



if __name__ == '__main__':
	fix_coordinates(pathway_path, outfile_path)


