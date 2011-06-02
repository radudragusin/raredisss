from trecUtil import wiki2trec
import lxml.html as h
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

def removeWikiDuplicates(rd_file, syn_file):
	with open(rd_file,"r") as f:
		htmls = h.fromstring(f.read())
	rd_pages = htmls.xpath('page')
	with open(syn_file,"r") as f:
		htmls = h.fromstring(f.read())
	syn_pages = htmls.xpath('page')

	rd_titles = []
	for page in rd_pages:
		rd_titles.append(page.xpath("title")[0].text_content())
	syn_titles = []
	for page in syn_pages:
		syn_titles.append(page.xpath("title")[0].text_content())

	sub_syn_inds = []
	for i,title in enumerate(syn_titles):
		if not title in rd_titles:
			sub_syn_inds.append(i)

	open(syn_file,"w").close()
	f = open(syn_file,"a")	
	for i in sub_syn_inds:
		f.write(h.tostring(syn_pages[i]))
	f.close()

def cleanWikipediaSyn():
	
	default_title = "Category:"
	fields = [
		["url", [["xpath","title","0"]]], \
		["title", [["xpath","title","0"]], default_title], \
		["date", [["xpath","revision/timestamp","0"]]], \
		["description", [["xpath","revision/text","0"]]]]
	required = ([1,3], []) # lists for "mandatory" and "oneof"
	wiki_baseurl = "en.wikipedia.org/wiki/"
	
	new_file_name = "../../data/wikisyn-data/wikisyn.xml"
	if not os.path.exists(new_file_name):
		if not renameWikiXml("../../data/wikisyn-data/",new_file_name):
			print "Could not transform. No filelist?"
			return
	if os.path.exists("../../data/wikird-data/wikird.xml"):
		removeWikiDuplicates("../../data/wikird-data/wikird.xml",new_file_name)
				
	doc_no = wiki2trec(new_file_name, "wikisyn", fields, required, wiki_baseurl)

cleanWikipediaSyn()
