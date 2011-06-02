from trecUtil import html2trec

def cleanGhr():
	fields = [
		["title", [["id","tab1"]]], \
		["reviewdate", [["class","datestamp","0"]]], \
		["publishdate", [["class","datestamp","1"]]], \
		["description", [["class","allcontent","0"]]]]
	required = ([0,3], []) # lists for "mandatory" and "oneof"
	doc_no = html2trec("../../data/ghr-data/", "ghr", "filelist", fields, required)

cleanGhr()
