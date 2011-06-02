from trecUtil import wiki2trec
import os

def renameWikiXml(path_to_file,new_file_name):
	with open(path_to_file+"filelist","r") as f:
		file_names = f.readlines()
	old_file_name = False
	for file_name in file_names:
		if file_name.startswith("api"):
			old_file_name = file_name
	if old_file_name:
		os.rename(path_to_file+old_file_name.strip(),new_file_name)
		return 1
	return 0

def cleanWikipediaRD():
	
	fields = [
		["url", [["xpath","title","0"]]],
		["title", [["xpath","title","0"]]], \
		["date", [["xpath","revision/timestamp","0"]]], \
		["description", [["xpath","revision/text","0"]]]]
	required = ([1,3], []) # lists for "mandatory" and "oneof"
	wiki_baseurl = "en.wikipedia.org/wiki/"
	
	new_file_name = "../../data/wikird-data/wikird.xml"
	if not os.path.exists(new_file_name):
		if not renameWikiXml("../../data/wikird-data/",new_file_name):
			print "Could not transform. No filelist?"
			return
	
	doc_no = wiki2trec(new_file_name, "wikird", fields, required, wiki_baseurl)
	

cleanWikipediaRD()
