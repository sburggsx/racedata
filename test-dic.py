#!/usr/bin/python

# Python version of RaceImport
# Restarted 8/23/15
# Steve

# opens defined file 
# fills dictionary with run data

import argparse

parser = argparse.ArgumentParser()
parser.add_argument('-i', dest='infile', help="input file", metavar='INPUT_FILE')
parser.add_argument('-o', dest='outdir', help="output directory", metavar='OUTPUT_DIR')

args = parser.parse_args()


run=dict()

with open(args.infile,"r") as infile:
	for line in infile:
		
		# Run Number
		if line.find("RUN:",0) > -1:
			run['Num']=line[4:9]
			run['DateTime']=line[13:36]

		# Round, Class, and Type	
		if line.find("RD#",0) > -1:
			run['Class']=line[0:19]
			run['Round']=line[28:36]
			run['Type']=line[18:27]

		# Car Numbers. Advances line and takes names
		if line.find("LEFT:",0) > -1:
			run['LeftNum']=line[6:17]
			run['RightNum']=line[33:36]
			line = next(infile)
			run['LeftName']=line[0:17]
			run['RightName']=line[18:36]

		# Dial Ins
		if line.find("DIAL IN",0) > -1:
			run['LeftDial']=line[0:7]
			run['RightDial']=line[28:36]

		# Reaction
		if line.find("REACTION",0) > -1:
			run['LeftReaction']=line[0:7]
			run['RightReaction']=line[28:36]

		# 60 Ft
		if line.find("60 FT",0) > -1:
			run['Left60FT']=line[0:7]
			run['Right60FT']=line[28:36]

		# ET
		if line.find("300 ET",0) > -1:
			run['LeftET']=line[0:7]
			run['RightET']=line[28:36]

		# MPH
		if line.find("300 MPH",0) > -1:
			run['LeftMPH']=line[0:7]
			run['RightMPH']=line[28:36]

		# Margin and Result
		if line.find("FINISH MARGIN",0) > -1:
			run['LeftMargin']=line[0:7]
			run['RightMargin']=line[28:36]
			line = next(infile)
			if line.find("OFF DIAL",0) > -1:
				run['LeftOffDial']=line[0:7]
				run['RightOffdial']=line[28:36]
				line = next(infile)
				run['LeftResult']=line[0:17]
				run['RightResult']=line[18:36]
			else:	
				run['LeftResult']=line[0:17]
				run['RightResult']=line[18:36]		

# Section to print contents of dictionary
# really only here for testing

		for key in run:
			if key == 'RightNum':
				print key, '=', run[key].strip(':')
			elif key == 'Round':
				print key, '=', run[key].strip('RD# ')			
			else:
				print key, '=', run[key].strip()

               # Empty this run from dictionary
		run.clear()
		

#			print run['Num'].strip()
#			print run['DateTime'].strip()
#			print run['Class'].strip()
#			print run['Round'].strip('RD# ')
#			print run['Type'].strip()
#			print run['LeftNum']
#			print run['RightNum'].strip(':')
#			print run['LeftName'].strip()
#			print run['RightName'].strip()


# Close log file
infile.close()

