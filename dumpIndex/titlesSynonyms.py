import pickle
import string
import sys

'''This script matches the document titles from titles.p with the synonyms from
orphadiseases.p, and generated a knowndiseases.p file.'''

def addOrphanetSynonyms(titlesFile,outputFile):

  def excludePunctuation(diseaseNames):
    # Exclude punctuation characters
    exclude = set(string.punctuation)
    newDiseaseNames = []
    for name in diseaseNames:
      newl = ''
      oldl = name.replace("'s","")
      for ch in oldl:
        if ch not in exclude:
          newl += ch
        else:
          newl += ' '
      newName = ' '.join(newl.title().split())
      newDiseaseNames.append(newName)
    return newDiseaseNames

  # Read document titles
  dictT = pickle.load(open(titlesFile,"rb"))

  # Read Orphanet synonyms, remove punctuation, and rewrite in file
  orphaDiseases = pickle.load(open("orphadiseases.p","rb"))
  newOrphaDiseases = []
  for disease in orphaDiseases:
    nd = excludePunctuation(disease)
    if nd not in newOrphaDiseases:
      newOrphaDiseases.append(nd)
  #pickle.dump(newOrphaDiseases, open("orphadiseases.p","wb"))
  orphaDiseases = newOrphaDiseases

  # Iterate over doc titles and orphanet synonyms for match
  disease_doc = []
  for key in dictT.iterkeys():
    #print key, titles[key]
    found = False
    for disease in orphaDiseases:
      if key in disease:
        #print "key " + key + " in " + str(disease)
        if disease in [dd[0] for dd in disease_doc]:
          break
        disease_doc.append([disease,dictT[key]])
        found = True
        break
    if not found:
      disease_doc.append([[key],dictT[key]])

  #print "disease doc:"
  #for dd in disease_doc:
  #  print str(dd)

  pickle.dump(disease_doc,open(outputFile,"wb"))

  print "Done adding orphanet synonyms. [orphanet entries: "+str(len(orphaDiseases))+\
" known diseases: "+str(len(disease_doc))+"]"

  # Uncomment if you need the orphanet diseases that did not match with the titles 
  '''
  udd = []
  # Find orphanet diseases that did not match with any title
  for disease in orphaDiseases:
    found = False
    for dd in disease_doc:
      if disease == dd[0]:
        found = True
        break
    if not found:
      udd.append(disease)

  print "unmatched:"
  for u in udd:
    print str(u)
  '''

if len(sys.argv) != 3:
  print "Usage: python titlesSynonyms.py index_rare.titles.p index_rare.diseases.p"
  exit(0)
else:
  titlesFile,outputFile = sys.argv[1],sys.argv[2]
  addOrphanetSynonyms(titlesFile,outputFile)
