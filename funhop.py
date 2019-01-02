#!/usr/bin/env python
# -*- coding: utf-8 -*-

import boxlistmaker
import change_namestring
import collapse_nodes
import create_genelist
import calculate_tcga
import extend_nodes
import fix_coordinates
import remove_lose_metabolites




import create_tcga

def main():

	changed_name = change_namestring.change_namestring(pathway_path = '/Users/Profile/Documents/GitHub/cell-lines/pathways', 
										hsalist_path = '/Users/profile/Documents/GitHub/cell-lines/old_data/hsalist_july18.txt')

	genelist = create_genelist.create_genelist(changed_name)

	changed_removed = remove_lose_metabolites.remove_lose_metabolites(changed_name)

	changed_removed_fixed = fix_coordinates.fix_coordinates(changed_removed)

	changed_removed_fixed_extended = extend_nodes.extend_nodes(changed_removed_fixed)

	collapsed = collapse_nodes.collapse_nodes(changed_removed)

	duplicates = boxlistmaker.boxlistmaker(changed_name)

	boxinfo = create_tcga.calculate_counts(expression_path = 'expression_table_TCGA.txt', 
                     						meta_data_path = 'meta_data_TCGA_nov2016.txt', 
                     						count_file_path = 'TCGA_expression_counts.txt',
                     						changed_name_path = 'gene_symbol_update_file_jan2016.txt', 
                    						genelist_path = 'genliste_metabolism.txt', 
                     						boxinfo_path = 'testtable_tcga_boxinfo.txt', 
                    						expression_table_path = 'test_expression.txt')


if __name__ == '__main__':
    main()