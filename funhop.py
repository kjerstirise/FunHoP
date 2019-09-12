#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import shutil
import argparse
import extend_nodes
import collapse_nodes
import create_genelist
import fix_coordinates
import calculate_counts
import create_connection
import change_namestring
import calculate_single_counts
import remove_loose_metabolites







def main():


	cwd = os.getcwd()
	

	ap = argparse.ArgumentParser()
	#ap.add_argument("-i", "--input", required = True, 
	#		help = "Add the hsa list")
	ap.add_argument("hsa_file", 
		help = "You need the hsa/gene name converter list")
	ap.add_argument("expression_table", 
		help = "You need the expression table")
	ap.add_argument("metadata", 
		help = "You need the metadata")
	ap.add_argument("expression_counts", 
		help = "you need the expression counts")
	ap.add_argument("updated_gene_symbol", 
		help = "you need a list of updated gene symbols")

	args = vars(ap.parse_args())

	print(args)
	

	
	changed_name = os.path.join(cwd,'changed_name/')
	if not os.path.exists(changed_name):
		os.makedirs(changed_name)

	#hslist = os.path.join(cwd,args['hsa_file'])
	#hsalist2 = hslist.replace("'", "")
	#print(hslist)
	#print(hsalist2)
	
	change_namestring.change_namestring(pathway_path = cwd,
										hsalist_path = os.path.join(cwd, args['hsa_file']), 
										outfile_path = changed_name)

	print("Namestrings have been changed to include all genes")

	create_genelist.create_genelist(pathway_path = changed_name, 
									outfile_path = cwd)

	print("The list of all nodes has been extracted from the pathways")

	changed_removed = os.path.join(cwd, 'changed_removed/')
	if not os.path.exists(changed_removed):
		os.makedirs(changed_removed)

	remove_loose_metabolites.remove_loose_metabolites(pathway_path = changed_name, 
														outfile_path = changed_removed)

	print("Loose metabolites have been removed")

	changed_removed_fixed = os.path.join(cwd, 'changed_removed_fixed/')
	if not os.path.exists(changed_removed_fixed):
		os.makedirs(changed_removed_fixed)

	fix_coordinates.fix_coordinates(pathway_path = changed_removed, 
									outfile_path = changed_removed_fixed)

	print("Coordinates have been stretched to make more room for the expanded nodes")

	changed_removed_fixed_extended = os.path.join(cwd, 'changed_removed_fixed_extended/')

	if not os.path.exists(changed_removed_fixed_extended):
		os.makedirs(changed_removed_fixed_extended)

	extend_nodes.extend_nodes(pathway_path = changed_removed_fixed, 
								outfile_path = changed_removed_fixed_extended)

	print("All nodes with more than one gene have been expanded to show all genes")

	#create_connection.find_duplicates(pathway_path = changed_name)

	duplicates = calculate_counts.calculate_counts(expression_path =  os.path.join(cwd, args['expression_table']), 
											meta_data_path = os.path.join(cwd, args['metadata']), 
					 						count_file_path = os.path.join(cwd, args['expression_counts']),
											changed_name_path = os.path.join(cwd,args['updated_gene_symbol']), 
											genelist_path = os.path.join(cwd, 'nodelist.txt'), 
											boxinfo_path = os.path.join(cwd, 'testtable_tcga_boxinfo.txt'), 
											expression_table_path = os.path.join(cwd, 'test_expression.txt'))

	print("The counts for each node have been calculated")

	collapsed_nodes = os.path.join(cwd, 'collapsed_nodes/')

	if not os.path.exists(collapsed_nodes):
		os.makedirs(collapsed_nodes)

	collapse_nodes.collapse_nodes(pathway_path = changed_removed, 
									outfile_path = collapsed_nodes, 
									duplicates = duplicates)

	print("Nodes with multiple genes have been collapsed, in order to show simpler pathways")


	calculate_single_counts.calculate_single_counts(counts = os.path.join(cwd, 'testtable_tcga_boxinfo.txt'),
													 outfilepath = os.path.join(cwd, 'single_counts.txt'))

	print("The count for each single gene has been calculated based on the weights from the multiple gene nodes")

"""
	try:
		shutil.rmtree(changed_name)
	except OSError as e:
		print("Error: %s - %s." % (e.filename, e.strerror))

"""

if __name__ == '__main__':
	

	main()

