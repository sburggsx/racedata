#!/usr/bin/python

# Python version of RaceImport
# Restarted 8/23/15
# Steve

# opens defined file 
# fills dictionary with run data

import os
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('-i', dest='infile', help="input file", metavar='INPUT_FILE')
parser.add_argument('-o', dest='outdir', help="output directory", metavar='OUTPUT_DIR')

args = parser.parse_args()

def Export_Left(rundata,outputfile):

	with open(outputfile, 'a') as out:
		out.write("insert into RunDetail (RaceNum, RaceDateTime, Class, RunType, ")
		out.write("Lane, CarNo, DriverName, DialIn, Reaction, ")
		out.write("Margin, OffDial, Result, ET) Values ")
		out.write("('%s', '%s', '%s', '%s', " % (rundata['Num'].strip(),rundata['DateTime'].strip(),rundata['RaceClass'].strip(),rundata['Type'].strip()) )
		out.write("'%s', '%s', '%s', '%s', '%s', " % ('L', rundata['LeftNum'].strip(), rundata['LeftName'].strip(), rundata['LeftDial'].strip(), rundata['LeftReaction'].strip()) )
		out.write("'%s', " % (rundata['LeftMargin'].strip()))
		out.write("'%s', '%s', '%s')\n" % (rundata['LeftOffDial'].strip(), rundata['LeftResult'].strip(), rundata['LeftET'].strip()) )
		out.close()

def Export_Right(rundata,outputfile):

	with open(outputfile, 'a') as out:
		out.write("insert into RunDetail (RaceNum, RaceDateTime, Class, RunType, ")
		out.write("Lane, CarNo, DriverName, DialIn, Reaction, ") 
		out.write("Margin, OffDial, Result, ET) Values ")
		out.write("('%s', '%s', '%s', '%s', " % (rundata['Num'].strip(),rundata['DateTime'].strip(),rundata['RaceClass'].strip(),rundata['Type'].strip()) )
		out.write("'%s', '%s', '%s', '%s', '%s', " % ('R', rundata['RightNum'].strip(":"), rundata['RightName'].strip(), rundata['RightDial'].strip(), rundata['RightReaction'].strip()) )
		out.write("'%s', " % (rundata['RightMargin'].strip()))		
		out.write("'%s', '%s', '%s')\n" % (rundata['RightOffDial'].strip(), rundata['RightResult'].strip(), rundata['RightET'].strip()) )
		out.close()

def ProcessRun(rundata,outputfileLeft,outputfileRight):
	Export_Left(rundata,outputfileLeft)
	Export_Right(rundata,outputfileRight)
	WriteLastRunNum(LastRunFile,rundata['Num'])
	run.clear()

def LastRunNumFile(infilename,outdir):
	logfile=os.path.basename(infilename)
	RunNumFile=os.path.splitext(logfile)[0]
	RunNumFile = outdir + RunNumFile + '.last'
	return RunNumFile

def WriteLastRunNum(outfile,runnum):
	with open(outfile,"w") as out:
		out.write(runnum + '\n')
		out.close()

def ReadLastRunNum(runfile):
	if os.path.exists(runfile):
		with open(runfile,"r") as runin:
			lastrun = runin.read()
			return int(lastrun)
	else:
		return 0


run={}
LastRunFile=LastRunNumFile(args.infile,args.outdir)
LastRun=ReadLastRunNum(LastRunFile)
print(LastRun)

with open(args.infile,"r") as infile:
	for line in infile:
		
		# Run Number
		if line.find("RUN:",0) > -1:
			run['Num']=line[4:9]
			run['DateTime']=line[13:36]
			outfileLeft = args.outdir + run['Num'].strip() + 'L.sql'
                        outfileRight = args.outdir + run['Num'].strip() + 'R.sql'


		# Round, Class, and Type	
		if line.find("RD#",0) > -1:
			run['RaceClass']=line[0:24]
			run['Round']=line[28:36]
			run['Type']=line[24:27]

		# Car Numbers. Advances line and takes names
		if line.find("LEFT:",0) > -1:
			run['LeftNum']=line[5:17]
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
		if line.find("100 FT",0) > -1:
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
				run['RightOffDial']=line[28:36]
				line = next(infile)
				run['LeftResult']=line[0:17]
				run['RightResult']=line[18:36]
				if int(run['Num']) > LastRun:
					ProcessRun(run,outfileLeft,outfileRight)
			else:	
				run['LeftOffDial']='0'
				run['RightOffDial']='0'
				run['LeftResult']=line[0:17]
				run['RightResult']=line[18:36]
				if int(run['Num']) > LastRun:
					ProcessRun(run,outfileLeft,outfileRight)		


#		Export_Left(run,outfileLeft)
#		Export_Right(run,outfileRight)
#print(run['RaceClass'])
#run.clear()

		# Section to print contents of dictionary
		# really only here for testing

		#		with open(outfilename,'a') as outfile: 
		#			for key in run:
		#				if key == 'RightNum':
		#					outfile.write(key + '=' + run[key].strip(':') + '\n')
		#				elif key == 'Round':
		#					outfile.write(key + '=' + run[key].strip('RD# ') + '\n')			
		#				else:
		#					outfile.write(key + '=' + run[key].strip() + '\n')


#		with open(outfilename,'a') as outfile:


		#		print run['RaceCls']
                # Empty this run from dictionary

# print outfilename		

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

