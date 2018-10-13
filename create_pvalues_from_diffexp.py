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

	diffexp_results = pd.read_table('/Users/profile/Documents/GitHub/cell-lines/diffexp_updated_cancertissueVsDU145_FPKM_oct18.txt',
		sep = "\t", header = 0, names = None)
	#diffexp_results = pd.read_table('/Users/profile/phd/sammenligninger/sign_table_canctr4_Kegg_TCGA_feb2017.txt',
	#	sep = "\t", header = None, names = None)
	
	print(diffexp_results.dtypes)
	print("original")
	print(diffexp_results.head())
	print(diffexp_results.size)
	significant_pvalues = diffexp_results.loc[diffexp_results.iloc[:,5] <= 0.05]

	print("Etter redusering på p-verdi")
	print(significant_pvalues.head())
	reg = []
	for row in significant_pvalues['logFC']:
		if row < 0:
			reg.append(int('-1'))
		else:
			reg.append(int('1'))
	
	significant_pvalues['regulation'] = reg
	creating_transformed_pvalues = np.log2(significant_pvalues.iloc[:,5]) * significant_pvalues.iloc[:, 8] * -10

	significant_pvalues['trans_pvalues'] = creating_transformed_pvalues
	print("etter å ha transformert")
	print(significant_pvalues)
	significant_pvalues = significant_pvalues.drop(significant_pvalues.columns[[1, 2, 3, 4, 5, 6, 7,8]], axis = 1)
	print("etter å ha fjernet")
	print(significant_pvalues.size)
	print(significant_pvalues.head())
	final_pvalues = significant_pvalues[significant_pvalues.trans_pvalues.notnull()]
	print("etter å ha fjernet negative")
	print(final_pvalues.size)
	#print(final_pvalues)
	#final_pvalues.to_csv('pvalues_diffexp_FPKM_cancerTissueVsDU145.txt', header = False, index = None, sep = '\t', mode = 'w') 
	"""
		pvalues = diffexp_results.loc[diffexp_results.iloc[:,5]] 
	pvalues.replace('\n',' ', regex = True)
	print(pvalues.head())
	significant_pvalues = float(pvalues) <= 0.05
	"""


def main():
	extract_pvalue()
	


if __name__ == '__main__':
	main()
