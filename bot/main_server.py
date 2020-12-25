#! /usr/bin/env python
# -*- coding: utf-8 -*-

from flask import Flask
from flask_cors import CORS
from flask import request
import datetime
import math
app = Flask(__name__)
CORS(app)

import sys
reload(sys)
sys.setdefaultencoding('utf-8')

@app.route('/')
def hello_world():
    return 'API'

@app.route('/test/')
def test (access_code):
    answer = "Отказано в доступе ..."
    return answer


@app.route('/n_users/<access_code>/<email_phone>/<password>/')     ### +1
def n_users (access_code,email_phone,password):
    import iz_func    
    import json
    db,cursor = iz_func.connect ()
    list = []
    sql = "select id,blocked,email,full_name,is_admin,password,phone from n_users where (email = '"+str(email_phone)+"' or phone = '"+str(email_phone)+"') and password = '"+str(password)+"' "
    print ('[sql1] :',sql)
    cursor.execute(sql)
    results2 = cursor.fetchall()        
    for row2 in results2:    
        id,blocked,email,full_name,is_admin,password,phone = row2
        list.append ({
            'id': id,
            'blocked': blocked,
            'email': email,
            'full_name': full_name,
            'is_admin': is_admin,
            'password': password,
            'phone': phone
        }) 
    answer = json.dumps(list)    
    #answer = "Отказано в доступе ..."
    return answer


@app.route('/n_userList/<access_code>/<sort_by>/<sort_type>/')   #### +2
def userList (access_code,sort_by,sort_type):
    import iz_func    
    import json
    db,cursor = iz_func.connect ()
    list = []
    sql = "select id,blocked,email,full_name,is_admin,password,phone from n_users where 1=1 ORDER BY "+str(sort_by)+" "+str(sort_type)+" "
    print ('[sql2] :',sql)
    cursor.execute(sql)
    results2 = cursor.fetchall()        
    for row2 in results2:    
        id,blocked,email,full_name,is_admin,password,phone = row2
        list.append ({
            'id': id,
            'blocked': blocked,
            'email': email,
            'full_name': full_name,
            'is_admin': is_admin,
            'password': password,
            'phone': phone
        }) 
    answer = json.dumps(list)    
    #answer = "Отказано в доступе ..."
    return answer



@app.route('/n_searchUser/<access_code>/<search_text>/')   ### 3
def searchUser (access_code,search_text):
    import iz_func    
    import json
    db,cursor = iz_func.connect ()
    list = []
    sql = "select id,blocked,email,full_name,is_admin,password,phone from n_users where full_name like '%"+str(search_text)+"%' "
    print ('[sql3] :',sql)
    cursor.execute(sql)
    results2 = cursor.fetchall()        
    for row2 in results2:    
        id,blocked,email,full_name,is_admin,password,phone = row2
        list.append ({
            'id': id,
            'blocked': blocked,
            'email': email,
            'full_name': full_name,
            'is_admin': is_admin,
            'password': 'password',
            'phone': phone
        }) 
    answer = json.dumps(list)    
    return answer


@app.route('/n_blockUser/<access_code>/<id>/')
def blockUser (access_code,id):
    import iz_func    
    import json
    db,cursor = iz_func.connect ()
    sql = "UPDATE n_users SET blocked = 'Заблокирован' WHERE `id` = '"+str(id)+"'"
    print ('[sql4] :',sql)
    cursor.execute(sql)
    db.commit()
    answer = 'Удален объект'
    return answer


@app.route('/n_addUset/<access_code>/<full_name>/<is_admin>/<password>/<phone>/<email>/') #### 4
def n_addUset (access_code,full_name,is_admin,password,phone,email):
    import iz_func    
    import json
    print ('[+] Добавление пользователей') 
    print ('[+] access_code:',access_code)
    print ('[+] full_name:',full_name)
    print ('[+] is_admin:',is_admin)
    print ('[+] password:',password)
    print ('[+] phone:',phone)
    print ('[+] email:',email)
    db,cursor = iz_func.connect ()
    full_name = full_name.encode('utf8')
    sql = "INSERT INTO n_users (`blocked`,`email`,`full_name`,`is_admin`,`password`,`phone`) VALUES ('{}','{}','{}','{}','{}','{}')".format('No',email.strip(),full_name.strip(),is_admin.strip(),password.strip(),phone.strip())
    print ('[sql5] :',sql)
    cursor.execute(sql)
    db.commit()
    lastid = cursor.lastrowid
    list = []
    list.append(lastid)
    #answer = "Отказано в доступе ..."
    return json.dumps(list)




@app.route('/n_update/<access_code>/<id>/<full_name>/<is_admin>/<password>/<phone>/<email>/') #### 5
def n_update (access_code,id,full_name,is_admin,password,phone,email):
    import iz_func    
    import json
    db,cursor = iz_func.connect ()
    list = []
    #sql = "select id,blocked,email,full_name,is_admin,password,phone from n_users where 1=1 "
    #cursor.execute(sql)
    #results2 = cursor.fetchall()        
    #for row2 in results2:    
    #    id,blocked,email,full_name,is_admin,password,phone = row2
    #    list.append ([id,region,region_kaz,rion,rion_kaz]) 
    #answer = json.dumps(list)    

    full_name = full_name.encode('utf8')
    sql = "UPDATE n_users SET full_name = '"+str(full_name).strip()+"' WHERE `id` = '"+str(id)+"'"
    cursor.execute(sql)
    db.commit()
    sql = "UPDATE n_users SET is_admin = '"+str(is_admin).strip()+"' WHERE `id` = '"+str(id)+"'"
    cursor.execute(sql)
    db.commit()
    sql = "UPDATE n_users SET password = '"+str(password).strip()+"' WHERE `id` = '"+str(id)+"'"
    cursor.execute(sql)
    db.commit()
    sql = "UPDATE n_users SET phone = '"+str(phone).strip()+"' WHERE `id` = '"+str(id)+"'"
    cursor.execute(sql)
    db.commit()
    sql = "UPDATE n_users SET email = '"+str(email).strip()+"' WHERE `id` = '"+str(id)+"'"
    cursor.execute(sql)
    db.commit()

    answer = "Обновлено"
    return answer







@app.route('/n_getBranchList/<access_code>/')
def n_getBranchList (access_code):
    import iz_func    
    import json
    db,cursor = iz_func.connect ()
    list = []
    # sql = "select id,answers_type,is_request,title,to_branch from n_branch where 1=1"
    sql = """SELECT b.id, b.for_all, b.title, b.is_request, b.answers_type, b.to_branch, 
          JSON_ARRAYAGG(JSON_OBJECT('id',a.id,'to_branch', a.to_branch,'content', a.content, 'tag_id',a.tag_id)) AS answers 
          FROM n_branch b 
          LEFT JOIN n_answers a ON  a.branch_id = b.id 
          GROUP BY b.id"""
    print (sql)
    cursor.execute(sql)
    results2 = cursor.fetchall()        
    for row2 in results2:    
        id,for_all,title,is_request,answers_type,to_branch,answers = row2
        list.append ({
            'id': id,
            'for_all': for_all,
            'title': title,
            'is_request': is_request,
            'answers_type': answers_type,
            'to_branch': to_branch,
            'answers': answers
        }) 
    answer = json.dumps(list)    
    #answer = "Отказано в доступе ..."
    return answer





@app.route('/n_getTemplateList/<access_code>/')
def n_getTemplateList (access_code):
    import iz_func    
    import json
    db,cursor = iz_func.connect ()
    list = []
    sql = "select id,title,to_branch from n_template where 1=1"
    print (sql)
    cursor.execute(sql)
    results2 = cursor.fetchall()        
    for row2 in results2:    
        id,title,to_branch = row2
        list.append ({
            'id': id,
            'title': title,
            'to_branch': to_branch
            }) 

    answer = json.dumps(list)    
    #answer = "Отказано в доступе ..."
    return answer



@app.route('/n_CreateTemplate/<access_code>/<title>/<to_branch>/')
def n_CreateTemplate (access_code,title,to_branch):
    import iz_func    
    import json
    db,cursor = iz_func.connect ()
    title = title.encode('utf8')
    sql = "INSERT INTO n_template (`title`,`to_branch`) VALUES ('{}','{}')".format(title.replace('*!*','/').replace('@!@','?'),to_branch)
    print ('[sql5] :',sql)
    cursor.execute(sql)
    db.commit()
    lastid = cursor.lastrowid
    list = []
    list.append(lastid)
    #answer = "Отказано в доступе ..."
    return json.dumps(list)

@app.route('/n_UpdateTemplate/<access_code>/<id>/<title>/<to_branch>/')
def n_UpdateTemplate (access_code,id,title,to_branch):
    import iz_func    
    import json
    db,cursor = iz_func.connect ()
    title = title.encode('utf8')
    sql = "UPDATE n_template SET title = '"+str(title).replace('*!*','/').replace('@!@','?')+"' WHERE `id` = '"+str(id)+"'"
    cursor.execute(sql)
    db.commit()
    sql = "UPDATE n_branch SET to_branch = '"+to_branch+"' WHERE `id` = '"+str(id)+"'"
    cursor.execute(sql)
    db.commit()

    branch = "Шаблон изменён"
    #answer = "Отказано в доступе ..."
    return branch

@app.route('/n_blockTemplate/<access_code>/<id>/')
def blockTemplate (access_code,id):
    import iz_func    
    import json
    db,cursor = iz_func.connect ()
    sql = "DELETE FROM n_template WHERE `id` = '"+str(id)+"' ORDER BY id LIMIT 1"
    print ('[sql4] :',sql)
    cursor.execute(sql)
    db.commit()
    answer = 'Удален объект'
    return answer












@app.route('/n_CreateBranch/<access_code>/<answers_type>/<is_request>/<title>/<to_branch>/<for_all>/')
def n_CreateBranch (access_code,answers_type,is_request,title,to_branch,for_all):
    import iz_func    
    import json
    db,cursor = iz_func.connect ()
    title = title.encode('utf8')
    is_request = is_request.encode('utf8')
    to_branch = to_branch.encode('utf8')
    for_all = for_all.encode('utf8')
    sql = "INSERT INTO n_branch (`answers_type`,`is_request`,`title`,`to_branch`,`for_all`) VALUES ('{}','{}','{}','{}','{}')".format (answers_type,is_request.replace('*!*','/').replace('@!@','?'),title.replace('*!*','/').replace('@!@','?'),to_branch,for_all)
    print ('[sql5] :',sql)
    cursor.execute(sql)
    db.commit()
    lastid = cursor.lastrowid
    list = []
    list.append(lastid)
    return json.dumps(list)


@app.route('/n_UpdateBranch/<access_code>/<id>/<answers_type>/<is_request>/<title>/<to_branch>/<for_all>/')
def n_UpdateBranch (access_code,id,answers_type,is_request,title,to_branch,for_all):
    import iz_func    
    import json
    db,cursor = iz_func.connect ()
    title = title.encode('utf8')
    is_request = is_request.encode('utf8')
    to_branch = to_branch.encode('utf8')
    for_all = for_all.encode('utf8')
    
    sql = "UPDATE n_branch SET answers_type = '"+str(answers_type)+"' WHERE `id` = '"+str(id)+"'"
    cursor.execute(sql)
    db.commit()
    sql = "UPDATE n_branch SET is_request = '"+is_request.replace('*!*','/').replace('@!@','?')+"' WHERE `id` = '"+str(id)+"'"
    cursor.execute(sql)
    db.commit()
    sql = "UPDATE n_branch SET title = '"+str(title).replace('*!*','/').replace('@!@','?')+"' WHERE `id` = '"+str(id)+"'"
    cursor.execute(sql)
    db.commit()
    sql = "UPDATE n_branch SET to_branch = '"+to_branch+"' WHERE `id` = '"+str(id)+"'"
    cursor.execute(sql)
    db.commit()
    sql = "UPDATE n_branch SET for_all = '"+for_all+"' WHERE `id` = '"+str(id)+"'"
    cursor.execute(sql)
    db.commit()

    answer = "Branch обновлён"
    #answer = "Отказано в доступе ..."
    return answer


@app.route('/n_CreateAnswer/<access_code>/<branch_id>/<content>/<tag_id>/<to_branch>/')
def n_CreateAnswer (access_code,branch_id,content,tag_id,to_branch):
    import iz_func    
    import json
    db,cursor = iz_func.connect ()
    content = content.encode('utf8')
    sql = "INSERT INTO n_answers (`branch_id`,`content`,`tag_id`,`to_branch`) VALUES ('{}','{}','{}','{}')".format(branch_id,content.replace('*!*','/').replace('@!@','?'),tag_id,to_branch)
    print ('[sql6] :',sql)
    cursor.execute(sql)
    db.commit()
    lastid = cursor.lastrowid
    list = []
    list.append(lastid)
    return json.dumps(list)

@app.route('/n_UpdateAnswer/<access_code>/<id>/<branch_id>/<content>/<tag_id>/<to_branch>/')
def n_UpdateAnswer (access_code,id,branch_id,content,tag_id,to_branch):
    import iz_func    
    import json
    db,cursor = iz_func.connect ()
    content = content.encode('utf8')
    
    sql = "UPDATE n_answers SET branch_id = '"+str(branch_id)+"' WHERE `id` = '"+str(id)+"'"
    cursor.execute(sql)
    db.commit()
    sql = "UPDATE n_answers SET content = '"+str(content).replace('*!*','/').replace('@!@','?')+"' WHERE `id` = '"+str(id)+"'"
    cursor.execute(sql)
    db.commit()
    sql = "UPDATE n_answers SET tag_id = '"+str(tag_id)+"' WHERE `id` = '"+str(id)+"'"
    cursor.execute(sql)
    db.commit()
    sql = "UPDATE n_answers SET to_branch = '"+to_branch+"' WHERE `id` = '"+str(id)+"'"
    cursor.execute(sql)
    db.commit()

    answer = "Ответ изменён"
    #answer = "Отказано в доступе ..."
    return answer


@app.route('/n_DeleteAnswer/<access_code>/<id>/')
def n_DeleteAnswer (access_code,id):
    import iz_func    
    import json
    db,cursor = iz_func.connect ()
    
    sql = "DELETE FROM n_answers WHERE `id` = '"+str(id)+"' ORDER BY id LIMIT 1"
    cursor.execute(sql)
    db.commit()

    answer = "Ответ удалён"
    #answer = "Отказано в доступе ..."
    return answer





@app.route('/n_createTag/<access_code>/<title>/')
def n_createTag (access_code,title):
    import iz_func    
    import json
    db,cursor = iz_func.connect ()
    #list = []
    #sql = "select id,title from n_tags where 1=1"
    #print (sql)
    #cursor.execute(sql)
    #results2 = cursor.fetchall()        
    #for row2 in results2:    
    #    id,title = row2
    #    list.append ([id,title]) 
    sql = "INSERT INTO n_tags (`title`) VALUES ('{}')".format(title)
    print ('[sql7] :',sql)
    cursor.execute(sql)
    db.commit()
    lastid = cursor.lastrowid
    answer = [lastid]
    #answer = "Отказано в доступе ..."
    return answer


@app.route('/n_tags/<access_code>/')
def n_tags (access_code):
    import iz_func    
    import json
    db,cursor = iz_func.connect ()
    list = []
    sql = "select id,title from n_tags where 1=1"
    print ('[sql8] :',sql)
    cursor.execute(sql)
    results2 = cursor.fetchall()        
    for row2 in results2:    
        id,title = row2
        list.append ([id,title]) 
    answer = json.dumps(list)    
    #answer = "Отказано в доступе ..."
    return answer





@app.route('/ClientsList/<access_code>/', methods=['POST'])
def myClientsList (access_code,user_id):
    import iz_func    
    import json
    db,cursor = iz_func.connect ()
    list = []
    request.form['sort_by']
    request.form['sort_type']
    request.form['from']
    request.form['tags']
    if(request.form['user_id'] != 0):
        sql = """SELECT id, from ,name,phone,user_id FROM n_clients 
            WHERE user_id = {} 
            LIMIT 7 OFFSET {}""".format(request.form['user_id'], request.form['page'])
    else
        sql = """SELECT id, from ,name,phone,user_id FROM n_clients 
            LIMIT 7 OFFSET {}""".format(request.form['page'])
    print ('[sql10] :',sql)
    cursor.execute(sql)
    results2 = cursor.fetchall()        
    for row2 in results2:    
        id,_from,name,phone,user_id = row2
        list.append ({
            'id':id,
            'from': _from,
            'name': name,
            'phone': phone,
            'user_id': user_id
            }) 
    answer = json.dumps(list)    
    return answer



@app.route('/update_changeManager/<access_code>/<id>/<user_id>/')
def update_changeManager (access_code,id,user_id):
    import iz_func    
    import json
    db,cursor = iz_func.connect ()

    sql = "UPDATE n_clients SET user_id = '"+str(user_id)+"' WHERE `id` = '"+str(id)+"'"
    print ('[sql11] :',sql)
    cursor.execute(sql)
    db.commit()

    #list = []
    #sql = "select id,from,name,phone,user_id from n_clients where 1=1"
    #print (sql)
    #cursor.execute(sql)
    #results2 = cursor.fetchall()        
    #for row2 in results2:    
    #    id,fromL,name,phone,user_id = row2
    #    list.append ([id,fromL,name,phone,user_id]) 
    answer = 'Изменено'    
    #answer = "Отказано в доступе ..."
    return answer








@app.route('/n_requests/<access_code>/', methods=['POST'])
def n_requests (access_code):
    import iz_func    
    import json
    db,cursor = iz_func.connect ()
    list = []
    
    if(request.form['checked'] != ''):
        sql = """SELECT r.id, r.date, r.status, r.checked, r.client_id, c.name, c.phone, c.from as from,
            JSON_OBJECT('id', u.id, 'full_name', u.full_name) as manager,
            JSON_ARRAYAGG(JSON_OBJECT('title', rc.title, 'value', rc.answer)) AS answers
            FROM n_requests r 
            LEFT JOIN n_request_content rc ON  rc.request_id = r.id
            JOIN n_clients c ON  c.id = r.client_id
            JOIN n_users u ON  u.id = c.user_id
            WHERE r.status = 1 
            AND r.checked= {} 
            AND (c.name LIKE '%{}%' OR c.phone LIKE '%{}%' OR u.full_name LIKE '%{}%')
            AND (r.date BETWEEN '{}' AND '{}')
            GROUP BY r.id
            LIMIT 7 OFFSET {}""".format(
                request.form['checked'],
                request.form['find'],
                request.form['find'],
                request.form['find'],
                request.form['date-start'],
                request.form['date-end'],
                request.form['page']
                )
    else:
        sql = """SELECT r.id, r.date, r.status, r.checked, r.client_id, c.name, c.phone, c.from as from,
            JSON_OBJECT('id', u.id, 'full_name', u.full_name) as manager,
            JSON_ARRAYAGG(JSON_OBJECT('title', rc.title, 'value', rc.answer)) AS answers
            FROM n_requests r 
            LEFT JOIN n_request_content rc ON  rc.request_id = r.id
            JOIN n_clients c ON  c.id = r.client_id
            JOIN n_users u ON  u.id = c.user_id
            WHERE r.status = 1 
            AND (c.name LIKE '%{}%' OR c.phone LIKE '%{}%' OR u.full_name LIKE '%{}%')
            AND (r.date BETWEEN '{}' AND '{}')
            GROUP BY r.id
            LIMIT 7 OFFSET {}""".format(
                request.form['find'],
                request.form['find'],
                request.form['find'],
                request.form['date-start'],
                request.form['date-end'],
                request.form['page']
                )
    print ('[sql12] :',sql)
    cursor.execute(sql)
    results2 = cursor.fetchall()        
    for row2 in results2:    
        id,date,status,checked,client_id,name,phone,_from,manager,answers = row2
        list.append ({
            'id': id,
            'date': date,
            'status': status,
            'checked': checked,
            'client_id': client_id,
            'name': name,
            'phone': phone,
            'from': _from,
            'manager': manager,
            'answers': answers
            }) 
            
    def myconverter(o):
        if isinstance(o, datetime.datetime):
            return o.__str__()
    
    answer = json.dumps(list, default = myconverter)    
    #answer = "Отказано в доступе ..."
    return json.dumps({'data': answer, 'pages': math.ceil(len(list) / 7)})








@app.route('/n_update_requestChecked/<access_code>/<id>/<checked>/')
def n_update_requestChecked (access_code,id,checked):
    import iz_func    
    import json
    db,cursor = iz_func.connect ()

    sql = "UPDATE n_requests SET checked = '"+str(checked)+"' WHERE `id` = '"+str(id)+"'"
    print ('[sql13] :',sql)
    cursor.execute(sql)
    db.commit()

    if(checked == 3):
        print('popal')
        
    answer = 'Изменено'    
    return answer

@app.route('/n_update_requestStatus/<access_code>/<id>/<status>/')
def n_update_requestStatus (access_code,id,status):
    import iz_func    
    import json
    db,cursor = iz_func.connect ()

    sql = "UPDATE n_requests SET status = '"+str(status)+"' WHERE `id` = '"+str(id)+"'"
    print ('[sql13] :',sql)
    cursor.execute(sql)
    db.commit()

    answer = 'Изменено'    
    return answer



@app.route('/n_messagesList/<access_code>/<sort_by>/<sort_type>/<limit>/<offset>/')
def n_messagesList (access_code,sort_by,sort_type,limit,offset):
    import iz_func    
    import json
    db,cursor = iz_func.connect ()
    list = []
    sql = "select id,content,user_id from n_messages where 1=1 ORDER BY "+str(sort_by)+" "+str(sort_type)+" limit "+str(limit)+" offset "+str(offset)+""
    print ('[sql14] :',sql)
    cursor.execute(sql)
    results2 = cursor.fetchall()        
    for row2 in results2:    
        id,content,user_id = row2
        list.append ([id,content,user_id]) 
    answer = json.dumps(list)    
    #answer = "Отказано в доступе ..."
    return answer

















if __name__ == '__main__':
    app.run(host='185.22.64.75',port=3143,debug=False)