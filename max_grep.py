#! /usr/bin/env python

import argparse
import os
import sys
import re
#from collections import defaultdict


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
	stats_file = "{}_max_grep_stats.txt".format(sam)

	# Regular Expressions
	virus_re = re.compile("chrvirus")
	human_re = re.compile("chr[1-9,XYM]")

	#Dictionaries
	#virus_dict = defaultdict(list)
	#human_dict = defaultdict(list)
	virus_dict = {}
	human_dict = {}

	# Counts
	virus_count = 0
	human_count = 0 

	with open(sam, 'r') as sam_handle: #, open(human_no_header, 'w')
		for line in sam_handle:
			# If the line is a header (@SQ/@PG)
			if line.startswith('@SQ') or line.startswith('@PG'):
				#print "Nope"
				pass
			# Virus
			elif virus_re.search(line) is not None:
				#print "Virus"
				split_line = line.split('\t')
				seq_id = split_line[0]
				hit = split_line[2]
				virus_dict[seq_id+hit] = line
				virus_count += 1
			# Human
			elif human_re.search(line) is not None:
				#print "Human"
				split_line = line.split('\t')
				seq_id = split_line[0]
				hit = split_line[2]
				human_dict[seq_id+hit] = line
				human_count += 1

	with open(stats_file, 'w') as stats:
		# Write virus
		stats.write("\nTotal Virus found:\t{}\n".format(virus_count))
		stats.write("Unique Virus found:\t{}\n".format(len(virus_dict.keys())))
		with open(virus_no_header, 'w') as virus_out:
			for key in virus_dict.keys():
				virus_out.write(virus_dict[key])
				stats.write(virus_dict[key].split('\t')[2]+'\n')
		# Write human
		stats.write("\nTotal Human found:\t{}\n".format(human_count))
		stats.write("Unique Human found:\t{}\n".format(len(human_dict.keys())))
		with open(human_no_header, 'w') as human_out:
			for key in human_dict.keys():
				human_out.write(human_dict[key])
				stats.write(human_dict[key].split('\t')[2]+'\n')

if __name__ == '__main__':
	main()
