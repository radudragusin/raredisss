from trecUtil import pubmed2trec
import os

def unzipArticles():
	articles_dir = "../../data/pmcoa-data/articles/"
	if not os.path.exists(articles_dir):
		os.mkdir(articles_dir)
	exit_status = os.system("for f in ../../data/pmcoa-data/articles.*.tar.gz; do tar -xzf $f -C " + articles_dir + "; done")
	if exit_status:
		print "Nothing decompressed (pmcoa)."
	else:
		#exit status of 0 means success
		print "Decompressed articles (pmcoa)."

def cleanPMCOA():
	
	unzipArticles()
	os.system('find ' + '../../data/pmcoa-data/articles/ -type f | sed "$d" | cut -d "/" -f 5- > ' + '../../data/pmcoa-data/filelist')
	
	pmcoa_baseurl = "www.ncbi.nlm.nih.gov/pmc/articles/PMC"
	doc_no = pubmed2trec("../../data/pmcoa-data/","pmcoa","filelist",pmcoa_baseurl)

	exit_status = os.system("for f in ../../data/pmcoa-data/articles.*.tar.gz; do rm $f; done")
	if exit_status:
		print "No archives to delete (pmcoa)."
	else:
		#exist status of 0 means success
		print "Deleted original archives (pmcoa)."

cleanPMCOA()
