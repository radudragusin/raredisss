import sys
import pickle
import csv

'''Create a rank of diseases based on frequency of each disease in the documents.'''

# Utility functions
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

# Utility functions for reading initial results and writing the ranked diseases
def readCSV(resultfile):
	csvReader = csv.reader(open(resultfile,"rb"),delimiter=',')
	results = []
	for row in csvReader:
		results.append(row)
	return (results[0],results[1:])
def writeCSV(results,resultfile):
	csvWriter = csv.writer(open(resultfile,"wb"),quoting=csv.QUOTE_ALL,delimiter=',')
	csvWriter.writerow(['t_resdis.f_rank','t_resdis.f_disease','t_resdis.f_freq','t_resdis.f_docnos'])
	for res in results:
		csvWriter.writerow(res)

def rerank(resultfile,prefix):
	print "Ranking the diseases"
	docFreq = pickle.load(open(prefix+"."+"freqByDoc.p","rb"))
	(header,results) = readCSV(resultfile)
	
	# Create a dict of disease frequencies
	topDiseases = []
	for i,res in enumerate(results):
		docno = res[1]
		freqForDoc = findDocInFreqList(docno,docFreq)
		cds = getDiseasesInDoc(freqForDoc)
		for cd in cds:
			cdFreq = getFreqOfDiseaseInDoc(cd,freqForDoc)
			print str(cd) + ': '+ str(cdFreq)
			found = -1
			for j,dis in enumerate(topDiseases):
				if cd == dis[0]:
					found = j
					break
			if found == -1: 
				topDiseases.append([cd,int(cdFreq),[docno]])
			else:
				topDiseases[found][1] += int(cdFreq)
				topDiseases[found][2].append(docno)

	# Sort diseases by appearances in docs, and then by total frequency
	topDiseases.sort(key=lambda x: (len(x[2]),x[1]))
	topDiseases.reverse()
	
	# Transform disease names list into readable strings
	# Remove the Rare Disease entry, if it exists
#	loc = []
	newTopDiseases = topDiseases
	for i,dis in enumerate(topDiseases):
#		if dis[0] == ['Rare Disease'] or dis[0] == ['Syndrome']:
#			loc.append(i)
		newTopDiseases[i][0] = ', '.join(dis[0])
		newTopDiseases[i][2] = ', '.join(dis[2])
#	if loc != []:
#		loclen = len(loc)
#		for k in range(loclen):
#			l = loc.index(min(loc))
#			newTopDiseases.pop(min(loc)-k)
#			loc.pop(l)
	topDiseases = newTopDiseases
	
	# Add ranks
	for i,dis in enumerate(topDiseases):
		dis.insert(0,i+1)

	# Write ranked diseases in file
	writeCSV(topDiseases,resultfile+'.dis')
	print "Done."

if len(sys.argv) != 3:
  print "Usage: python rerankDiseases.py resultfile index_prefix"
  exit(0)
else:
  rerank(sys.argv[1],sys.argv[2])
