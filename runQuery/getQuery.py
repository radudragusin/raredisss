'''Trasform query from plain format to trec format.'''

import sys

def query2trec(query_text, query_no="0", prior=False):
	'''Given a query's text and number, construct the trec text.
	Returns a query in trec format.
	'''
	terms = query_text.replace("(",", ").replace(")","").replace('/',', ').replace(","," ")
	
	query_trec = '<query><number>'+query_no+'</number><text>#combine('
	if prior:
		query_trec += '#prior('+prior+') '
	query_trec += ' '.join(terms.split())
	query_trec += ')</text></query>'

	return query_trec
	
if not 2 <= len(sys.argv) <= 4:
  print "Usage: python getQuery.py query_text"
  print "Usage: python getQuery.py query_text query_number"
  print	"Usage:	python getQuery.py query_text query_number prior_name"
  exit(0)
else:
  if len(sys.argv) == 2:
    query2trec(sys.argv[1])
  else:
    print "Using more than one argument - Not implemented yet"
