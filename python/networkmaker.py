#this file will read the TNS, PAC and Garasi data and create edgelists for gephi

#import
import itertools
import re
import glob

for fileItem in glob.glob("../input/rawcsv/*.csv"):
	fileName = fileItem.replace("../input/rawcsv/","").replace(".csv","")
	personDict = {}
	csv = open(fileItem).readlines()
	gephi = "Source,Target,Type,Weight\n"

	for line in csv:
		if ("," in line):
			peopleArray = re.sub(r"\s","", line).split(",")
			for subset in itertools.combinations(peopleArray, 2): #iterate trhough each pair and name it
				name = subset[0] + "_" + subset[1]
				altName = subset[1] + "_" + subset[0]
			
				#if already in dict, increase the degree, otherwise add new item to edgelist
				if (name in personDict):
					personDict[name]["degree"] = personDict[name]["degree"]+1
			
				#make sure a->b is not duplicated as b->a	
				elif (altName in personDict): 
					personDict[altName]["degree"] = personDict[altName]["degree"]+1
		
				#if not in list, give it degree of 1		
				else:
					personDict[name] = {}
					personDict[name]["from"] = subset[0]
					personDict[name]["to"] = subset[1]
					personDict[name]["degree"] = 1

	for key,value in personDict.items():
		gephi += str(value["from"]) + "," + str(value["to"]) + ",Undirected," + str(value["degree"]) + "\n"

	with open("../gephi/input/edgeInfo/%s_edgeInfo.csv" % fileName, "w") as file:
		file.write(gephi)
	
	print "%s created successfully!" % fileName
