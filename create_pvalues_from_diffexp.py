#!/usr/bin/env python
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

	diffexp_results = pd.read_table('/Users/profile/phd/sign_table_canctr_Prensner_Voom_oct2015.txt',
		sep = "\t", header = None, names = None)
    
	
	significant_pvalues = counts.loc[counts.iloc[:,5] <= 0.05]
	creating_transformed_pvalues = np.log2(result.iloc[:,5]) * result.iloc[:,7] * -10
	significant_pvalues['trans_pvalues'] = creating_transformed_pvalues
	significant_pvalues = significant_pvalues.drop(significant_pvalues.columns[[1, 2, 3, 4, 5, 6, 7]], axis = 1)
	final_pvalues = significant_pvalues[significant_pvalues.reg.notnull()]

	final_pvalues.to_csv('pvalues_noneCorrigated_canctr_Prensner_sep17.txt', header = False, index = None, sep = '\t', mode = 'w') 

	

def main():
	extract_pvalue()
	


if __name__ == '__main__':
	main()
