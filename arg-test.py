#! /usr/bin/python

import argparse

parser = argparse.ArgumentParser()

parser.add_argument('-i', dest='infile', help="input file", metavar='INPUT_FILE')
parser.add_argument('-o', dest='outfile', help="output file", metavar='OUTPUT_FILE')

args = parser.parse_args()

print args.infile

#print sys.argv[1]
