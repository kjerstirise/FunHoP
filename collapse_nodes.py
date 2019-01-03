#!/usr/bin/env python
# -*- coding: utf-8 -*-

import xml.etree.ElementTree as ET
import glob



def ortholog_remover(root):
	print("orthologs")
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
			print(hsa_string)
			for underchild in child:
				name = underchild.attrib['name']
				splitname = name.split(' ')
				number_of_genes = len(hsa_string.split())
				print(number_of_genes)
				newnamefront = splitname[0].replace(',', '').replace(';', '')
				newnameback = 'B' + str(number_of_genes)
				newname = newnamefront + '-' + newnameback
				print(newname)
				print(underchild.attrib['name'])
				isThere = duplicatefinder(root, newname)
				print(isThere)
				if isThere == False:
					underchild.attrib['name'] = newname
				if isThere == True:
					counter = counter + 1
					newname2 = newname + '-' + str(counter)
					underchild.attrib['name'] = newname2


def duplicatefinder(root, name):

	for child in root:
		if (child.attrib['type'] == 'gene'):
			for underchild in child:
				if underchild.attrib['name'] == name:
					return True
				else:
					return False




def main():
	g = glob.glob('/Users/profile/Documents/GitHub/cell-lines/changed_removed_fixed/*.xml')

	for file in g:
		filename = file.split("/")
		out_file_name = "collapsed_" + filename[7] 
		tree = ET.parse(file)
		root = tree.getroot()
		ortholog_remover(root)
		boxadder(root)
		tree.write(out_file_name)


if __name__ == '__main__':
	main()
