from trecUtil import medline2trec
import os

def unzipArticles():
	articles_dir = "../../data/medline-data/articles/"
	if not os.path.exists(articles_dir):
		os.mkdir(articles_dir)
	exit_status = os.system("for f in ../../data/medline-data/medline*.xml.zip; do unzip -o $f -d " + articles_dir + "; done")
	if exit_status:
		print "Nothing decompressed (medline)."

def cleanMedline():
	#unzipArticles()
	os.system('find ' + '../../data/medline-data/articles/ -type f | sed "$d" | cut -d "/" -f 5- > ' + '../../data/medline-data/filelist')
	
	medline_baseurl = "http://www.ncbi.nlm.nih.gov/pubmed/"
	doc_no = medline2trec("../../data/medline-data/","medline","filelist",medline_baseurl)

	#exit_status = os.system("for f in ../../data/medline-data/medline*.xml.zip; do rm $f; done")
	#if exit_status:
	#	print "No archives removed."
cleanMedline()
