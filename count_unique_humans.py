#! /usr/bin/env python
import argparse

def main():
	# Get command line arguments
	parser = argparse.ArgumentParser(description='Convert a qiime workflow to proper lefse format')

	# Input file
	parser.add_argument('-i','--input',dest='files',  nargs='*', help='The unique counts files', required=True)
	parser.add_argument('-o','--output',dest='out', help='Output file', required=True)
	args = parser.parse_args()
	input_files = args.files
	outfile =  args.out
	with open(outfile, 'w') as output:
		for file in input_files:
			with open(file, 'r') as infile:
				for line in infile:
					if line.startswith('Unique Human found:'):
						human_count = line.rstrip('\n').split('\t')[-1]
				print "{}\t{}".format(file, human_count)
				output.write("{}\t{}\n".format(file, human_count))


if __name__ == '__main__':
	main()