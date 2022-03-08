#!/usr/bin/env python
# -*- coding: utf-8 -*-

import numpy as np
import pandas as pd
import os
import glob
import sys

def duplicate_list(fil):

	temp_list = []
	fin_list = []
	boxes = open(fil, 'r')
	list_of_singles = []
	list_of_duplicates = []
	curfile = ""
	fork = {}


	for line in boxes.readlines():
	
		check = line.split( )
		length = len(check)-1
		
		test = " ".join(check)

		#print(test)		
	

	fork = {}
	curfile = ""
	for item in temp_list:
		check = item.split(" ")
		length = len(check) - 1
		test = " ".join(check)
		#print(test)
		
		if test.startswith('---'):
			curfile = test
			continue
		else:
			newname = check[1] + '-B' + str(length)

		#print(newname)
		#fin_list.append(newname)

		f = " ".join(check[1:])

		if newname not in list_of_singles:
			list_of_singles.append(newname)
			fork[newname] = f
		elif (length > 1):
			if fork[newname] != f:
				list_of_duplicates.append(test + "_" + curfile)


		#if newnamefront in fin_list:# and length > 1 :
		#if length > 1:
		#	fin_list.append(newnamefront)
	
	print(len(list_of_singles))	
	print(len(list_of_duplicates))
	print("The duplicate nodes are:")
	for word in list_of_duplicates:
		print(word)






def find_duplicates(pathway_path):
	
	g = glob.glob(os.path.join(pathway_path, '*.xml'))

	for file in g:
		duplicate_list(file)



