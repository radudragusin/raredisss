import pickle
import sys
from dumpUtil import *

'''This script creates a disease-document matrix, with associated frequencies,
based on an index and the knowndisease.p file.'''

#index = "../../indexes/index_rare"

def getFrequencyByDisease(diseases, index):
	print "Computing frequencies by diseases..."
	diseaseFreq = []
	for disease in diseases:
		if len(disease) == 1:
			e = "#1("+disease[0]+")"
		else:
			e = "#syn( "
			for altname in disease:
				e += "#1("+altname+") "
			e += ")"
		# Run dumpindex for the expression, and extract docids from result
		results = getDumpForExpression(index,e)
		results = results.split('\n')
		print results[0]
		results = results[1:] #remove first line of result
		docids = [res.split()[0] for res in results]
		# Create doc, frequency pairs
		uniq_docids = list(set(docids))
		uniq_docids.sort()
		freqs = []
		for docid in uniq_docids:
			freqs.append( (docid,str(docids.count(docid))) )
		# Add disease and corresponding frequencies to structure
		diseaseFreq.append([disease,freqs])
	pickle.dump(diseaseFreq,open(prefix+"."+"freqByDisease.p","wb"))
	#print str(diseaseFreq)
	print "Done."
	return diseaseFreq

def getFrequencyByDoc(diseaseFreq):
	print "Computing frequencies by documents..."
	docFreq = dict()
	for df in diseaseFreq:
		disease,freqs = df[0],df[1]
		for f in freqs:
			(docid,freq) = f
			if docid not in docFreq:
				docFreq[docid] = []
			docFreq[docid].append( (disease,freq) )
	# Transform dict to list
	docFreqList = []
	for key in docFreq.iterkeys():
		docFreqList.append([key,docFreq[key]])
	pickle.dump(docFreqList,open(prefix+"."+"freqByDoc.p","wb"))
	print str(docFreqList)
	print "Done."
	return docFreqList

if len(sys.argv) != 4:
  print "Usage: python constrDisDocMatrix.py ../../indexes/index_rare index_rare.diseases.p prefixoutput"
  exit(0)
index = sys.argv[1]
knownDiseasesFile = sys.argv[2]
prefix = sys.argv[3]

# Extract the disease names (and synonyms)
knowndiseases = pickle.load(open(knownDiseasesFile,"rb"))
diseases = []
for line in knowndiseases:
	# Exclude "Rare Disease" and "Syndrome" from the list of diseases
	if not (line[0] == ["Rare Disease"] or line[0] == ["Syndrome"]):
		diseases.append(line[0])
	
diseaseFreq = getFrequencyByDisease(diseases, index)
#diseaseFreq = pickle.load(open(prefix+".freqByDisease.p","rb"))
docFreq = getFrequencyByDoc(diseaseFreq)
