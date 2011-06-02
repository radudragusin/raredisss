'''Trasform queries from txt format to trec format.'''

def queries2trec(queries,trec_filename,prior=False):
	'''Given a list of query names and their text, create a 
	trec query parameter file.
	'''
	trec_file = open(trec_filename,"w")
	trec_text = '<parameters>\n'
	for query in queries:
		trec_text += query2trec(query[1],query[0],prior) + '\n'
	trec_text += '</parameters>'
	trec_file.write(trec_text)
	trec_file.close()

def query2trec(query_text, query_no, prior):
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
	

#Read text file with queries 
#--(one query per line, query name and text are sepparated by a tab)
f = open("queries.txt","r")
queries = [line.strip().split("\t") for line in f.readlines()]
queries2trec(queries,"queries.trec")
queries2trec(queries,"queries_priors.trec","orphan")