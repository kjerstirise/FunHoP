#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pandas as pd
import numpy as np
import os

def boxfikser(boxfil):

	liste = []
	boxes = open(boxfil, 'r')
	for line in boxes.readlines():
		
		split = line.split( )
		if split[3] == '1.0':
			
			liste.append(split[0] + ' ' + split[2])
		if len(split) > 4:
			out = " ".join(split)
			store = stringworker(out)			
			for linje in store:
				
				if linje[0] not in liste:
					liste.append(linje)

	liste.sort()
	red = remove_duplicates(liste)
	for rad in red:
		print(rad)



def stringworker(string):
	
	teller = 0
	split = string.split()
	utliste = []
	testliste = []
	for ting in split:
		
		if ting == 'Not-found':
			ting2 = ting.replace('Not-found', '-1')
			teller = teller + 1
		
			testliste.append(ting2)
		else:
			if(ting.replace('.', '').replace('e-', '').isdigit()):
				teller = teller + 1 
			testliste.append(ting)

	
	fikset = ' '.join(testliste)


	for i in range(0, teller - 1):
		
		prosent = testliste[i + teller+1]
		totalt = testliste[len(testliste) - teller]
	
		antall = (float(totalt)*float(prosent))
	
		if antall >= 0:
			ut = testliste[i] + " " + str(antall)
			utliste.append(ut)

	
	return(utliste)

def remove_duplicates(genelist):
	counts = pd.DataFrame(data = genelist)
	print(counts.head())
	counts.columns = ['Gene']


	counts2 = counts.drop_duplicates(subset = 'Gene', keep = 'first')
	counts2.to_csv('singel_gene_counts_test.txt', sep = '\t', mode ='w', header = False, index = None)


def main():
	
	mappesti = '/Users/profile/documents/GitHub/cell-lines'

	innfil = 'boxinfo_metabolisme_Prensner_fpkm_LNCaP.txt'

	boxfil = os.path.join(mappesti, innfil)
	boxfikser(boxfil)



if __name__ == '__main__':
	main()

	