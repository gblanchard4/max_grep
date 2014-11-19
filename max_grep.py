#! /usr/bin/env python

import argparse
import os
import sys
import re
from collections import defaultdict

__author__ = "Gene Blanchard"
__email__ = "me@geneblanchard.com"

'''
Max Grep
'''


class Valid_Read:

	def __init__(self, line):

		self.line = line
		# Initialize with first mapping found
		split_line = line.split('\t')
		self.seq_id = split_line[0]
		hit = split_line[2]
		self.mappings = [hit]

	def add_mapping(self, hit):
		self.mappings.append(hit)

# Check for some defined homopolymers. Sequence is split_line[9]
def no_homopolymer(sequence):
	split_line = sequence.split('\t')
	if not 'TTTTTTTTTTTTTTTTTTTT' in split_line[9]:
		if not 'AAAAAAAAAAAAAAAAAAAA' in split_line[9]:
			if not 'TTTTTTTTTTTTTTTTCTTT' in split_line[9]:
				return True
	else:
		return False

def processing(dict, line):
	# Values from line
	split_line = line.split('\t')
	seq_id = split_line[0]
	hit = split_line[2]

	# If the item already exist in the list add a new mapping
	if seq_id in dict.keys():
		# Add the mapping to the Valid_Read mappings list
		seq_id.add_mapping(hit)
		# Increase the mappings count 
		dict[seq_id] += 1
	# Else not in the list
	else:
		# Create the valid read with initial mapping added
		seq_id = Valid_Read(line)
		# Add the valid read to the dictionary with a count of 1
		dict[seq_id] = 1

def grep(sam, test, human, verbose):
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
	# # Number of reads that pass filter
	total_virus_count = 0
	total_human_count = 0 
	# Number of homopolymers
	virus_homopolymer = 0
	human_homopolymer = 0 

	with open(sam, 'r') as sam_handle: #, open(human_no_header, 'w')
		for line in sam_handle:
			# If the line is a header (@SQ/@PG)
			if line.startswith('@SQ') or line.startswith('@PG'):
				#print "Nope"
				continue
			# Virus
			if virus_re.search(line) is not None:
				if no_homopolymer(line):
					processing(virus_dict, line)
					total_virus_count += 1
				else:
					virus_homopolymer += 1
			# Human
			elif human_re.search(line) is not None:
				if no_homopolymer(line):
					processing(human_dict, line)
					total_human_count += 1
				else:
					human_homopolymer += 1
			print "Virus:\t{}".format(len(virus_dict.keys()))
			print "Human:\t{}".format(len(human_dict.keys()))
			print "Total:\t{}\n".format(len(virus_dict.keys())+len(human_dict.keys()))


	# Just print stats, don't write files
 	if test:
 		print "Total Homopolymers found:\t{}".format(virus_homopolymer + human_homopolymer)
 		print "Virus Homopolymers found:\t{}".format(virus_homopolymer)
 		print "Human Homopolymers found:\t{}".format(human_homopolymer)
 		print "Total Virus found:\t{}".format(total_virus_count)
		print "Unique Virus found:\t{}".format(len(virus_dict.keys()))
		print "Total Human found:\t{}".format(total_human_count)
		print "Unique Human found:\t{}".format(len(human_dict.keys()))
		print "\n+Virus Mappings"
		for virus_id in virus_dict.keys():
			print ">{}".format(virus.seq_id)
			for mapping in virus_id.mappings:
				print "\t*{}".format(mapping)
		print "\n+Human Mappings"
		for human_id in human_list:
			print ">{}".format(human.seq_id)
			for mapping in human_id.mappings:
				print "\t*{}".format(mapping)
 	'''
 	# Do real work
 	else:
		with open(stats_file, 'w') as stats:
			# Homopolymer stats
			stats.write("Total Homopolymers found:\t{}".format(virus_homopolymer + human_homopolymer))
 			stats.write("Virus Homopolymers found:\t{}".format(virus_homopolymer))
 			stats.write("Human Homopolymers found:\t{}".format(human_homopolymer))
			# Write virus stats
			stats.write("\nTotal Virus found:\t{}\n".format(total_virus_count))
			stats.write("Unique Virus found:\t{}\n".format(len(virus_list)))
			# Write virus file
			with open(virus_no_header, 'w') as virus_out:
				# Write a line for each virus found in the list
				for virus in virus_list:
					virus_out.write(virus.line)
					for mapping in virus.mappings.keys():
						stats.write("\t*{}".format(mapping))
			# Write human stats
			stats.write("\nTotal Human found:\t{}\n".format(total_human_count))
			stats.write("Unique Human found:\t{}\n".format(len(human_list)))
			# Write Human file if flag passed
			if human:
				with open(human_no_header, 'w') as human_out:
					for human in human_list:
						human_out.write(human.line)
						for mapping in human.mappings.keys():
							stats.write("\t*{}".format*mapping)
	'''

def main():
	# Get command line arguments
	parser = argparse.ArgumentParser(description='Grep a sam file for virus and human sequences')

	# Input file
	parser.add_argument('-i','--input',dest='input', ,default ='test/sam.sam',help='The input stats')
	parser.add_argument('-t','--test', action='store_true', help='Test mode: Just print stats')
	parser.add_argument('--human', action='store_true', help='Write the human sam file, Default: False')
	parser.add_argument('-r','--recurse', action='store_true', help='Input is a directory, recurse and grep all sam files')
	parser.add_argument('-v','--verbose', action='store_true', help='Verbose, write mappings to stats file')

	# Parse arguments
	args = parser.parse_args()
	sam = os.path.abspath(args.input)
	test = args.test
	human = args.human
	recurse = args.recurse
	verbose = args.verbose

	if recurse:
		samlist = []
		for file in os.listdir(sam):
			if file.endswith(".sam"):
				samlist.append(sam+"/"+file)
		for sam in samlist:
			grep(sam,test,human, verbose)
	else:
		grep(sam, test, human, verbose)


if __name__ == '__main__':
	main()