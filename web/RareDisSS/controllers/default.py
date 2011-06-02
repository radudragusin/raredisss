# -*- coding: utf-8 -*- 
# this file is released under public domain and you can use without limitations

#########################################################################
## This is a samples controller
## - index is the default action of any application
## - user is required for authentication and authorization
## - download is for downloading files uploaded in the db (does streaming)
## - call exposes all registered services (none by default)
#########################################################################
import os
import time
import hashlib

def index():
    """
    Test powerTable
    """
    
    class Virtual(object):
        @virtualsettings(label=T('Source'))
        def sourcelink(self):
            return A(self.t_result.f_source,_href=self.t_result.f_url,_target='_blank')
    
    db.t_result.truncate()
    query = ""
    collection = ""
    timer = ""
    if request.vars.q:
        t0 = time.clock()
        query = request.vars.q
        checked = request.vars.c
        os.system('pwd')
        if checked == "on":
            hashstring = hashlib.md5(request.vars.q+"index_raregenet"+str(time.time())).hexdigest()
            collection = "CHECKED"
            os.system('sh runQuery.sh "'+request.vars.q+'" index_raregenet '+hashstring)
        else:
            hashstring = hashlib.md5(request.vars.q+"index_rare"+str(time.time())).hexdigest()
            collection = ""
            os.system('sh runQuery.sh "'+request.vars.q+'" index_rare '+hashstring)
        db.t_result.import_from_csv_file(open('results/'+hashstring,'r'))
        timer = time.clock() - t0
    print timer
    table = plugins.powerTable
    table.datasource = db.t_result
    table.dtfeatures['sScrollY'] = '100%'
    table.virtualfields = Virtual()
    table.dtfeatures['bSort'] = False
    table.dtfeatures['aaSortingFixed'] = [[2,'asc']]
    table.dtfeatures['iDisplayLength'] = 20
    table.dtfeatures['bPaginate'] =  False
    
    table.truncate = 60 
    table.headers = 'labels'
    table.keycolumn = 't_result.id'
    table.showkeycolumn = False
    table.extra = dict(
                       details={'detailscolumns':'t_result.f_title,t_result.f_url,t_result.f_snippet','detailscallback':URL('display_details.load')}
                       )
    table.columns = ['t_result.f_rank',
                     't_result.f_title',
                     'virtual.sourcelink',
                     #'t_result.f_source',
                     #'t_result.f_docno',
                     #'t_result.f_score',
                    ]
    table.hiddencolumns = ['t_result.f_source','t_result.f_url']
    table.dtfeatures['bInfo'] =  False
    table.dtfeatures['bFilter'] =  False
    table.dtfeatures['bAutoWidth'] =  False
    table.dtfeatures['aoColumns'] = [
            { 'sWidth': '50px' },
            { 'sWidth': '50px' },
            { 'sWidth': '50px' },
            { 'sWidth': '500px' },
            { 'sWidth': '300px' }
        ]
    
    table = table.create()
    #print request.vars.q
    return locals()
    
    
def display_details():
    """
    return a custom object to be inserted in detail for table
    """
    key = None
    cols = None
    for k in request.vars.keys():
        if k[:3] == 'dt_':
            key = request.vars[k]
        elif k[:6] == 'dtcols':
            cols = request.vars[k]

    value = key.split('.')[2]

    if cols:
        cols = cols.split(',')
        row = db(db.t_result.id==value).select(*cols)
    else:
        row = db(db.t_result.id==value).select()
    
    rows = row.as_list()[0]
    details = DIV(B("Article Title: "))
    details.append(P(str(rows['f_title'])))
    details.append(B("URL: "))
    details.append(P(A(str(rows['f_url']),_href=str(rows['f_url']),_target='_blank')))
    details.append(B("Text: "))
    details.append(P(str(rows['f_snippet'])))
    return details

def user():
    """
    exposes:
    http://..../[app]/default/user/login 
    http://..../[app]/default/user/logout
    http://..../[app]/default/user/register
    http://..../[app]/default/user/profile
    http://..../[app]/default/user/retrieve_password
    http://..../[app]/default/user/change_password
    use @auth.requires_login()
        @auth.requires_membership('group name')
        @auth.requires_permission('read','table name',record_id)
    to decorate functions that need access control
    """
    return dict(form=auth())


def download():
    """
    allows downloading of uploaded files
    http://..../[app]/default/download/[filename]
    """
    return response.download(request,db)


def call():
    """
    exposes services. for example:
    http://..../[app]/default/call/jsonrpc
    decorate with @services.jsonrpc the functions to expose
    supports xml, json, xmlrpc, jsonrpc, amfrpc, rss, csv
    """
    session.forget()
    return service()
