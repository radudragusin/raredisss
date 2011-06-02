import fileinput
import sys
import json

'''This script gets the titles of all documents indexed - specified in the 
param file given as argument. '''

def getTitles(index,files):
  open(index+".titles","w").close()
  f = open(index+".titles","a")
  for filename in files:
    for line in fileinput.input(filename):
      if line.startswith("<DOCNO>"):
        title = line[line.index("<DOCNO>")+7:line.index("</DOCNO>")]
      if line.startswith("<title>"):
        title += "\t" + line[line.index("<title>")+7:line.index("</title>")]
        f.write(title+"\n")
  f.close()
  print "Done extracting titles."

def readCorpusFileNames(jsonFile):
  f = open(jsonFile,'r').read()
  js = json.loads(f)
  index = str(js["indexPath"]) + str(js["indexName"])
  corpusPath = str(js["corpusPath"])
  files = [corpusPath+str(filename)+".trec" for filename in js["corpusFiles"]]
  assert len(files) > 0
  return (index,files)

if len(sys.argv) != 4:
  print 'Usage: python titlesExtract.py ../../indexes/index_rare ../../trec "aboutcom,gard,hon,social,madisons,wikird,nord,orphanet"'
  print 'Usage: python titlesExtract.py ../../indexes/index_raregenet ../../trec "aboutcom,gard,hon,social,madisons,wikird,nord,orphanet,omim,wikisyn,ghr"'
  exit(0)
else:
  index = sys.argv[1]
  corpusPath = sys.argv[2]
  files = [corpusPath+f+".trec" for f in sys.argv[3].split(',')]
  getTitles(index,files)
