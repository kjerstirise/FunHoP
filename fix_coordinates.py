#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import xml.etree.ElementTree as ET
import copy
import glob
import pandas as pd


def fix_y(root):

	result = []

	for child in root:
		for underchild in child:
			if (child.attrib["type"] == "gene") or (child.attrib["type"] == "compound"):
				namestring = underchild.attrib["name"]
				if "," in namestring:
					length = 1
				else:
					split_namestring = namestring.split(" ")
					length = len(split_namestring)
				result.append((int(child.attrib["id"]), int(length), int(underchild.attrib["y"])))

	#print(result)
	results = pd.DataFrame(result)
	results.columns = ["ID", "length", "y"]
	#results.reset_index(drop = True, inplace = True)
	results.sort_values(by = ['y'], ascending = True, inplace = True)
	results = results.apply(pd.to_numeric, errors = 'ignore')
	#print(results)

	listres = results.values.tolist()
	print(type(listres))
	#[' '.join(x) for x in listres]

	"""	
	y = 0
	for i, column in results.iterrows():
		if column['y'] > y:
			y = column['y']
			y_string = str(y)
		if column['length'] > 1:
			value = column['length'] * 17
			print(value)
		for j, column in results.iloc[y_string:].iterrows():
			#column['y'] = column['y'] + value
			print("here")


	#print(results)
	
	result_sorted = result.sort(key = lambda x: x[2])
	#result_lines = result_sorted.split()

	print(result_sorted)
	"""

	y = 0
	counter = 0
	for row in listres:
		print(row)
		counter = counter + 1
		if row[2] > y:
			y = row[2]

		# Hvis vi har flere enn 1 gen (flyttetid)
		gene_count = row[1]
		if gene_count > 1:
			value = gene_count * 17
			print(type(value))

			for i in range(counter, len(listres)):	
				print(listres[i])
				listres[i][2] = listres[i][2] + value


	new_y = {}
	for  line in listres:
		new_y[line[0]] = line[2]

	print(new_y) 
	
	for child in root:
		if (child.attrib["type"] == "gene") or (child.attrib["type"] == "compound"):
			id_child = child.attrib["id"]
			for underchild in child:
				new_y_insert = new_y[int(id_child)]
				underchild.attrib["y"] = str(new_y_insert)

							

	
					



def main():
	tree = ET.parse('/Users/profile/Documents/GitHub/cell-lines/changed_name/changed_name_hsa00340.xml')
	#tree = ET.parse('/Users/Kjersti/phd/Kode/boxtester.xml')
	root = tree.getroot()
	fix_y(root)
	tree.write("outfile_testfile.xml")



if __name__ == '__main__':
	main()


