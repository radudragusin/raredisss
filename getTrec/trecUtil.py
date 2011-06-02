import lxml.html as h
from lxml import etree
import os
import platform
import re
import unicodedata

trec_location = '../../trec/'

def writeStatHeader(statfile, field_names):
	# Write first row of the statistics file
	stat_str = "Filename"
	for name in field_names:
		stat_str += "\tHas_"+name
	statfile.write(stat_str+"\n")

def writeStatPerFile(statfile, fname, field_names, has_field):
	# Write statistics for file
	stat_str = fname
	for i in range(len(field_names)):
		stat_str += "\t"+str(has_field[i])
	statfile.write(stat_str+"\n")
	
def openTrecStatFiles(resource_name,append):
	filename = trec_location+resource_name
	if not append:
		open(filename+".trec","w").close()
		open(filename+".stat.log","w").close()
	trecfile = open(filename+".trec","a")
	statfile = open(filename+".stat.log","a")
	return (trecfile,statfile)

def recordIsValid(has_field, required):
	(mandatory_fields, oneof_fields) = required
	for i in mandatory_fields:
		if has_field[i] == 0:
			return False
	if len(oneof_fields) == 0:
		return True
	for i in oneof_fields:
		if has_field[i]:
			return True
	return False
	
def writeDocNo(resource_name, total_docs):
	# Write a file containing the number of documents transformed
	filename = trec_location+resource_name
	f = open(filename+'.docno','w')
	f.write(str(total_docs)+'\n')
	f.close()

def printStartMessage(resource_name):
	print "Transforming "+resource_name+" into TREC format... "

def printEndMessage(resource_name,total_docs):
	print "Done transforming "+resource_name+". ["+str(total_docs)+" docs]"

def removeWikiNoise(wiki):
	'''Based on the code shared on 
	http://stackoverflow.com/questions/4460921/extract-the-first-paragraph-from-a-wikipedia-article-python
	'''
	#Remove wiki markup from the text.
	wiki = re.sub(r'(?i)\{\{IPA(\-[^\|\{\}]+)*?\|([^\|\{\}]+)(\|[^\{\}]+)*?\}\}', lambda m: m.group(2), wiki)
	wiki = re.sub(r'(?i)\{\{Lang(\-[^\|\{\}]+)*?\|([^\|\{\}]+)(\|[^\{\}]+)*?\}\}', lambda m: m.group(2), wiki)
	wiki = re.sub(r'\{\{[^\{\}]+\}\}', '', wiki)
	wiki = re.sub(r'(?m)\{\{[^\{\}]+\}\}', '', wiki)
	wiki = re.sub(r'(?m)\{\|[^\{\}]*?\|\}', '', wiki)
	#wiki = re.sub(r'(?i)\[\[Category:[^\[\]]*?\]\]', '', wiki)
	wiki = re.sub(r'(?i)\[\[Image:[^\[\]]*?\]\]', '', wiki)
	wiki = re.sub(r'(?i)\[\[File:[^\[\]]*?\]\]', '', wiki)
	wiki = re.sub(r'\[\[[^\[\]]*?\|([^\[\]]*?)\]\]', lambda m: m.group(1), wiki)
	wiki = re.sub(r'\[\[([^\[\]]+?)\]\]', lambda m: m.group(1), wiki)
	wiki = re.sub(r'\[\[([^\[\]]+?)\]\]', '', wiki)
	wiki = re.sub(r'(?i)File:[^\[\]]*?', '', wiki)
	wiki = re.sub(r'\[[^\[\]]*? ([^\[\]]*?)\]', lambda m: m.group(1), wiki)
	wiki = re.sub(r"''+", '', wiki)
	wiki = re.sub(r'(?m)^\*$', '', wiki)
	#Remove HTML from the text.
	wiki = re.sub(r'(?i)&nbsp;', ' ', wiki)
	wiki = re.sub(r'(?i)<br[ \\]*?>', '\n', wiki)
	wiki = re.sub(r'(?m)<!--.*?--\s*>', '', wiki)
	wiki = re.sub(r'(?i)<ref[^>]*>[^>]*<\/ ?ref>', '', wiki)
	wiki = re.sub(r'(?m)<.*?>', '', wiki)
	wiki = re.sub(r'(?i)&amp;', '&', wiki)
	#Remove trailing white spaces
	wiki = ' '.join(wiki.split())
	return wiki

def html2trec(path_to_files, resource_name, path_to_filelist, fields, required, append=0):
	printStartMessage(resource_name)
	
	with open(path_to_files+path_to_filelist,"r") as f:
		filelist = f.readlines()
	
	(trecfile, statfile) = openTrecStatFiles(resource_name,append)
	
	field_names = [field[0] for field in fields]
	writeStatHeader(statfile, field_names)
	field_rules = [field[1] for field in fields]
	
	doc_no = 0

	file_has_field = [[0]*len(field_names) for i in filelist]
	
	for file_no, fname in enumerate(filelist):
		# Read content of html file
		fname = fname.strip()
		with open(path_to_files+fname,"r") as f:
			htmls = h.fromstring(f.read())
		
		# Start the document content
		doc_text = "<DOC>\n<DOCNO>"+str(doc_no+1)+"</DOCNO>\n<TEXT>\n"
		doc_text += "<url>"+fname+"</url>\n"
		
		# Extract the fields of interest from the html file
		for i, rule in enumerate(field_rules):
			try:
				default_val = False
				hs = htmls
				for cmd in rule:
					if cmd[0] == "id":
						hs = hs.get_element_by_id(cmd[1])
						#print "id", hs.text_content()
					elif cmd[0] == "class":
						hs = hs.find_class(cmd[1])[int(cmd[2])]
						#print "class", hs.text_content()
					elif cmd[0] == "xpath":
						hs = hs.xpath(cmd[1])[int(cmd[2])]
						#print "xpath", hs.text_content()
				try:	
					default_val = fields[i][2]
				except:
					pass
				if default_val:
					if hs.text_content().startswith(default_val):
						raise Error
				doc_text += "<"+field_names[i]+">"+' '.join(hs.text_content().split())+"</"+field_names[i]+">\n"
				file_has_field[file_no][i] = 1
			except:
				#print "no "+field_names[i]+" for file "+fname
				pass
			
		doc_text += "</TEXT>\n</DOC>\n"
		
		# Write doc into trecfile if all required fields were found
		if recordIsValid(file_has_field[file_no], required):
			trecfile.write(doc_text.encode("ascii","ignore"))
			doc_no += 1
		
		writeStatPerFile(statfile, fname, field_names, file_has_field[file_no])
			
	trecfile.close()
	statfile.close()
	writeDocNo(resource_name, doc_no)
	
	printEndMessage(resource_name,doc_no)

	return doc_no

def nord2trec(path_to_files, resource_name, path_to_filelist, fields, required, append=0):
	printStartMessage(resource_name)
	
	with open(path_to_files+path_to_filelist,"r") as f:
		filelist = f.readlines()

	(trecfile, statfile) = openTrecStatFiles(resource_name,append)

	field_names = [field[0] for field in fields]
	writeStatHeader(statfile, field_names)
	field_rules = [field[1] for field in fields]

	doc_no = 0

	file_has_field = [[0]*len(field_names) for i in filelist]

	for file_no, fname in enumerate(filelist):
		# Read content of html file
		fname = fname.strip()
		try:
			with open(path_to_files+fname,"r") as f:
				htmls = h.fromstring(f.read())

			# Start the document content
			doc_text = "<DOC>\n<DOCNO>"+str(doc_no+1)+"</DOCNO>\n<TEXT>\n"
			doc_text += "<url>"+fname.replace(' ','%20')+"</url>\n"

			# Extract the fields of interest from the html file
			for i, rule in enumerate(field_rules):
				try:
					default_val = False
					hs = htmls
					for cmd in rule:
						if cmd[0] == "id":
							hs = hs.get_element_by_id(cmd[1])
						elif cmd[0] == "class":
							hs = hs.find_class(cmd[1])[int(cmd[2])]
						elif cmd[0] == "xpath":
							hs = hs.xpath(cmd[1])[int(cmd[2])]
					try:	
						default_val = fields[i][2]
					except:
						pass
					if default_val:
						if hs.text_content().startswith(default_val):
							raise Error

					# NORD-Specific code
					content = ' '.join(hs.text_content().split())
					if field_names[i] == "divided":
						sections = ["Synonyms of","Disorder Subdivisions","General Discussion","Organizations related to"]
						ind = [0]*len(sections)
						try:
							for k,section in enumerate(sections):
								ind[k] = content.index(section)
						except:
							print "cannot get sections"
						try:
							doc_text += "<synonyms>"+content[ind[0]+len(sections[0]):ind[1]]+"</synonyms>\n"
							doc_text += "<subdivision>"+content[ind[1]+len(sections[1]):ind[2]]+"</subdivision>\n"
							doc_text += "<description>"+content[ind[2]+len(sections[2]):ind[3]]+"</description>\n"
						except:
							print "cannot divide"
							pass
					else:
						doc_text += "<"+field_names[i]+">"+content+"</"+field_names[i]+">\n"
					file_has_field[file_no][i] = 1
				except:
					pass

			doc_text += "</TEXT>\n</DOC>\n"

			# Write doc into trecfile if all required fields were found
			if recordIsValid(file_has_field[file_no], required):
				trecfile.write(doc_text.encode("ascii","ignore"))
				doc_no += 1

		except:
			print "Could not open file: "+fname

		writeStatPerFile(statfile, fname, field_names, file_has_field[file_no])

	trecfile.close()
	statfile.close()
	writeDocNo(resource_name, doc_no)

	printEndMessage(resource_name, doc_no)

	return doc_no

def wiki2trec(path_to_file, resource_name, fields, required, wiki_baseurl, append=0):
	printStartMessage(resource_name)

	with open(path_to_file,"r") as f:
		htmls = h.fromstring(f.read())
	pages = htmls.xpath('page')

	(trecfile, statfile) = openTrecStatFiles(resource_name,append)

	field_names = [field[0] for field in fields]
	writeStatHeader(statfile, field_names)
	field_rules = [field[1] for field in fields]

	doc_no = 0

	page_has_field = [[0]*len(field_names) for i in range(len(pages))]

	for page_no,page in enumerate(pages):
		doc_text = "<DOC>\n<DOCNO>"+str(doc_no+1)+"</DOCNO>\n<TEXT>\n"

		# Extract the fields of interest from the html file
		for i, rule in enumerate(field_rules):
			try:
				default_val = False
				p = page
				for cmd in rule:
					if cmd[0] == "xpath":
						p = p.xpath(cmd[1])[int(cmd[2])]
				try:	
					default_val = fields[i][2]
				except:
					pass
				if default_val:
					if p.text_content().startswith(default_val):
						raise Error
				content = ' '.join(p.text_content().split())
				content = content.replace(u'\xe2','-')
				if field_names[i] == "url":
					doc_text += "<"+field_names[i]+">"+wiki_baseurl+content.replace(' ','%20')+"</"+field_names[i]+">\n"
				elif field_names[i] == "description":
					content = removeWikiNoise(content)
					doc_text += "<"+field_names[i]+">"+content+"</"+field_names[i]+">\n"
				else:
					doc_text += "<"+field_names[i]+">"+content+"</"+field_names[i]+">\n"
				page_has_field[page_no][i] = 1
			except:
				pass

		doc_text += "</TEXT>\n</DOC>\n"

		if recordIsValid(page_has_field[page_no], required):
			trecfile.write(doc_text.encode("ascii","ignore"))
			#trecfile.write(unicodedata.normalize('NFD',unicode(doc_text)).encode("ascii","ignore"))
			doc_no += 1

		writeStatPerFile(statfile, str(page_no), field_names, page_has_field[page_no])

	trecfile.close()
	statfile.close()
	writeDocNo(resource_name, doc_no)

	printEndMessage(resource_name, doc_no)

	return doc_no

def orphanet2trec(path_to_file, resource_name, fields, required, orphanet_baseurl, append=0):
	printStartMessage(resource_name)

	with open(path_to_file,"r") as f:
		orpha_lines = f.readlines()
	orpha_data = [line.split('\t') for line in orpha_lines if line.strip()]
	orpha_data = orpha_data[2:]

	(trecfile, statfile) = openTrecStatFiles(resource_name,append)

	field_names = [field[0] for field in fields]
	writeStatHeader(statfile, field_names)
	field_tabs = [field[1] for field in fields]
	
	doc_no = 0

	record_has_field = [[0]*len(field_names) for i in range(len(orpha_data))]
	for record_no, record in enumerate(orpha_data):
		# Start the document content
		doc_text = "<DOC>\n<DOCNO>"+str(doc_no+1)+"</DOCNO>\n<TEXT>\n"
		# Extract the fields of interest
		for i,tab in enumerate(field_tabs):
			try:
				tab_content = str(record[tab].strip())
				default_val = False
				try:	
					default_val = fields[i][2]
				except:
					pass
				if default_val:
					if tab_content.startswith(default_val):
						raise Error
				if field_names[i] == "url":
					doc_text += "<"+field_names[i]+">"+orphanet_baseurl+tab_content+"</"+field_names[i]+">\n"
				else:
					doc_text += "<"+field_names[i]+">"+tab_content+"</"+field_names[i]+">\n"
				record_has_field[record_no][i] = 1
			except:
				pass
		doc_text += "</TEXT>\n</DOC>\n"
		
		# Write doc into trecfile if all required fields were found
		if recordIsValid(record_has_field[record_no], required):
			trecfile.write(doc_text)
			doc_no += 1
		
		writeStatPerFile(statfile, str(record_no), field_names, record_has_field[record_no])
	
	trecfile.close()
	statfile.close()
	writeDocNo(resource_name, doc_no)

	printEndMessage(resource_name, doc_no)

	return doc_no	
			
def omim2trec(path_to_file, resource_name, fields, required, omim_baseurl, append=0):
	printStartMessage(resource_name)
	
	with open(path_to_file,"r") as f:
		omim_data = f.read()
	omim_records = omim_data.split("*RECORD*")[1:]
	
	(trecfile, statfile) = openTrecStatFiles(resource_name,append)
	
	valid_fields_tag = [field[0] for field in fields]
	writeStatHeader(statfile, valid_fields_tag)
	valid_fields_id = [field[1] for field in fields]
	
	doc_no = 0

	record_has_field = [[0]*len(valid_fields_tag) for i in range(len(omim_records))]
	
	for record_no,record in enumerate(omim_records):
		rec_fields = record.split("*FIELD*")[1:]
		doc_text = "<DOC>\n<DOCNO>"+str(doc_no+1)+"</DOCNO>\n<TEXT>\n"
		
		for field in rec_fields:
			if field.strip()[:2] in valid_fields_id:
				i = valid_fields_id.index(field.strip()[:2])
				content = ' '.join(field.strip()[3:].split())
				default_val = False
				try:	
					default_val = fields[i][2]
				except:
					pass
				if not default_val or (default_val and not content.startswith(default_val)):
					if valid_fields_tag[i] == "url":
						doc_text += "<"+valid_fields_tag[i]+">"+omim_baseurl+content+"</"+valid_fields_tag[i]+">\n"
					if valid_fields_tag[i] == "title":
						content = re.sub(r"[\*\#\+\%\^]*[0-9]{6}","",content).strip().title()
						content = content.replace(";;",";")
						doc_text += "<"+valid_fields_tag[i]+">"+content+"</"+valid_fields_tag[i]+">\n"
					else:
						doc_text += "<"+valid_fields_tag[i]+">"+content+"</"+valid_fields_tag[i]+">\n"
					record_has_field[record_no][i] = 1
		doc_text += "</TEXT>\n</DOC>\n"
		
		# Write doc into trecfile if all required fields were found
		if recordIsValid(record_has_field[record_no], required):
			trecfile.write(doc_text)
			doc_no += 1
		
		writeStatPerFile(statfile, str(record_no), valid_fields_tag, record_has_field[record_no])
	
	trecfile.close()
	statfile.close()
	writeDocNo(resource_name, doc_no)

	printEndMessage(resource_name, doc_no)
	
	return doc_no

	
def pubmed2trec(path_to_files, resource_name, path_to_filelist, pmcoa_baseurl, append=0):
	printStartMessage(resource_name)
	
	with open(path_to_files+path_to_filelist,"r") as f:
		filelist = f.readlines()
	
	(trecfile, statfile) = openTrecStatFiles(resource_name,append)
	
	doc_no = 0
	
	field_names = ["title","url","abstract","description","references"]
	writeStatHeader(statfile, field_names)
	file_has_field = [[0]*len(field_names) for i in range(len(filelist))]
	
	for file_no, fname in enumerate(filelist):
		fname = fname.strip()
		#print "Parsing file: "+fname
		try:
			root = etree.iterparse(path_to_files+fname)
		except:
			print "Could not parse file: "+fname
			break
		doc_text = "<DOC>\n<DOCNO>"+str(doc_no+1)+"</DOCNO>\n<TEXT>\n"
		isTitleSet = False # use the first title tag found as title, the rest as references
		abstract = []
		references = []
		description = []
		for action,elem in root:
			if elem.tag == "article-title":
				etree.strip_tags(elem,"italic","bold")
				if not isTitleSet:
					if elem.text:
						doc_text += "<title>"+' '.join(elem.text.split())+"</title>\n"
						file_has_field[file_no][0] = 1
					isTitleSet = True
				else:
					if elem.text:
						references.append(' '.join(elem.text.split()))
						file_has_field[file_no][4] = 1
			elif elem.tag == "article-id":
				if elem.get("pub-id-type") == "pmc":
					if elem.text:
						doc_text += "<url>"+pmcoa_baseurl+' '.join(elem.text.split())+"</url>\n"
						file_has_field[file_no][1] = 1
			elif elem.tag == "abstract":
				for text in elem.iter():
					if text.text:
						abstract.append(' '.join(text.text.split()))
						file_has_field[file_no][2] = 1
			elif elem.tag == "body":
				for text in elem.iter():
					if text.text:
						description.append(' '.join(text.text.split()))
						file_has_field[file_no][3] = 1
		doc_text += "<abstract>"+''.join(abstract)+"</abstract>\n"
		doc_text += "<description>"+''.join(description)+"</description>\n"
		doc_text += "<references>"+' '.join(references)+"</references>\n"
		doc_text += "</TEXT>\n</DOC>\n"
		# Only write docs that have a title, a PMC id, and have an abstract or description
		if file_has_field[file_no][0] and file_has_field[file_no][1] and (file_has_field[file_no][2] or file_has_field[file_no][3]):
			trecfile.write(doc_text.encode("ascii","ignore"))
			doc_no += 1
		writeStatPerFile(statfile, fname, field_names, file_has_field[file_no])

	trecfile.close()
	statfile.close()
	writeDocNo(resource_name, doc_no)	

	printEndMessage(resource_name, doc_no)

	return doc_no
	
def medline2trec(path_to_files, resource_name, path_to_filelist, medline_baseurl, append=0):
	printStartMessage(resource_name)
	
	with open(path_to_files+path_to_filelist,"r") as f:
		filelist = f.readlines()
		
	doc_no = 0
	
	field_names = ["title","url","abstract"]
	
	for file_no, fname in enumerate(filelist):
		fname = fname.strip()
		#print "Parsing file: "+fname
		try:
			root = etree.iterparse(path_to_files+fname)
		except:
			print "Could not parse file: "+fname
			break
		
		(trecfile, statfile) = openTrecStatFiles(os.path.basename(fname),append)

		#writeStatHeader(statfile, field_names)
		#file_has_field = [[0]*len(field_names) for i in range(len(filelist))]
		have_title = 0
		have_url = 0
		have_abstract = 0
		
		for action,elem in root:
			if elem.tag == "ArticleTitle":
				if elem.text:
					articleTitle = ' '.join(elem.text.split())
					#file_has_field[file_no][0] = 1
					have_title += 1
			elif elem.tag == "PMID":
				if elem.text:
					articlePMID = ' '.join(elem.text.split())
					#file_has_field[file_no][1] = 1
					have_url += 1
			elif elem.tag == "AbstractText":
				articleAbstract = []
				for text in elem.iter():
					if text.text:
						articleAbstract.append(' '.join(text.text.split()))
				if len(articleAbstract):
					#file_has_field[file_no][2] = 1
					have_abstract += 1
					doc_text = "<DOC>\n<DOCNO>"+str(doc_no+1)+"</DOCNO>\n<TEXT>\n"
					doc_text += "<url>"+medline_baseurl+articlePMID+"</url>\n"
					doc_text += "<title>"+articleTitle+"</title>\n"
					doc_text += "<abstract>"+''.join(articleAbstract)+"</abstract>\n"
					doc_text += "</TEXT>\n</DOC>\n"
					trecfile.write(doc_text.encode("ascii","ignore"))
					doc_no +=1
		statfile.write("With title:"+str(have_title)+"\nWith PMID:"+str(have_url)+"\nWith Abstract:"+str(have_abstract))
		#writeStatPerFile(statfile, fname, field_names, file_has_field[file_no])
	
		trecfile.close()
		statfile.close()
		writeDocNo(os.path.basename(fname), doc_no)
		printEndMessage(os.path.basename(fname), doc_no)
	printEndMessage(resource_name, doc_no)
	
	return doc_no
