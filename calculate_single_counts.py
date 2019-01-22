#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pandas as pd
import numpy as np
import os
import sys
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from collections import Counter
from matplotlib import rcParams, rc


"""
This file finds the counts from the calculated boxes. This was done this way in order to keep the same weights all over.
The first function runs through each line, and if there's more than one gene, it passes it to the second function. 
The second function then calculates the count for each of the genes, based on the total count and the percentage. 
The final function removes the duplicates, and writes to file. The file can then be used to filter in Cytoscape. 

"""

def split_lines(counts, outfilepath):

	temp_list = []
	boxes = open(counts, 'r')

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
	
	
	print_values_for_colourscale(final_list, outfilepath)
	



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


def print_values_for_colourscale(genelist, outfilepath):
	
	labels = ['Gene', 'Value']
	counts_with_duplicates = pd.DataFrame.from_records(genelist, columns = labels)
	
	counts_without_duplicates = counts_with_duplicates.drop_duplicates(subset = 'Gene', keep = 'first')
	print("The highest value found is: ")
	print(counts_without_duplicates.Value.astype(float).max())
    #This one is not really needed, as the chance of the lowest value being 0.0 is pretty high. But still.. 
	print("The lowest value found is: ")
	print(counts_without_duplicates.Value.astype(float).min())
	
	extract_values = counts_without_duplicates.iloc[:,1]
	squeeze_values = extract_values.T.squeeze()
	
	below_200 = []
	from_200_to_1000 = []
	from_1000_to_5000 = []
	from_5000_to_10000 = []
	over_10000 = []

	for element in squeeze_values:
		if (float(element)) < 200:
			below_200.append(element)
		if (float(element)) >= 200 and (float(element)) < 1000:
			from_200_to_1000.append(element)
		if (float(element)) >= 1000 and (float(element)) < 5000:
			from_1000_to_5000.append(element)
		if (float(element)) >= 5000 and (float(element)) < 10000:
			from_5000_to_10000.append(element)
		if (float(element)) >= 10000:
			over_10000.append(element)

	print("Below 200: ")
	print(len(below_200))
	print("200 to 1000: ")
	print(len(from_200_to_1000))
	print("1000 to 5000: ")
	print(len(from_1000_to_5000))
	print("5000 to 10000: ")
	print(len(from_5000_to_10000))	
	print("Above 10000: ")
	print(len(over_10000))

	
	counts_without_duplicates.to_csv(outfilepath, sep = '\t', mode ='w', header = True, index = None)
	



def calculate_single_counts(counts, outfilepath):

	split_lines(counts, outfilepath)



if __name__ == '__main__':
	calculate_single_counts(counts, outfilepath)

	
