from wsgiref.simple_server import make_server
from webob import Request
from subprocess import call
import os

def serveDocument(environ, start_response):
    print "*"
    get = Request(environ).str_GET
    print get

    path_to_index = '../evaluation/0412/index_similar'
    try:
        docnos = get['docid']
        docnos = docnos.split(',')
    except:
        status = '200 OK'
        headers = [('Content-type', 'text/html')]
        start_response(status, headers)
        return open("results_focused.html").read()
    
    open("doctext","w").close()
    f_text = open("doctext","a")
    for docno in docnos:
        f_id = open("docid","w")
        call(['/usr/local/bin/dumpindex',path_to_index,'di','docno',docno],stdout=f_id)
        f_id.close()

        f_id = open("docid","r")
        trec_docno = f_id.readlines()
        f_id.close()

        s = ''.join(trec_docno).strip()
        print s

        call(['/usr/local/bin/dumpindex',path_to_index,'dt',s],stdout=f_text)
    
    f_text.close()

    status = '200 OK'
    headers = [('Content-type', 'text/plain')]
    start_response(status, headers)
    return open("doctext","r").read()

httpd = make_server('', 8082, serveDocument)
httpd.serve_forever()
