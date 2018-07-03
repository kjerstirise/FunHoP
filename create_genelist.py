#!/usr/bin/env python
# -*- coding: utf-8 -*-

import itertools
import pandas as pd
import numpy as np
import xml.etree.ElementTree as ET
import glob 

"""	
The create_genlist code is made for extracting the gene names in the pathways, in order to create a list 
of all of the genes. The code takes in the pathway files created by change_namestring, which has the complete namestrings 
for each child. The result from this file is a .txt file with all the namestrings from all the children in all the files, 
indicating which of them will need extended nodes. This file is used to calculate new values for the extended nodes.  


"""



	# Read XML file
	tree = ET.parse(file)

	# Get root node
	root = tree.getroot()

	genlist = []

	# Create divider
	start = "----"
	middle = root.attrib['org']
	final = root.attrib["number"]
	
	divider = start + middle + final

	

	for child in root:
		if (child.attrib["type"] == "gene"):
			for underchild in child:
				# For children with only one gene, removing ; and adding string to list
				if ("," in underchild.attrib['name']):
					only_one_gen_string = underchild.attrib['name'].split(",")
					one_gene = only_one_gen_string[0].replace(";", "")
					if one_gene not in genlist: 
						genlist.append(one_gene)
					
				# For children with multiple genes, removing ; and adding string to list	
				if (not "," in underchild.attrib["name"]):
					multiple_genes = underchild.attrib["name"].replace(";", "")
					if multiple_genes not in genlist:
						genlist.append(multiple_genes)
				
	# Start by adding the divider, this makes it easier to check the results in the txt file. 			
	outfile = open("genelist_FunHoP.txt", "a")
	outfile.write(divider)
	outfile.write("\n")

	# Write results to file 
	for line in genlist:
		outfile.write(line)
		outfile.write("\n")
	outfile.close()

	
	for element in genlist:
		print(element)


	
def main():

	# Create a new file to write results to. 
	outfile = open("genelist_FunHoP.txt", "w")

	# Go through all pathway files in the folder
	g = glob.glob('/Users/Profile/phd/testmappe/*.xml')

	for file in g:
		geneList(file)
		


if __name__ == '__main__':
	main()
