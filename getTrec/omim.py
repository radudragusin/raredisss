from trecUtil import omim2trec
import os

def cleanOmim():
	default_title = "^"
	fields = [["url","NO"],
		["title","TI",default_title], 
		["description","TX"],
		["symptoms","CS"],
		["synonyms","AV"],
		["references","RF"]]
	required = ([1,2],[])
	omim_baseurl = "www.ncbi.nlm.nih.gov/omim/"
	
	os.system("gunzip "+"../../data/omim-data/omim.txt.Z")
	doc_no = omim2trec("../../data/omim-data/omim.txt","omim",fields,required, omim_baseurl)

cleanOmim()
