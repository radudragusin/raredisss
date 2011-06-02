from subprocess import check_output

def getInternalIdForTrecID(index,trec_no):
	'''Given an index and a TREC document number, return the internal 
	document number from the index. Returns a string representing the
	internal document number.'''
	s = check_output(['/usr/local/bin/dumpindex',index,'di','docno',str(trec_no)])
	return s.strip()

def getDocForInternalID(index,idoc_no):
	'''Given an index and a Lemur internal document number, return the
	text of the document identified by that document number in the index. 
	Returns a string with the entire document.'''
	s = check_output(['/usr/local/bin/dumpindex',index,'dt',str(idoc_no)])
	return s.strip()
	
def getDumpForTerm(index,term):
	'''Given an index and a term, return the inverted list for that term
	in the index. Returns a string with the result of the dump.'''
	s = check_output(['/usr/local/bin/dumpindex',index,'term',str(term)])
	return s.strip()

def getDumpForExpression(index,expression):
	'''Given an index and an expression, return the inverted list for that 
	expression in the index. Returns a string with the result of the dump.'''
	s = check_output(['/usr/local/bin/dumpindex',index,'e',str(expression)])
	return s.strip()