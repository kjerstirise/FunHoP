#!/usr/bin/env python
# -*- coding: utf-8 -*-

import change_namestring
import create_genelist
import remove_lose_metabolites
import fix_coordinates
import extend_nodes
import collapse_nodes
import boxlistmaker
import create_tcga

def main():

	changed_name = change_namestring.change_namestring(pathway_path = '/Users/Profile/Documents/GitHub/cell-lines/pathways', 
										hsalist_path = '/Users/profile/Documents/GitHub/cell-lines/old_data/hsalist_july18.txt')

	genelist = create_genelist.create_genelist(changed_name)

	changed_removed = remove_lose_metabolites(changed_name)

	changed_removed_fixed = fix_coordinates(changed_removed)

	changed_removed_fixed_extended = extend_nodes(changed_removed_fixed)

	collapsed = collapse_nodes(changed_removed)

	duplicates = boxlistmaker(changed_name)

	boxinfo = create_tcga.calculate_counts()


if __name__ == '__main__':
    main()