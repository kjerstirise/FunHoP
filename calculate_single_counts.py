#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pandas as pd
import numpy as np
import os
import sys


"""
This file finds the counts from the calculated boxes. This was done this way in order to keep the same weights all over.
The first function runs through each line, and if there's more than one gene, it passes it to the second function. 
The second function then calculates the count for each of the genes, based on the total count and the percentage. 
The final function removes the duplicates, and writes to file. The file can then be used to filter in Cytoscape. 

"""

def split_lines(boxfil):

	temp_list = []
	boxes = open(boxfil, 'r')

	for line in boxes.readlines():
		split = line.split( )

		if split[3] == '1.0':
			temp_list.append(split[0] + ' ' + split[2])

		if len(split) > 4:
			extended_node = " ".join(split)
			calculated_count = calculate_count(extended_node)	

			for line in calculated_count:	
				if line[0] not in temp_list:
					temp_list.append(line)

	
	temp_list.sort()
	final_list = []

	for item in temp_list:
		two_columns = item.split(" ")
		final_list.append(two_columns)
	
	
	remove_duplicates(final_list)
	



def calculate_count(string):
	
	counter = 0
	split = string.split()
	outlist = []
	templist = []
	for item in split:
		
		if item == 'Not-found':
			replaced_nf = item.replace('Not-found', '-1')
			counter = counter + 1
		
			templist.append(replaced_nf)
		else:
			if(item.replace('.', '').replace('e-', '').isdigit()):
				counter = counter + 1 
			templist.append(item)


	
	fikset = ' '.join(templist)



	for i in range(0, counter - 1):
		
		percentage = templist[i + counter + 1]
		total_count = templist[len(templist) - counter]
	
		single_count = (float(total_count) * float(percentage))
	
		if single_count >= 0:
			finished_pair = templist[i] + " " + str(single_count)
			outlist.append(finished_pair)

	
	return(outlist)


def remove_duplicates(genelist):
	
	labels = ['Gene', 'Value']
	counts_with_duplicates = pd.DataFrame.from_records(genelist, columns = labels)
	
	counts_without_duplicates = counts_with_duplicates.drop_duplicates(subset = 'Gene', keep = 'first')
	print("The highest value found is: ")
	print(counts_without_duplicates.Value.astype(float).max())
	print("The lowest value found is: ")
	print(counts_without_duplicates.Value.astype(float).min())
	counts_without_duplicates.to_csv('singel_FPKM_cancerTissue_oct18.txt', sep = '\t', mode ='w', header = True, index = None)


def main():
	
	mappesti = '/Users/profile/documents/GitHub/cell-lines'

	innfil = 'boxinfo_cancerTissue_FPKM_updated_oct18.txt'
	#mappesti = '/Users/profile/phd/sammenligninger/'
	#innfil = 'boxinfo_test4_feb17.txt'
	boxfil = os.path.join(mappesti, innfil)
	split_lines(boxfil)



if __name__ == '__main__':
	main()

	