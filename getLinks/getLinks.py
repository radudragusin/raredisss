import os
import sys
import subprocess

if len(sys.argv) != 2:
  print "Usage: python getLinks.py param_file"
  exit(0)

#rare = ["Aboutcom","Gard","Hon","Madisons","Nord","Social","Wikird"]
#genetic = ["Ghr","Wikisyn","Omim"]
#collection = rare + genetic

if not os.path.isfile(sys.argv[1]):
  print "Parameter file not found"
  exit(0)

f = open(sys.argv[1],'r')
collection = f.readlines()
f.close()

for resource in collection:
  resource = resource.strip().capitalize()
  print "Getting links for " + resource + "..."
  os.system("javac -cp '.:../../lib/htmlunitjars/*' GetLinks"+resource+".java")
  # Could use subprocess here to do the job in background and 
  #then download data based on the status of the pid
  os.system("java -cp '.:../../lib/htmlunitjars/*:../../lib/' GetLinks"+resource)

