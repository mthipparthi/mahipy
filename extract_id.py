import re
import argparse
'''
		This script is to extarct pattern 
		"Loading [sc_ow_loading_1234]""
		from html file
		Reference: https://mkaz.com/2014/07/26/python-argparse-cookbook/
'''
arg_parser = argparse.ArgumentParser(description='Generates Ids from inputfile')
arg_parser.add_argument('-i','--inputfile', required=True,type=argparse.FileType('r'),help='Input HTML File')
arg_parser.add_argument('-o','--outputfile',required=True,type=argparse.FileType('w'),help='Output file')
args = arg_parser.parse_args()

pattern="([\w\s\.-]+\[[\w_]+\])<"
re.compile(pattern)

with args.inputfile as f:
	for line in f:
		match = re.search(pattern,line)
		if match:
			args.outputfile.write(match.group(1))
			args.outputfile.write("\n")

args.outputfile.close()
