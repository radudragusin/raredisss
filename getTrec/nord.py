from trecUtil import nord2trec

def cleanNord():	
	fields = [
		["title", [["class","main_editorial_bodyCopy","0"],["xpath","h3","0"]]], \
		["divided", [["class","feature_body","0"]]]]
	required = ([0,1], []) # lists for "mandatory" and "oneof"
	doc_no = nord2trec("../../data/nord-data/", "nord", "filelist", fields, required)
		
cleanNord()
