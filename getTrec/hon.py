from trecUtil import html2trec

def cleanHon():
	fields = [
		["title", [["class","input","5"],["xpath","option","0"]]], \
		["description", [["class","txtbeige","0"]]]]
	required = ([0,1], []) # lists for "mandatory" and "oneof"
	doc_no = html2trec("../../data/hon-data/", "hon", "filelist", fields, required)
		
cleanHon()
