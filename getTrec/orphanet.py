from trecUtil import orphanet2trec
import os

def cleanOrphanet():
	default_desc = 'This term does not characterize a disease but a group of diseases. To learn about the diseases included under this term'
	fields = [
		["url",1],
		["title",2],
		["description",3,default_desc]]
	required = ([1,2],[])
	orphanet_baseurl = "www.orpha.net/consor/cgi-bin/OC_Exp.php?lng=EN&Expert="

	os.system("unzip -o -P q1w2e3r4 ../../data/orphanet-data/orpha.zip -d ../../data/orphanet-data/")
	doc_no = orphanet2trec("../../data/orphanet-data/OrphanetProduct4_descript.txt","orphanet",fields,required, orphanet_baseurl)
	#remember to remove duplicates from the file

cleanOrphanet()
