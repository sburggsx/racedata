#!/usr/bin/python

with open("/media/networkshare/public/14-08-21.log","r") as infile:
	for line in infile:
		if line.find("RUN:",0) > -1:
			runNum=line[4:9]
			runDateTime=line[13:36]	
		if line.find("RD#",0) > -1:
			runClass=line[0:19]
			runRound=line[28:36]
			runType=line[18:27]
		if line.find("LEFT:",0) > -1:
			runLeftNum=line[6:17]
			runRightNum=line[33:36]
			if runRightNum.find(":",0) > -1:
				runRightNum=line[34:36]
			print runNum.lstrip()
			print runDateTime.lstrip()
			print runClass.lstrip()
			print runRound.lstrip('RD# ')
			print runType.lstrip()
			print runLeftNum
			print runRightNum



	infile.close()