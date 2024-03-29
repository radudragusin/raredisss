import string
import pickle
import sys

'''This script sorts the titles from a .titles file generated by titles.py and 
creates a sorted dictionary (titles.p).'''

#titlesFile = "../../indexes/index_rare.titles"

def sortTitles(titlesFile,outputFile):
    # Read file with docnos and titles into an array
    titleLines = open(titlesFile,"r").readlines()
    titleLines = [titleLines[i].strip().split('\t') for i in range(len(titleLines))]

    # Exclude punctuation characters
    exclude = set(string.punctuation)
    for line in titleLines:
      newl = ''
      oldl = line[1].replace("'s","")
      for ch in oldl:
        if ch not in exclude:
          newl += ch
        else:
          newl += ' '
      line[1] = ' '.join(newl.title().split())

    # Sort by title
    titleLines.sort(key=lambda x: x[1].lower()) 

    # Write back to file, sorted by title
    '''
    open(titlesFile,"w").close()
    with open(titlesFile,"a") as f:
      for line in titleLines:
        f.write(line[0]+'\t'+line[1]+'\n')
    '''

    # Create dictionary for titles and their appearance
    titles = [line[1] for line in titleLines]
    dictT = dict()
    for i,title in enumerate(titles):
      if title not in dictT:
        dictT[title] = []
      dictT[title].append(titleLines[i][0])

    # Pickle the dict
    pickle.dump(dictT, open(outputFile,"wb"))

    print "Done sorting the titles. [titles: "+str(len(titleLines))+" unique: "+str(len(dictT))+"]"

    # Write also to file, sorted by title
    '''
    open(titlesFile+'.sorted',"w").close()
    with open(titlesFile+'.sorted',"a") as f:
      for key in sorted(dictT.iterkeys()):
        f.write("%s\t" % (key))
        if len(dictT[key]) == 1:
          f.write(dictT[key][0])
        else:
          ks = ''
          for k in dictT[key]:
            ks += k+','
          f.write(ks[:-1])
        f.write("\n")
    '''

if len(sys.argv) != 3:
  print "Usage: python titlesSort.py ../../indexes/index_rare.titles index_rare.titles.p"
  exit(0)
else:
  titlesFile,outputFile = sys.argv[1],sys.argv[2]
  sortTitles(titlesFile,outputFile)
