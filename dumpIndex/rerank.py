import sys
import pickle
import csv

'''Rerank results based on frequency of diseases in documents.'''

# Utility functions for computing the new scores
def findDocInFreqList(docno,docFreq):
	freqForDoc = [f for f in docFreq if f[0]==docno][0]
	print "Frequency list for document "+docno+": "+str(freqForDoc)
	return freqForDoc
def getDiseasesInDoc(freqForDoc):
	diseaseList = []
	for tup in freqForDoc[1]:
		diseaseList.append(tup[0])
	return diseaseList
def getFreqOfDiseaseInDoc(cd,freqForDoc):
	return float([tup[1] for tup in freqForDoc[1] if tup[0] == cd][0])
def getNoOfDiseasesInDoc(freqForDoc):
	return len(freqForDoc[1])
def getFreqOfDiseasesInDoc(freqForDoc):
	freqSum = 0.
	for tup in freqForDoc[1]:
		freqSum += float(tup[1])
	return freqSum

# Utility functions for reading initial results and writing the reranked results
def readCSV(resultfile):
	csvReader = csv.reader(open(resultfile,"rb"),delimiter=',')
	results = []
	for row in csvReader:
		results.append(row)
	return (results[0],results[1:])
def writeCSV(results,header,resultfile):
	csvWriter = csv.writer(open(resultfile,"wb"),delimiter=',')
	csvWriter.writerow(header)
	for res in results:
		csvWriter.writerow(res)

def computeNewScore(docno,oldscore,freqForDoc):
	newscore = 1.
	cds = getDiseasesInDoc(freqForDoc)
	freqOfDiseases = getFreqOfDiseasesInDoc(freqForDoc)
	for cd in cds:
		newscore *= getFreqOfDiseaseInDoc(cd,freqForDoc) / freqOfDiseases
	return str(float(oldscore) * newscore)

def rerank(resultfile,prefix):
	print "Reranking the results"
	docFreq = pickle.load(open(prefix+"."+"freqByDoc.p","rb"))
	(header,results) = readCSV(resultfile)
	# Compute the new score for each result
	newresults = results
	for i,res in enumerate(results):
		docno = res[1]
		oldscore = res[4]
		freqForDoc = findDocInFreqList(docno,docFreq)
		newscore = computeNewScore(docno,oldscore,freqForDoc)
		newresults[i][4] = newscore
		print oldscore +"=>"+newscore
	# Sort results by rank, add new rank number
	newresults.sort(key=lambda x: abs(float(x[4])))
	for i in range(len(newresults)):
		newresults[i][0] = i+1
	# Write reranked results in file
	writeCSV(newresults,header,resultfile)
	print "Done."

if len(sys.argv) != 3:
  print "Usage: python rerank.py resultfile index_prefix"
  exit(0)
else:
  rerank(sys.argv[1],sys.argv[2])
