#! /usr/bin/env python

import argparse
import os
import sys
import re

__author__ = "Gene Blanchard"
__email__ = "me@geneblanchard.com"

'''
Max Grep
'''
# Check for some defined homopolymers. Sequence is split_line[9]
def no_homopolymer(sequence):
	split_line = sequence.split('\t')
	if not 'TTTTTTTTTTTTTTTTTTTT' in split_line[9]:
		if not 'AAAAAAAAAAAAAAAAAAAA' in split_line[9]:
			if not 'TTTTTTTTTTTTTTTTCTTT' in split_line[9]:
				return True
	else:
		return False
def grep(sam, test, human):
	# Regular Expressions
	virus_re = re.compile("chrvirus")
	human_re = re.compile("chr[1-9,XYM]")

	# Output files
	virus_no_header = "{}_Human_Virus_no_header.txt".format(sam)
	human_no_header = "{}_Human_Only_no_header.txt".format(sam)
	stats_file = "{}_max_grep_stats.txt".format(sam)

	#Dictionaries
	virus_dict = {}
	human_dict = {}

	# Counts
	virus_count = 0
	human_count = 0 
	homopolymer_count = 0

	with open(sam, 'r') as sam_handle: #, open(human_no_header, 'w')
		for line in sam_handle:
			# If the line is a header (@SQ/@PG)
			if line.startswith('@SQ') or line.startswith('@PG'):
				#print "Nope"
				continue
			# Virus
			if virus_re.search(line) is not None:
				#print "Virus"
				split_line = line.split('\t')
				seq_id = split_line[0]
				hit = split_line[2]
				if no_homopolymer(line):
					virus_dict[seq_id+hit] = line
					virus_count += 1
				else:
					homopolymer_count += 1
			# Human
			elif human_re.search(line) is not None:
				#print "Human"
				split_line = line.split('\t')
				seq_id = split_line[0]
				hit = split_line[2]
				if no_homopolymer(line):
					human_dict[seq_id+hit] = line
					human_count += 1
				else:
					homopolymer_count += 1
	# Just print stats, don't write files
 	if test:
 		print "Homopolymers found:\t{}".format(homopolymer_count)
 		print "Total Virus found:\t{}".format(virus_count)
		print "Unique Virus found:\t{}".format(len(virus_dict.keys()))
		print "Total Human found:\t{}".format(human_count)
		print "Unique Human found:\t{}".format(len(human_dict.keys()))
 	# Do real work
 	else:
		with open(stats_file, 'w') as stats:
			# Homopolymer stats
			stats.write("\nHomopolymers found:\t{}".format(homopolymer_count))
			# Write virus stats
			stats.write("\nTotal Virus found:\t{}\n".format(virus_count))
			stats.write("Unique Virus found:\t{}\n".format(len(virus_dict.keys())))
			# Write virus file
			with open(virus_no_header, 'w') as virus_out:
				for key in virus_dict.keys():
					virus_out.write(virus_dict[key])
					stats.write(virus_dict[key].split('\t')[2]+'\n')
			# Write human stats
			stats.write("\nTotal Human found:\t{}\n".format(human_count))
			stats.write("Unique Human found:\t{}\n".format(len(human_dict.keys())))
			# Write virus file
			if human:
				with open(human_no_header, 'w') as human_out:
					for key in human_dict.keys():
						human_out.write(human_dict[key])
						stats.write(human_dict[key].split('\t')[2]+'\n')
def main():
	# Get command line arguments
	parser = argparse.ArgumentParser(description='Grep a sam file for virus and human sequences')

	# Input file
	parser.add_argument('-i','--input',dest='input', help='The input stats', required=True)
	parser.add_argument('-t','--test', action='store_true', help='Test mode: Just print stats')
	parser.add_argument('--human', action='store_true', help='Write the human sam file, Default: False')
	parser.add_argument('-r','--recurse', action='store_true', help='Input is a directory, recurse and grep all sam files')

	# Parse arguments
	args = parser.parse_args()
	sam = os.path.abspath(args.input)
	test = args.test
	human = args.human
	recurse = args.recurse

	if recurse:
		samlist = []
		for file in os.listdir(sam):
			if file.endswith(".sam"):
				samlist.append(file)
		for sam in samlist:
			grep(sam,test,human)
	else:
		grep(sam, test, human)


if __name__ == '__main__':
	main()