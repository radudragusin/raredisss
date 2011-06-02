from trecUtil import html2trec
import os.path

def removeSocialDuplicates():
	with open("../../data/social-data/filelist","r") as f:
		paths = f.readlines()
	uniqpaths = []
	for p in paths:
		p = p.strip()
		if not os.path.basename(p) in [os.path.basename(up) for up in uniqpaths]:
			uniqpaths.append(p)
	if len(uniqpaths) == len(paths): 
		return
	with open("../../data/social-data/filelist","w") as f:
		for up in uniqpaths:
			f.write(up+'\n')
	
def cleanSocialstyrelsen():
	
	fields = [
		["title", [["id","socextContentPageArea"],["xpath","h1","0"]]], \
		["synonyms", [["class","info-box","0"],["xpath","p","2"]]], \
		["description", [["id","socextPageBody"]]]]
	required = ([0,2],[])
	removeSocialDuplicates()
	doc_no = html2trec("../../data/social-data/", "social", "filelist", fields, required)
		
cleanSocialstyrelsen()
