
# Extract the titles (and corresp. docno) from the indexed documents 
# --- will create a index_*.titles file
python titlesExtract.py ../../indexes/index_raregenet ../../trec/ "aboutcom,gard,hon,social,madisons,wikird,nord,orphanet,omim,wikisyn,ghr"

# Sort the titles 
# --- will create a titles.p file
python titlesSort.py ../../indexes/index_raregenet.titles index_raregenet.titles.p

# Add orphanet synonyms 
# --- uses titles.p and orphadiseases.p
# --- will create diseases.p
python titlesSynonyms.py index_raregenet.titles.p index_raregenet.diseases.p

# Create disease - doc matrix
# --- uses diseases.p
# --- will create freqByDisease.p and freqByDoc.p
python constrDisDocMatrix.py ../../indexes/index_raregenet index_raregenet.diseases.p index_raregenet

echo "Use rerank.sh to run a query."
