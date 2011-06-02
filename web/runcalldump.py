from subprocess import call

def calldump(path_to_index, disease, path_to_output):
	#Example arguments:
	#disease = "Fibrodysplasia ossificans progressiva"
	#path_to_index = "index_focused"

	terms = disease.split()
	terms_dump = []
	terms_dump_docids = []
	f = open("calldumpterm","w").close()
	f = open("calldumpterm","r+")
	for term in terms:
		call(['/usr/local/bin/dumpindex',path_to_index,'term',term],stdout=f)
	f.close()

	f = open("calldumpterm","r")
	results = f.readlines()
	f.close()

	ids = []
	curr_ids = False
	for res in results:
		docid = res.split()[0]
		if docid.isdigit():
			curr_ids.append(docid)
		else:
			if curr_ids:
				ids.append(curr_ids)
			curr_ids = []
	ids.append(curr_ids)

	sets = [set(idlist) for idlist in ids]
	newset = sets[0]
	for i in range(1,len(sets)):
		newset = set.intersection(newset,sets[i])
	newset = list(newset)
	print newset

	f = open(path_to_output,"w")
	f.write(disease+'\n'+'\n'.join(newset)+'\n\n')
	f.write(''.join(results)+'\n\n')
	f.flush()
	for docid in newset:
		call(['/usr/local/bin/dumpindex',path_to_index,'dt',docid],stdout=f)
	f.close()
	
	return newset



with open("diseases.txt","r") as f:
	diseases = f.readlines();

open("dumpresults_focused/dumpindex.html","w").close()
f = open("dumpresults_focused/dumpindex.html","a")
f.write("<html><title>Dump Results Focused</title><body>")
f.write("<table border=0><tr><td width='100'><img src='http://code.google." +
				"com/p/raredisss/logo?cct=1301003415' width='75'></td><td><font color='grey'>" +
				"<h1>raredisss</h1>RareDisSS - Rare Diseases Decision Support " +
				"System</font></td></tr></table><br><br>")
f.write("<table border=0>")

for disease in diseases:
	dis_name = disease.split('\t')[0].strip()
	print "Disease: "+dis_name
	docids = calldump("index_focused",dis_name,"dumpresults_focused/"+dis_name.replace(' ','_'))
	f.write("<tr><td width='100'><a href="+dis_name.replace(' ','_')+"><b>"+dis_name+"</b></a></td>"+ \
		"<td width='900'>Appears in "+str(len(docids))+" documents: "+', '.join(docids)+"</td></tr>")
	try:
		dis_syns = disease.split('\t')[1].strip()
		dis_syns = dis_syns.split(',')
		for syn in dis_syns:
			syn = syn.strip()
			print "Alternative: "+syn
			docids = calldump("index_focused",syn,"dumpresults_focused/"+syn.replace(' ','_'))
			f.write("<tr><td width='100'></td><td width='900'><font color='grey' size=1>+ Alternative: " +
				"<a href="+syn.replace(' ','_')+">"+syn+"</a></font>"+
				"<br><font color='grey' size=1>Appears in "+str(len(docids))+" documents: "+
				', '.join(docids)+"</font></td></tr>")
	except:
		pass

f.write("</table></body></html>")
f.close()