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
			


def boxadder(root):

	for child in root:
		counter = 0
		if (child.attrib["type"] == "gene"):
			hsa_string = child.attrib['name']
			for underchild in child:
				name = underchild.attrib['name']
				splitname = name.split(' ')
				number_of_genes = len(hsa_string.split())
				newnamefront = splitname[0].replace(',', '').replace(';', '')
				newnameback = 'B' + str(number_of_genes)
				newname = newnamefront + '-' + newnameback
				#isThere = duplicatefinder(root, newname)
				underchild.attrib['name'] = newname
				#if isThere == False:
			#		underchild.attrib['name'] = newname
			#	if isThere == True:
			#		counter = counter + 1
			#		newname2 = newname + '-' + str(counter)
			#		underchild.attrib['name'] = newname2
			#		print(root.attrib['title'])
			#		print(child.attrib['id'])
			#		print('it was true')


def duplicatefinder(root, name):

	for child in root:
		if (child.attrib['type'] == 'gene'):
			for underchild in child:
				if underchild.attrib['name'] == name:
					return True
				else:
					return False




def collapse_nodes(pathway_path, outfile_path):
	g = glob.glob(os.path.join(pathway_path, '*.xml'))

	for file in g:
		filename = file.split("/")
		out_file_name = os.path.join(outfile_path, "collapsed_" + filename[8]) 
		tree = ET.parse(file)
		root = tree.getroot()
		ortholog_remover(root)
		boxadder(root)
		tree.write(out_file_name)


if __name__ == '__main__':
	collapse_nodes(pathway_path, outfile_path)
