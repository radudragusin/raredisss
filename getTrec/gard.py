from trecUtil import html2trec

def cleanGard():
	default_desc = 'These Web pages are updated as the Genetic and Rare Diseases Information Center receives questions and as new information becomes available.'
	fields = [
		["title", [["id","lblTitle"]]], \
		["synonyms", [["id","divSynonymColumn"]]], \
		["description", [["id","lblDescriptionQuestion"]], default_desc], \
		["references", [["id","divReferences"]]]]
	required = ([0], [1,2]) # lists for "mandatory" and "oneof"
	doc_no = html2trec("../../data/gard-data/", "gard", "filelist", fields, required)
		
cleanGard()
