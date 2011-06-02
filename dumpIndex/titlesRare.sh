
# Extract the titles (and corresp. docno) from the indexed documents 
# --- will create a index_*.titles file
python titlesExtract.py ../../indexes/index_rare ../../trec/ "aboutcom,gard,hon,social,madisons,wikird,nord,orphanet"

# Sort the titles 
# --- will create a titles.p file
python titlesSort.py ../../indexes/index_rare.titles index_rare.titles.p

# Add orphanet synonyms 
# --- uses titles.p and orphadiseases.p
# --- will create diseases.p
python titlesSynonyms.py index_rare.titles.p index_rare.diseases.p

# Create disease - doc matrix
# --- uses diseases.p
# --- will create freqByDisease.p and freqByDoc.p
python constrDisDocMatrix.py ../../indexes/index_rare index_rare.diseases.p index_rare

echo "Use rerank.sh to run a query."
