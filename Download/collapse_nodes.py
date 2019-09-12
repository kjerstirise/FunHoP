#!/usr/bin/env python
# -*- coding: utf-8 -*-

import xml.etree.ElementTree as ET
import glob
import os


def ortholog_remover(root):
	#print("orthologs")
	number = 0;
	for child in root:
		if (child.attrib["type"] == "ortholog"):
			number += 1
	for child in root:
		if (child.attrib["type"] == "ortholog"):
			root.remove(child)
	if (number > 0):
		ortholog_remover(root)
			


def boxadder(root, duplicates):

	for child in root:
		counter = 0
		if (child.attrib["type"] == "gene"):
			hsa_string = child.attrib['name']
			for underchild in child:
				name = underchild.attrib['name']
				splitname = name.split(' ')

				if name in duplicates.keys():
					underchild.attrib['name'] = duplicates[name]

				else:
					number_of_genes = len(hsa_string.split())
					newnamefront = splitname[0].replace(',', '').replace(';', '')
					newnameback = 'B' + str(number_of_genes)
					newname = newnamefront + '-' + newnameback
					underchild.attrib['name'] = newname
	


def duplicatefinder(root, name):

	for child in root:
		if (child.attrib['type'] == 'gene'):
			for underchild in child:
				if underchild.attrib['name'] == name:
					return True
				else:
					return False




def collapse_nodes(pathway_path, outfile_path, duplicates):
	g = glob.glob(os.path.join(pathway_path, '*.xml'))

	for file in g:
		filename = file.split("/")
		out_file_name = os.path.join(outfile_path, "collapsed_" + filename[7]) 
		tree = ET.parse(file)
		root = tree.getroot()
		ortholog_remover(root)
		boxadder(root, duplicates)
		tree.write(out_file_name)


if __name__ == '__main__':
	collapse_nodes(pathway_path, outfile_path, duplicates)
