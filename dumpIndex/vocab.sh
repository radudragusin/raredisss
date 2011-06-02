# Extract the vocabulary for the indexes
# # First row: TOTAL term_count doc_count
# # Next rows: word term_count doc_count
dumpindex ../../indexes/index_rare v > ../../indexes/index_rare.vocab
dumpindex ../../indexes/index_raregenet v > ../../indexes/index_raregenet.vocab
