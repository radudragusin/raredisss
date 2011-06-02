from trecUtil import html2trec

def cleanAboutCom():
	resource_name = "aboutcom"

	fields = [
		["title", [["class","fn","0"]]], \
		["subtitle", [["id","abt"],["xpath","h2","0"]]], \
		["date", [["id","date"]]], \
		["description", [["id","articlebody"]]]]
	required = ([0,3], [])
	doc_no = html2trec("../../data/aboutcom-data/", resource_name, "filelist", fields, required)
	
cleanAboutCom()
