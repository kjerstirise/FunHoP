#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import xml.etree.ElementTree as ET
import copy
import glob

def id_finder(root):
	""" Finds the first free ID with no used IDs above it"""
	id_whole = 0
	for child in root:
		if 'id' in child.attrib:
			new = int(child.attrib['id'])
			if(id_whole <= new):
				id_whole = new
	return str(id_whole + 1)

def number_of_cases(root):
	""" Counts number of entries with multiple genes """
	casenumber = 0
	for child in root:
		if (child.attrib["type"] == "gene"):
			child_name = child.attrib["name"]
			if (child_name.startswith("hsa:")):
				split = child_name.split()
				if(len(split) > 1):
					casenumber = casenumber + 1
	return casenumber

def get_multiple_cases(root):
	""" Counts number of entries with multiple genes """
	entries = []
	for child in root:
		if (child.attrib["type"] == "gene"):
			child_name = child.attrib["name"]
			if (child_name.startswith("hsa:")):
				split = child_name.split()
				if(len(split) > 1):
					entries.append(child)
	return entries

def create_new_component(assigned_id, name, source_node, counter):
	""" Create a new component by copying an existing node

	Keyword arguments:
	assigned_id 	The ID to assign.
	name 			The name to assign.
	source_node     The node we copy everything from.
	"""


	child = ET.Element('entry')
	child.attrib = copy.deepcopy(source_node.attrib)
	child.attrib['id'] = assigned_id
	child.attrib['name'] = name

	try:
		for sub_node in source_node:	
			underchild_copy = copy.deepcopy(sub_node)
			current_y = underchild_copy.attrib["y"]
			new_y = set_y_component(current_y, counter)
			underchild_copy.attrib["y"] = new_y
			child.append(underchild_copy)
	except:
		for sub_node in source_node:
			underchild_copy = copy.deepcopy(sub_node)
			child.append(underchild_copy)

	return child


def set_y_component(current_y, counter):
	to_int = int(current_y)
	y = to_int + (17*counter)
	return str(y)	


def set_y_box(current_y_box, number_of_genes_in_box):
	y_int = int(current_y_box)
	number = int(number_of_genes_in_box)
	new_y = y_int + (3.75 * (number+1))
	return str(new_y)


def boxmaker(root, component, contained_ids):
	""" Creates a "box"-group

	Keyword arguments:
	root			The root node to append in.
	component 		The original component now grouped into a box.
	contained_ids   The IDs of the entries contained within this box.
	"""
	
	id_whole = id_finder(root)

	child = ET.Element('entry')
	child.attrib['id'] = id_whole
	child.attrib['name'] = 'undefined'
	child.attrib['type'] = 'group'
	root.append(child)

	graphics_node = None

	for sub_node in component:
		if sub_node.tag == "graphics":
			graphics_node = sub_node
			break

	underchild = ET.Element('graphics')
	underchild.attrib['type'] = 'rectangle'
	underchild.attrib['bgcolor'] = graphics_node.attrib["bgcolor"]
	underchild.attrib['fgcolor'] = graphics_node.attrib["fgcolor"]
	
	try:
		underchild.attrib['height'] = str(17*len(contained_ids))
		underchild.attrib['width'] = '55'
		underchild.attrib['x'] = graphics_node.attrib["x"]
		current_y_box = graphics_node.attrib["y"]
		new_y = set_y_box(current_y_box, len(contained_ids))
		underchild.attrib['y'] = new_y
		child.append(underchild)
	except:
		underchild.attrib['coords'] = "1,2,3,4"	

	for id_number in contained_ids:
		comp = ET.Element('component')
		comp.attrib['id'] = str(id_number)
		child.append(comp)


def get_graphics_names(node):
	"""Gets the name field of any graphics-sub node, asserts if more than one found """
	graphics_child_name_list = []
	for graphics_child in node:
		if graphics_child.tag == "graphics":
			assert(len(graphics_child_name_list) == 0)
			graphics_child_name_list = graphics_child.attrib["name"]
	graphics_child_name_list = graphics_child_name_list.split()
	return graphics_child_name_list

def set_graphics_names(node, name):
	"""Sets the name field of any graphics-sub node, asserts if more than one found """
	graphics_found = False
	for graphics_child in node:
		if graphics_child.tag == "graphics":
			assert(graphics_found == False)
			graphics_found = True
			graphics_child.attrib["name"] = name


def fix_duplicate_nodes(root):
	for child in root:
		if (child.attrib["type"] == "gene"):
			child_name = child.attrib["name"]
			if (child_name.startswith("hsa:")):
				split = child_name.split()
				if(len(split) > 1):
					new_names = split[1:]
					child.attrib["name"] = split[0]

					graphics_child_name_list = get_graphics_names(child)
					set_graphics_names(child, graphics_child_name_list[0])

					id_list = [ child.attrib["id"] ]
				
					nye_graphics_names = graphics_child_name_list[1:]

					counter = 1
					for index, name in enumerate(new_names):
						free_id = id_finder(root)
						new_component = create_new_component(free_id, name, child, counter)
						set_graphics_names(new_component, nye_graphics_names[index])
						root.append(new_component)
						id_list.append(free_id)
						counter = counter + 1

					boxmaker(root, child, id_list)

					

def test_fix_duplicate():
	root = ET.Element('pathway')

	entry = ET.Element('entry')
	entry.attrib["id"] = "1"
	entry.attrib["name"] = "hsa:1 hsa:2"
	entry.attrib["type"] = "gene"
	

	underchild = ET.Element('graphics')
	underchild.attrib['type'] = 'rectangle'
	underchild.attrib['name'] = 'foo bar'
	underchild.attrib['bgcolor'] = "#FFFFFF"
	underchild.attrib['fgcolor'] = "#FFFFFF"
	underchild.attrib['height'] = "32"
	underchild.attrib['width'] = '46'
	underchild.attrib['x'] = "0"
	underchild.attrib['y'] = "0"
	entry.append(underchild)
	root.append(entry)

	fix_duplicate_nodes(root)

	assert(len(root) == 3)

	if len(root) != 3:
		raise Exception("Would have expected 3 nodes")


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


		
def fix_file(filename_in, filnavn_ut):
	# Read in XML-file
	tree = ET.parse(filename_in)

	# Get the root node
	root = tree.getroot()

	# Find the highest ID of the file
	first_free_id = id_finder(root)


	#number_of_multiples = number_of_cases(root)
	
	#multiplied_entries = get_multiple_cases(root)

	fix_duplicate_nodes(root)

	ortholog_remover(root)

	tree.write(filnavn_ut)

	
	

def main():	
				
	g = glob.glob('/Users/Profile/Documents/GitHub/cell-lines/changed_name/testmappe/*.xml')

	for file in g:
		filename = file.split("/")
		out_file_name = "extended_nodes_TEST" + filename[8] 
		fix_file(file, out_file_name)
		print("Done")
	

if __name__ == '__main__':
	main()





































