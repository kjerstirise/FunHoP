#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pandas as pd
import numpy as np
"""
This file is used to extract p-values from the result files from performing differential expression. 
It's a fairly simple function, only extracting the significant p-values, log2-transforming them, and multiplying
with -10. This value is them multiplied with -1 (for downregulated genes) or 1 (for upregulated genes), 
and the values are then exported.
"""


def extract_pvalue():

	diffexp_results = pd.read_table('/Users/profile/Documents/GitHub/cell-lines/celllines_only/pathway_analysis/redo/diffexp_boxes_LNCaPVCaPvsRWPEPrEC_feb21.txt',
		sep = "\t", header = 0, names = None)

	significant_pvalues = diffexp_results.loc[diffexp_results.iloc[:,5] <= 0.05]

	
	reg = []
	for row in significant_pvalues['logFC']:
		if row < 0:
			reg.append(int('-1'))
		else:
			reg.append(int('1'))
	
	# This one creates a warning! But it still works..
	significant_pvalues['regulation'] = reg
	creating_transformed_pvalues = np.log2(significant_pvalues.iloc[:,5]) * significant_pvalues.iloc[:, 8] * -10

	# Another warning from this one.. 
	significant_pvalues['trans_pvalues'] = creating_transformed_pvalues
	
	significant_pvalues = significant_pvalues.drop(significant_pvalues.columns[[1, 2, 3, 4, 5, 6, 7,8]], axis = 1)
	
	final_pvalues = significant_pvalues[significant_pvalues.trans_pvalues.notnull()]
	
	print("The highest found value is: ")
	print(final_pvalues.trans_pvalues.astype(float).max())
	print("The lowest found value is: ")
	print(final_pvalues.trans_pvalues.astype(float).min())
	
	final_pvalues.to_csv('pvalues_diffexp_LNCaPVCaPvsRWPE_feb21.txt', header = True, index = None, sep = '\t', mode = 'w') 
	


def main():
	extract_pvalue()
	


if __name__ == '__main__':
	main()
