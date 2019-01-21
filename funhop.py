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


	start_folder = '/Users/profile/Documents/GitHub/cell-lines/enkelt/'
	hsa_file = 'hsalist_july18.txt'

	#cwd = os.getcwd()
	#print(cwd)

	changed_name = os.path.join(start_folder,'changed_name/')
	if not os.path.exists(changed_name):
		os.makedirs(changed_name)

	change_namestring.change_namestring(pathway_path = start_folder,
										hsalist_path = os.path.join(start_folder,hsa_file), 
										outfile_path = changed_name)

	print("Namestrings have been changed to include all genes")

	create_genelist.create_genelist(pathway_path = changed_name, 
									outfile_path = start_folder)

	print("The list of all nodes has been extracted from the pathways")

	changed_removed = os.path.join(start_folder, 'changed_removed/')
	if not os.path.exists(changed_removed):
		os.makedirs(changed_removed)

	remove_loose_metabolites.remove_loose_metabolites(pathway_path = changed_name, 
														outfile_path = changed_removed)

	print("Loose metabolites have been removed")

	changed_removed_fixed = os.path.join(start_folder, 'changed_removed_fixed/')
	if not os.path.exists(changed_removed_fixed):
		os.makedirs(changed_removed_fixed)

	fix_coordinates.fix_coordinates(pathway_path = changed_removed, 
									outfile_path = changed_removed_fixed)

	print("Coordinates have been stretched to make more room for the expanded files")

	changed_removed_fixed_extended = os.path.join(start_folder, 'changed_removed_fixed_extended/')

	if not os.path.exists(changed_removed_fixed_extended):
		os.makedirs(changed_removed_fixed_extended)

	extend_nodes.extend_nodes(pathway_path = changed_removed_fixed, 
								outfile_path = changed_removed_fixed_extended)

	print("All nodes with more than one gene have been expanded to show all genes")

	#create_connection.find_duplicates(pathway_path = changed_name)

	duplicates = calculate_counts.calculate_counts(expression_path = os.path.join(start_folder, 'expression_table_TCGA.txt'), 
											meta_data_path = os.path.join(start_folder, 'meta_data_TCGA_nov2016.txt'), 
					 						count_file_path = os.path.join(start_folder, 'TCGA_expression_counts.txt'),
											changed_name_path = os.path.join(start_folder,'gene_symbol_update_file_jan2016.txt'), 
											genelist_path = os.path.join(start_folder, 'nodelist.txt'), 
											boxinfo_path = os.path.join(start_folder, 'testtable_tcga_boxinfo2.txt'), 
											expression_table_path = os.path.join(start_folder, 'test_expression.txt'))

	print("The counts for each node have been calculated")

	collapsed_nodes = os.path.join(start_folder, 'collapsed_nodes2/')

	if not os.path.exists(collapsed_nodes):
		os.makedirs(collapsed_nodes)

	collapse_nodes.collapse_nodes(pathway_path = changed_removed, 
									outfile_path = collapsed_nodes, 
									duplicates = duplicates)

	print("Nodes with multiple genes have been collapsed, in order to show simpler pathways")


	calculate_single_counts.calculate_single_counts(counts = os.path.join(start_folder, 'testtable_tcga_boxinfo.txt'),
													 outfilepath = os.path.join(start_folder, 'single_counts.txt'))

	print("The count for each single gene has been calculated based on the weights from the multiple gene nodes")
"""
	try:
		shutil.rmtree(changed_name)
	except OSError as e:
		print("Error: %s - %s." % (e.filename, e.strerror))

"""


if __name__ == '__main__':
    main()