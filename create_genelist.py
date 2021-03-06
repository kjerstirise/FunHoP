#!/usr/bin/env python3

# -*- coding: utf-8 -*-

import itertools
import pandas as pd
import numpy as np
import xml.etree.ElementTree as ET
import glob 
import os

"""	
The create_genelist code is made for extracting the gene names in the pathways, in order to create a list 
of all of the genes in all of the pathways of interest. The code takes in the pathway files created by change_namestring,
which has the complete namestrings for each child. The result from this file is a .txt file with all the namestrings 
from all the children in all the files, indicating which of them will need extended nodes.
This file is used to calculate new values for the extended nodes.  

The reason for having one function which includes ID and one which doesn't, is that they can be used in different places
further down in FunHoP. The list without IDs is used for making the boxes in calculate_tcga, and the one with IDs is used 
in create_connection. So they're both pretty important.  

"""

def geneList_with_id(file, outfile_path):

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
			idnumber = child.attrib["id"]
			for underchild in child:
				# For children with only one gene, removing ; and adding string to list
				if ("," in underchild.attrib['name']):
					only_one_gen_string = underchild.attrib['name'].split(",")
					one_gene = only_one_gen_string[0].replace(";", "")
					if one_gene not in genlist: 
						one_gene_id = str(idnumber) + " " + one_gene
						genlist.append(one_gene_id)

				# For children with multiple genes, removing ; and adding string to list	
				if (not "," in underchild.attrib["name"]):
					multiple_genes = underchild.attrib["name"].replace(";", "")
					if multiple_genes not in genlist:
						multiple_genes_id = str(idnumber) + " " + multiple_genes
						genlist.append(multiple_genes_id)

	# Start by adding the divider, this makes it easier to check the results in the txt file. 			
	outfile = open(outfile_path + "/genelist_test_python3.txt", "a")
	outfile.write(divider)
	outfile.write("\n")

	# Write results to file 
	for line in genlist:
		outfile.write(line)
		outfile.write("\n")
	outfile.close()


	#for element in genlist:
	#	print(element)


def geneList_without_id(file, outfile_path):

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

	# Parse all files
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
	outfile = open(outfile_path + "/nodelist.txt", "a")
	outfile.write(divider)
	outfile.write("\n")

	# Write results to file 
	for line in genlist:
		outfile.write(line)
		outfile.write("\n")
	outfile.close()

	

	
def create_genelist(pathway_path, outfile_path):

	# Create a new file to write results to. 
	outfile = open(outfile_path + "/nodelist.txt", "w")

	# Go through all pathway files in the folder
	g = glob.glob(os.path.join(pathway_path,'*.xml'))

	for file in g:
		geneList_without_id(file, outfile_path)
	


if __name__ == '__main__':
	create_genelist(pathway_path, outfile_path)

