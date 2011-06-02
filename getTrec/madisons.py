from trecUtil import html2trec

def cleanMadisons():
	fields = [
		["title", [["class","headerpaneopen","0"]]], \
		["createdate", [["class","createdate","0"]]], \
		["modifydate", [["class","modifydate","0"]]], \
		["description", [["class","mpowerwrapper","0"]]]]
	required = ([0,3], []) # lists for "mandatory" and "oneof"
	doc_no = html2trec("../../data/madisons-data/", "madisons", "filelist", fields, required)
	
		
cleanMadisons()
