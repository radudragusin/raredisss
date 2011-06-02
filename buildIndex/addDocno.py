import fileinput
import sys
import json
import os

trec_path = "../../trec/"

def addDocNoToFilename(start_docno,filename):
  docno = start_docno
  f = open(filename+'.nr','a')
  for line in fileinput.input(filename+'.trec'):
    if line.startswith("<DOCNO>"):
      line = "<DOCNO>"+str(docno)+"</DOCNO>\n"
      docno += 1
    f.write(line)
  f.close()
  os.rename(filename+'.nr',filename+'.trec')
  d = open(filename+'.docno','w')
  d.write(str(docno-start_docno)+'\n'+str(start_docno)+','+str(docno-1)+'\n')
  d.close()

def addDocNo(start_docno,files):
  nrDocs = []
  for file in files:
    nrDocs.append(int(open(trec_path+file+'.docno','r').readline().strip()))
  startNos = [start_docno]
  assert len(nrDocs) > 0
  for i in range(len(nrDocs)-1):
    startNos.append(startNos[-1]+nrDocs[i])
  for i,file in enumerate(files):
    print "Adding doc nos to file: "+file+".trec"
    addDocNoToFilename(startNos[i],trec_path+file)

def readCorpusFileNames(jsonFile):
  f = open(jsonFile,'r').read()
  files = [str(filename) for filename in json.loads(f)["corpusFiles"]]
  assert len(files) > 0
  return files

if len(sys.argv) != 3:
  print "Usage: python addDocno.py start_docno index_param.json"
  print "Usage: python addDocno.py start_docno 'aboutcom,ghr'"
  exit(0)
else:
  if sys.argv[2].endswith('.json'):
    files = readCorpusFileNames(sys.argv[2])
  else:
    files = sys.argv[2].split(',')
  addDocNo(int(sys.argv[1]), files)
