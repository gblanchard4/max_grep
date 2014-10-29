#! /usr/bin/env python

import argparse
import os
import sys

__author__ = "Gene Blanchard"
__email__ = "me@geneblanchard.com"

'''
Max Grep
'''
# Check for some defined homopolymers. Sequence is split_line[9]
def no_homopolymer(sequence):
	split_line = line.split('\t')
	if not 'TTTTTTTTTTTTTTTTTTTT' in split_line[9]:
		if not 'AAAAAAAAAAAAAAAAAAAA' in split_line[9]:
			if not 'TTTTTTTTTTTTTTTTCTTT' in split_line[9]:
				return True
	else:
		return False

def main():

	'''
	Get command line arguments
	'''
	parser = argparse.ArgumentParser(description='Grep a sam file for virus and human sequences')

	# Input file
	parser.add_argument('-i','--input',dest='input', help='The input stats', required=True)

	# Parse arguments
	args = parser.parse_args()
	sam = os.path.abspath(args.input)

	# output files
	virus_no_header = "{}_Human_Virus_no_header.txt".format(sam)
	human_no_header = "{}_Human_Only_no_header.txt".format(sam)
	human_no_header_no_poly = "{}_Human_Only_no_header_no_polyA_polyT.sam".format(sam)
	human_quantification_unique_count.txt = "{}_Human_Only_quantification_unique_count.txt".format(sam)



	with open(sam, 'r') as sam_handle, 


	# Open the sam file
if __name__ == '__main__':
	main()
