#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import shutil
import create_connection
#import calculate_counts
#import calculate_single_counts
import change_namestring
import collapse_nodes
import create_genelist
import extend_nodes
import fix_coordinates
import remove_loose_metabolites



def main():

	start_folder = '/Users/profile/Documents/GitHub/cell-lines/enkelt/'
	hsa_file = 'hsalist_july18.txt'


	changed_name = os.path.join(start_folder,'changed_name/')
	if not os.path.exists(changed_name):
		os.makedirs(changed_name)

	change_namestring.change_namestring(pathway_path = start_folder,
										hsalist_path = os.path.join(start_folder,hsa_file), 
										outfile_path = changed_name)

	create_genelist.create_genelist(pathway_path = changed_name, 
									outfile_path = start_folder)


	changed_removed = os.path.join(start_folder, 'changed_removed/')
	if not os.path.exists(changed_removed):
		os.makedirs(changed_removed)

	remove_loose_metabolites.remove_loose_metabolites(pathway_path = changed_name, 
														outfile_path = changed_removed)


	changed_removed_fixed = os.path.join(start_folder, 'changed_removed_fixed/')
	if not os.path.exists(changed_removed_fixed):
		os.makedirs(changed_removed_fixed)

	fix_coordinates.fix_coordinates(pathway_path = changed_removed, 
									outfile_path = changed_removed_fixed)


	changed_removed_fixed_extended = os.path.join(start_folder, 'changed_removed_fixed_extended/')

	if not os.path.exists(changed_removed_fixed_extended):
		os.makedirs(changed_removed_fixed_extended)

	extend_nodes.extend_nodes(pathway_path = changed_removed_fixed, 
								outfile_path = changed_removed_fixed_extended)


	collapsed_nodes = os.path.join(start_folder, 'collapsed_nodes/')

	if not os.path.exists(collapsed_nodes):
		os.makedirs(collapsed_nodes)

	collapse_nodes.collapse_nodes(pathway_path = changed_removed, 
									outfile_path = collapsed_nodes)


	create_connection.find_duplicates(pathway_path = changed_name)

"""
	boxinfo = calculate_counts.calculate_counts(expression_path = 'expression_table_TCGA.txt', 
                     						meta_data_path = 'meta_data_TCGA_nov2016.txt', 
                     						count_file_path = 'TCGA_expression_counts.txt',
                     						changed_name_path = 'gene_symbol_update_file_jan2016.txt', 
                    						genelist_path = 'genliste_metabolism.txt', 
                     						boxinfo_path = 'testtable_tcga_boxinfo.txt', 
                    						expression_table_path = 'test_expression.txt')

	single_counts = calculate_single_counts.calculate_single_counts(boxinfo)

	try:
		shutil.rmtree(changed_name)
	except OSError as e:
		print("Error: %s - %s." % (e.filename, e.strerror))

"""


if __name__ == '__main__':
    main()