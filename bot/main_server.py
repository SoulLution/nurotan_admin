#! /usr/bin/env python
# -*- coding: utf-8 -*-

import requests
import json
from flask import Flask
from flask_cors import CORS
from flask import request
import datetime
import math
app = Flask(__name__)
CORS(app)

# from importlib import reload
# import sys
# reload(sys)
# sys.setdefaultencoding('utf-8')



def send_requests(method, data):
    url = "https://eu188.chat-api.com/instance209738/{}?token=t76l2xhbiudrs3uv".format(method)
    headers = {'Content-type': 'application/json'}
    answer = requests.post(url, data=json.dumps(data), headers=headers)
    print(answer.json())
    return answer.json()

def send_message(chatID, text):
    data = {"chatId" : chatID,
            "body" : text}  
    answer = send_requests('sendMessage', data)
    print(answer)
    return answer



from bs4 import BeautifulSoup
def replaceText(text):
    return BeautifulSoup(text.replace('<p>','\n').replace('<br>','\n').replace('<strong>','*').replace('</strong>','*').replace('<em>','_').replace('</em>','_').strip(), "html.parser").get_text()
def replaceTextButton(text):
    return BeautifulSoup(text.strip(), "html.parser").get_text()
def replaceTextWP(text):
    return BeautifulSoup(text.replace('<br>','\n').replace('<strong>','*').replace('</strong>','*').replace('<em>','_').replace('</em>','_').strip(), "html.parser").get_text()

def addEmoji(numb):
    arr = [
        '0️⃣',
        '1️⃣',
        '2️⃣',
        '3️⃣',
        '4️⃣',
        '5️⃣',
        '6️⃣',
        '7️⃣',
        '8️⃣',
        '9️⃣'   
    ]
    return arr[int(numb)]

def spliceNameReference (value, id):
    return {id: value}


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



@app.route('/searchUser/<access_code>/', methods=['POST'])   ### 3
def searchUser (access_code):
    import iz_func    
    import json
    db,cursor = iz_func.connect ()
    list = []
    sql = """SELECT id, full_name 
            FROM n_users
            WHERE is_admin = 'No'
            AND blocked = 'No'
            AND (full_name LIKE '%{}%' OR phone LIKE '%{}%' OR email LIKE '%{}%')
    """.format(request.form['find'], request.form['find'], request.form['find'])
    cursor.execute(sql)
    results2 = cursor.fetchall()        
    for row2 in results2:    
        id,full_name = row2
        list.append ({
            'id': id,
            'full_name': full_name
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
    # full_name = full_name.encode('utf8')
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
    if is_admin == '0':
       is_admin = 'No' 
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
    sql = """SET SESSION group_concat_max_len = 1000000"""
    cursor.execute(sql)
    sql = """SELECT b.id, b.for_all, b.title, b.is_request, b.answers_type, b.to_branch, 
            CONCAT(
            '[',
                GROUP_CONCAT(
                    JSON_OBJECT('id',a.id,'to_branch', a.to_branch,'content', a.content,'position',a.position, 'documentolog_id',a.documentolog_id)
                    order by a.position
                ),
            ']'
            ) answers 
            FROM n_branch b 
            LEFT JOIN n_answers a ON  a.branch_id = b.id 
            GROUP BY b.id"""
        #   JSON_ARRAYAGG(JSON_OBJECT('id',a.id,'to_branch', a.to_branch,'content', a.content, 'tag_id',a.tag_id, 'position',a.position, 'documentolog_id',a.documentolog_id)) AS answers 
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
    # title = title.encode('utf8')
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
    # title = title.encode('utf8')
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
    # title = title.encode('utf8')
    # is_request = is_request.encode('utf8')
    # to_branch = to_branch.encode('utf8')
    # for_all = for_all.encode('utf8')
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
    # title = title.encode('utf8')
    # is_request = is_request.encode('utf8')
    # to_branch = to_branch.encode('utf8')
    # for_all = for_all.encode('utf8')
    
    sql = "UPDATE n_branch SET answers_type = '"+str(answers_type)+"' WHERE `id` = '"+str(id)+"'"
    cursor.execute(sql)
    db.commit()
    sql = "UPDATE n_branch SET is_request = '"+str(is_request).replace('*!*','/').replace('@!@','?')+"' WHERE `id` = '"+str(id)+"'"
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


@app.route('/n_CreateAnswer/<access_code>/<branch_id>/<content>/<tag_id>/<to_branch>/<position>/<documentolog_id>/')
def n_CreateAnswer (access_code,branch_id,content,tag_id,to_branch,position,documentolog_id):
    import iz_func    
    import json
    db,cursor = iz_func.connect ()
    # content = content.encode('utf8')
    if documentolog_id == 'null' :
        documentolog_id = ''
    sql = "INSERT INTO n_answers (`branch_id`,`content`,`tag_id`,`to_branch`, `position`, `documentolog_id`) VALUES ('{}','{}','{}','{}','{}','{}')".format(branch_id,content.replace('*!*','/').replace('@!@','?'),tag_id,to_branch,position,documentolog_id)
    print ('[sql6] :',sql)
    cursor.execute(sql)
    db.commit()
    lastid = cursor.lastrowid
    list = []
    list.append(lastid)
    return json.dumps(list)

@app.route('/n_UpdateAnswer/<access_code>/<id>/<branch_id>/<content>/<tag_id>/<to_branch>/<position>/<documentolog_id>/')
def n_UpdateAnswer (access_code,id,branch_id,content,tag_id,to_branch,position,documentolog_id):
    import iz_func    
    import json
    db,cursor = iz_func.connect ()
    # content = content.encode('utf8')
    
    sql = "UPDATE n_answers SET branch_id = '"+str(branch_id)+"' WHERE `id` = '"+str(id)+"'"
    cursor.execute(sql)
    db.commit()
    sql = "UPDATE n_answers SET content = '"+content.replace('*!*','/').replace('@!@','?')+"' WHERE `id` = '"+str(id)+"'"
    cursor.execute(sql)
    db.commit()
    sql = "UPDATE n_answers SET tag_id = '"+str(tag_id)+"' WHERE `id` = '"+str(id)+"'"
    cursor.execute(sql)
    db.commit()
    sql = "UPDATE n_answers SET to_branch = '"+to_branch+"' WHERE `id` = '"+str(id)+"'"
    cursor.execute(sql)
    db.commit()
    sql = "UPDATE n_answers SET position = '"+position+"' WHERE `id` = '"+str(id)+"'"
    cursor.execute(sql)
    db.commit()
    if documentolog_id == 'null' :
        documentolog_id = ''
    sql = "UPDATE n_answers SET documentolog_id = '"+documentolog_id+"' WHERE `id` = '"+str(id)+"'"
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





@app.route('/Client/<access_code>/<client_id>/')
def Client (access_code, client_id):
    import iz_func    
    import json
    db,cursor = iz_func.connect ()
    list = []
    sql = """SELECT c.id, c.name, c.phone, c.from,
            JSON_ARRAYAGG(JSON_OBJECT('content', m.content, 'date', m.date)) AS messages
            FROM n_clients c
            JOIN n_messages m ON (m.user_id = c.id AND m.from = 'client')
            WHERE c.id = {}
            GROUP BY c.id
            LIMIT 1
            """.format(client_id)
    cursor.execute(sql)
    results2 = cursor.fetchall()        
    for row2 in results2:    
        id,name,phone,_from,messages = row2
        list.append ({
            'id':id,
            'from': _from,
            'name': name,
            'phone': phone,
            'messages': messages
            }) 
    answer = json.dumps(list)    
    return answer


@app.route('/ClientsList/<access_code>/', methods=['POST'])
def ClientsList (access_code):
    import iz_func    
    import json
    db,cursor = iz_func.connect ()
    list = []
    _from = "tg' OR c.from = 'wp"
    if request.form['from'] :
        _from = request.form['from']
    sql = {}
    if request.form['user_id'] != '0' :
        sql = """SELECT c.id, c.name, c.phone, c.from,
                JSON_OBJECT('id', u.id, 'full_name', u.full_name) as manager,
                JSON_ARRAYAGG(JSON_OBJECT('content', m.content, 'date', m.date)) AS messages
                FROM n_clients c
                JOIN n_messages m ON (m.user_id = c.id AND m.from = 'client')
                JOIN n_users u on u.id = c.user_id
                WHERE c.user_id = {}
                AND (c.name LIKE '%{}%' OR c.phone LIKE '%{}%')
                AND (c.from = '{}')
                GROUP BY c.id
                LIMIT 7 OFFSET {}
                """.format(request.form['user_id'],request.form['find'], request.form['find'], _from, request.form['page'])
    else :
        sql = """SELECT c.id, c.name, c.phone, c.from,
                JSON_OBJECT('id', u.id, 'full_name', u.full_name) as manager,
                JSON_ARRAYAGG(JSON_OBJECT('content', m.content, 'date', m.date)) AS messages
                FROM n_clients c
                JOIN n_messages m ON (m.user_id = c.id AND m.from = 'client')
                JOIN n_users u on u.id = c.user_id
                WHERE (c.from = '{}')
                AND (c.name LIKE '%{}%' OR c.phone LIKE '%{}%')
                GROUP BY c.id
                LIMIT 7 OFFSET {}
                """.format(_from,request.form['find'], request.form['find'], request.form['page'])
    print ('[sql10] :',sql)
    cursor.execute(sql)
    results = cursor.fetchall()
    if request.form['user_id'] != '0' :
        sql = """SELECT c.id, c.name, c.phone, c.from,
                JSON_OBJECT('id', u.id, 'full_name', u.full_name) as manager,
                JSON_ARRAYAGG(JSON_OBJECT('content', m.content, 'date', m.date)) AS messages
                FROM n_clients c
                JOIN n_messages m ON (m.user_id = c.id AND m.from = 'client')
                JOIN n_users u on u.id = c.user_id
                WHERE c.user_id = {}
                AND (c.name LIKE '%{}%' OR c.phone LIKE '%{}%')
                AND (c.from = '{}')
                GROUP BY c.id
                """.format(request.form['user_id'],request.form['find'], request.form['find'], _from)
    else :
        sql = """SELECT c.id, c.name, c.phone, c.from,
                JSON_OBJECT('id', u.id, 'full_name', u.full_name) as manager,
                JSON_ARRAYAGG(JSON_OBJECT('content', m.content, 'date', m.date)) AS messages
                FROM n_clients c
                JOIN n_messages m ON (m.user_id = c.id AND m.from = 'client')
                JOIN n_users u on u.id = c.user_id
                WHERE (c.from = '{}')
                AND (c.name LIKE '%{}%' OR c.phone LIKE '%{}%')
                GROUP BY c.id
                """.format(_from,request.form['find'], request.form['find'])
    print ('[sql10] :',sql)    
    cursor.execute(sql)
    results2 = cursor.fetchall()     
    for row in results:    
        id,name,phone,_from,manager,messages = row
        list.append ({
            'id':id,
            'from': _from,
            'name': name,
            'phone': phone,
            'manager': manager,
            'messages': messages
            })    

    answer = json.dumps(list)    
    return json.dumps({'data': answer, 'pages': math.ceil(len(results2) / 7)})



@app.route('/update_changeManager/<access_code>/<id>/<user_id>/')
def update_changeManager (access_code,id,user_id):
    import iz_func    
    import json
    db,cursor = iz_func.connect ()

    sql = "UPDATE n_clients SET user_id = '"+str(user_id)+"' WHERE id = '"+str(id)+"'"
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
        sql = """SELECT r.id, r.date, r.status, r.checked, r.client_id, c.name, c.phone, c.from as _from,
            JSON_OBJECT('id', u.id, 'full_name', u.full_name) as manager,
            JSON_ARRAYAGG(JSON_OBJECT('title', rc.title, 'value', rc.answer, 'documentolog_id', rc.documentolog_id)) AS answers
            FROM n_requests r 
            LEFT JOIN n_request_content rc ON  rc.request_id = r.id
            JOIN n_clients c ON  c.id = r.client_id
            JOIN n_users u ON  u.id = c.user_id
            WHERE r.status = 1 
            AND r.checked= {} 
            AND (c.name LIKE '%{}%' OR c.phone LIKE '%{}%' OR u.full_name LIKE '%{}%')
            AND (r.date BETWEEN '{}' AND '{}')
            GROUP BY r.id
            ORDER BY r.id DESC
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
        sql = """SELECT r.id, r.date, r.status, r.checked, r.client_id, c.name, c.phone, c.from as _from,
            JSON_OBJECT('id', u.id, 'full_name', u.full_name) as manager,
            JSON_ARRAYAGG(JSON_OBJECT('title', rc.title, 'value', rc.answer, 'documentolog_id', rc.documentolog_id)) AS answers
            FROM n_requests r 
            LEFT JOIN n_request_content rc ON  rc.request_id = r.id
            JOIN n_clients c ON  c.id = r.client_id
            JOIN n_users u ON  u.id = c.user_id
            WHERE r.status = 1 
            AND (c.name LIKE '%{}%' OR c.phone LIKE '%{}%' OR u.full_name LIKE '%{}%')
            AND (r.date BETWEEN '{}' AND '{}')
            GROUP BY r.id
            ORDER BY r.id DESC
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
    
    
    if(request.form['checked'] != ''):
        sql = """SELECT r.id, r.date, r.status, r.checked, r.client_id, c.name, c.phone, c.from as _from,
            JSON_OBJECT('id', u.id, 'full_name', u.full_name) as manager,
            JSON_ARRAYAGG(JSON_OBJECT('title', rc.title, 'value', rc.answer, 'documentolog_id', rc.documentolog_id)) AS answers
            FROM n_requests r 
            LEFT JOIN n_request_content rc ON  rc.request_id = r.id
            JOIN n_clients c ON  c.id = r.client_id
            JOIN n_users u ON  u.id = c.user_id
            WHERE r.status = 1 
            AND r.checked= {} 
            AND (c.name LIKE '%{}%' OR c.phone LIKE '%{}%' OR u.full_name LIKE '%{}%')
            AND (r.date BETWEEN '{}' AND '{}')
            GROUP BY r.id""".format(
                request.form['checked'],
                request.form['find'],
                request.form['find'],
                request.form['find'],
                request.form['date-start'],
                request.form['date-end']
                )
    else:
        sql = """SELECT r.id, r.date, r.status, r.checked, r.client_id, c.name, c.phone, c.from as _from,
            JSON_OBJECT('id', u.id, 'full_name', u.full_name) as manager,
            JSON_ARRAYAGG(JSON_OBJECT('title', rc.title, 'value', rc.answer, 'documentolog_id', rc.documentolog_id)) AS answers
            FROM n_requests r 
            LEFT JOIN n_request_content rc ON  rc.request_id = r.id
            JOIN n_clients c ON  c.id = r.client_id
            JOIN n_users u ON  u.id = c.user_id
            WHERE r.status = 1 
            AND (c.name LIKE '%{}%' OR c.phone LIKE '%{}%' OR u.full_name LIKE '%{}%')
            AND (r.date BETWEEN '{}' AND '{}')
            GROUP BY r.id""".format(
                request.form['find'],
                request.form['find'],
                request.form['find'],
                request.form['date-start'],
                request.form['date-end']
                )
    cursor.execute(sql)
    results2 = cursor.fetchall() 

    def myconverter(o):
        if isinstance(o, datetime.datetime):
            return o.__str__()
    
    answer = json.dumps(list, default = myconverter)    
    #answer = "Отказано в доступе ..."
    return json.dumps({'data': answer, 'pages': math.ceil(len(results2) / 7)})








@app.route('/n_update_requestChecked/<access_code>/<id>/<checked>/', methods=['POST'])
def n_update_requestChecked (access_code,id,checked):
    import iz_func    
    import json
    db,cursor = iz_func.connect ()

    
    if(checked == '3'): 
        sql = """SELECT JSON_ARRAYAGG(JSON_OBJECT(0, rc.title, 1, rc.answer, 2, rc.documentolog_id)) AS content
                FROM n_requests r
                JOIN n_request_content rc ON rc.request_id = r.id
                WHERE r.id = '{}'
                GROUP BY r.id
                LIMIT 1""".format(id)
        cursor.execute(sql)
        results = cursor.fetchall() 
        content = json.loads(results[0][0])
        data = {
            'Адрес': '',
            'ФИО': '',
            'Регион': '',
            'Характер вопроса': '',
            'Возраст': '',
            'Вопрос': '',
            'Телефон': '',
            'Район': '',
            'Пол': '',
            'rajoni_gorodov': '',
            'Статус обращающегося': '',
            'Тип вопроса': '',
            'Язык': '',
            'Район города': '',
            'Актуальные вопросы': ''
        }
        for item in content:
            if item['2']:
                data[item['0']] = {item['2']: item['1']}
            else:
                data[item['0']] = item['1']
            if item['0'] == 'Район' :
                sql = """INSERT INTO korrespondenty (korrespondenty_id, district_id)
                        VALUES ('{}', '{}')
                        """.format(request.form['korrespondenty_id'], item['2'])
                cursor.execute(sql)
                db.commit()

        sql = """SELECT c.from 
                FROM n_requests r
                JOIN n_clients c ON  c.id = r.client_id
                WHERE r.id = {}
                LIMIT 1;""".format(id)
        cursor.execute(sql)
        results = cursor.fetchall() 
        if results[0][0] == 'tg':
            _from = {'key': '38351f92-8e30-4172-bf3d-5c023319035e', 'value': 'Telegram'}
        else :
            _from = {'key': '23ca40bc-6c67-4478-a5fd-5c023312007c', 'value': 'Whatsapp'}
        
        data = {
            'dom': data['Адрес'].split(' ')[1] if len(data['Адрес'].split(' ')) >= 2 else None,
            'familiya': data['ФИО'].split(' ')[1] if len(data['ФИО'].split(' ')) >= 2 else None,
            'gorod': None,
            'harakter_voprosa': data['Характер вопроса'] or None,
            'imya': data['ФИО'].split(' ')[0] if len(data['ФИО'].split(' ')) >= 1 else None,
            'kategoriya_vozrasta': data['Возраст'] or None,
            'komu': {request.form['korrespondenty_id']: request.form['korrespondent']},
            'kratkoe_soderzhanie': data['Вопрос'] or None,
            'kvartira': data['Адрес'].split(' ')[2] if len(data['Адрес'].split(' ')) >= 3 else None,
            'mobilnij_telefon':  data['Телефон'] or None,
            'oblast': data['Район'] or None,
            'rajoni_gorodov': data['Район города'] or None,
            'otchestvo': data['ФИО'].split(' ')[2] if len(data['ФИО'].split(' ')) >= 3 else None,
            'pol': data['Пол'] or None,
            'region': data['Регион'] or None,
            'status_obrativshegosya_litsa': data['Статус обращающегося'] or None,
            'tematika_voprosa': data['Тип вопроса'] or None,
            'trebuet_otveta': {'1': 'Да'} if data['Статус обращающегося'] else {'2': 'Нет'},
            'ulitsa': data['Адрес'].split(' ')[0] if len(data['Адрес'].split(' ')) >= 1 else None,
            'vlozheniya': [],
            'yazik_dokumenta': data['Язык'] or None,
            'whatsapp_telegram': _from['value'],
            'istochnik_obrasheniya': {_from['key']: _from['value']},
            'aktualnie_voprosi_ozekti_syraktar': data['Актуальные вопросы'] or None
        }    
        print(json.dumps(data))
        import requests
        from requests.auth import HTTPBasicAuth
        response = requests.post('https://doc.nurotan.kz/webservice/json/82be1ae3-5131-47ab-ae04-5fcc8a8a0161',
        auth=HTTPBasicAuth('Chatbot', "5+xcsV!r*;%aR5GY9F44"),
        data=json.dumps(data))
        print(response.content)
        print(str(response.content).split('950fff8d-b9a4-4920-8fff-5285deb002c8:')[1].split('":"')[0])
        sql = "UPDATE n_requests SET documentolog_id = '"+str(response.content).split('950fff8d-b9a4-4920-8fff-5285deb002c8:')[1].split('":"')[0]+"' WHERE `id` = '"+id+"'"
        print ('[sql13] :',sql)
        cursor.execute(sql)
        db.commit()
        
    sql = "UPDATE n_requests SET checked = '"+str(checked)+"' WHERE `id` = '"+str(id)+"'"
    print ('[sql13] :',sql)
    cursor.execute(sql)
    db.commit()

        
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



@app.route('/n_messagesList/<access_code>/', methods=['POST'])
def n_messagesList (access_code):
    import iz_func    
    import json
    db,cursor = iz_func.connect ()
    list = []
    sql = {}

    if request.form['last'] == '0' :
        sql = """SELECT id, content, m.date, m.from 
                FROM n_messages m
                WHERE m.user_id = {}
                ORDER BY m.id DESC
                LIMIT 20 OFFSET {}
        """.format(request.form['user_id'], request.form['page'])
    else :
        sql = """SELECT id, content, m.date, m.from 
                FROM n_messages m
                WHERE m.user_id = {}
                AND m.id > {}
        """.format(request.form['user_id'], request.form['last'])

    cursor.execute(sql)
    results = cursor.fetchall()        
    for row2 in results:    
        id,content,date,_from = row2
        if _from == 'client' :
            sql = """SELECT c.id, c.name, c.phone
                    FROM n_clients c
                    WHERE c.id = {}
                    LIMIT 1
            """.format(request.form['user_id'])
            cursor.execute(sql)
            results2 = cursor.fetchall() 
            list.append ({
                'id': id,
                'content': content,
                'date': date,
                'from': _from,
                'user': {
                    'id': results2[0][0],
                    'name': results2[0][1],
                    'phone': results2[0][2],
                }
            })
        elif _from != 'bot' :
            sql = """SELECT u.id, u.full_name
                    FROM n_users u
                    WHERE u.id = {}
                    LIMIT 1
            """.format(_from)
            cursor.execute(sql)
            results2 = cursor.fetchall() 
            list.append ({
                'id': id,
                'content': content,
                'date': date,
                'from': _from,
                'user': {
                    'id': results2[0][0],
                    'name': results2[0][1],
                }
            })
        else :
            list.append ({
                'id': id,
                'content': content,
                'date': date,
                'from': _from,
                'user': {
                    'id': 0,
                    'name': 'bot',
                }
            }) 
    def myconverter(o):
        if isinstance(o, datetime.datetime):
            return o.__str__()
    
    answer = json.dumps(list, default = myconverter)    
    #answer = "Отказано в доступе ..."
    return answer



@app.route('/sendMessage/<access_code>/', methods=['POST'])
def sendMessage (access_code):
    import iz_func    
    import json
    # from bot import botSendMessage

    db,cursor = iz_func.connect ()
    list = []
    sql = "SELECT c.messanger_id, c.from FROM n_clients c WHERE id = '{}' LIMIT 1".format(request.form['user_id'])
    cursor.execute(sql)
    results = cursor.fetchall()
    
    if results[0][1] == 'tg' :
        import telebot
        token = '1393957889:AAEy0SgED_mt0zooGfgsrUHsQvkoC_7THz0'
        bot   = telebot.TeleBot(token)
        bot.send_message(results[0][0], request.form['message'], parse_mode='Markdown')
    else :
        send_message(results[0][0], request.form['message'])
    
    sql = "INSERT INTO n_messages (`content`,`user_id`,`from`) VALUES ('{}', '{}', '{}')".format(request.form['message'], request.form['user_id'], request.form['from'])
    cursor.execute(sql)
    db.commit()

    answer = "Сообщение отправленно"
    return answer


@app.route('/lastBranches/<access_code>/', methods=['POST'])
def lastBranches (access_code):
    import iz_func    
    import json
    db,cursor = iz_func.connect ()
    list = []
    sql = """SELECT r.id,
            JSON_ARRAYAGG(JSON_OBJECT('branch_id', rc.branch_id, 'title', rc.title)) AS content
            FROM n_requests r
            JOIN n_request_content rc ON rc.request_id = r.id
            WHERE client_id = '{}'
            GROUP BY r.id
            ORDER BY r.id DESC 
            LIMIT 1""".format(request.form['client_id'])
    cursor.execute(sql)
    results = cursor.fetchall()      
    for row in results:    
        id,content = row
        list.append ({
            'id':id,
            'content': content
            }) 
    answer = json.dumps(list)    
    return answer

@app.route('/changeBranch/<access_code>/', methods=['POST'])
def changeBranch (access_code):
    import iz_func    
    import json
    db,cursor = iz_func.connect ()

    sql = "SELECT id FROM n_requests WHERE client_id = '{}' ORDER BY id DESC LIMIT 1".format(request.form['client_id'])
    cursor.execute(sql)
    results = cursor.fetchall()
    sql = "UPDATE n_requests SET status = 0 WHERE `id` = '"+str(results[0][0])+"'"
    cursor.execute(sql)
    db.commit()
    sql = "UPDATE n_clients SET branch_id = {} WHERE `id` = {}".format(request.form['to_branch'], request.form['client_id'])
    cursor.execute(sql)
    db.commit()
    sql = """SET SESSION group_concat_max_len = 1000000"""
    cursor.execute(sql)
    
    sql = """SELECT b.id, b.title, b.answers_type,
        CONCAT(
        '[',
            GROUP_CONCAT(
                JSON_OBJECT('id', a.id, 'content', a.content)
                order by a.position
            ),
        ']'
        ) answers,
        b.is_request
        FROM n_branch b
        LEFT JOIN n_answers a ON  a.branch_id = b.id
        WHERE b.id = {}
        GROUP BY b.id
        LIMIT 1""".format(request.form['to_branch'])
    cursor.execute(sql)
    results2 = cursor.fetchall()     
    item = {
        'id': results2[0][0],
        'title': results2[0][1],
        'answers_type': results2[0][2],
        'answers': json.loads(results2[0][3]),
        'is_request': results2[0][4]
    }
    sql = "SELECT c.messanger_id, c.from FROM n_clients c WHERE id = '{}' LIMIT 1".format(request.form['client_id'])
    cursor.execute(sql)
    results = cursor.fetchall()
    if results[0][1] == 'tg' :
        import telebot
        from telebot import types
        token = '1393957889:AAEy0SgED_mt0zooGfgsrUHsQvkoC_7THz0'
        bot   = telebot.TeleBot(token)
        if item['answers_type'] == '0' :
            markup = types.InlineKeyboardMarkup(row_width=2)
            for answer in item['answers']:    
                markup_item = types.InlineKeyboardButton(text=replaceTextButton(answer['content']), callback_data=(answer['id']))
                markup.add(markup_item)
            bot.send_message(results[0][0], replaceText(item['title']), parse_mode='Markdown', reply_markup=markup)
            sql = "INSERT INTO n_messages (`content`,`from`,`user_id`) VALUES ('{}', 'bot', '{}')".format(item['title'],request.form['client_id'])
            cursor.execute(sql)
            db.commit()
        elif item['answers_type'] == '1' :
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            for answer in item['answers']:    
                markup_item = types.KeyboardButton(text=replaceTextButton(answer['content']))
                markup.add(markup_item)
            bot.send_message(results[0][0], replaceText(item['title']), parse_mode='Markdown', reply_markup=markup)
            sql = "INSERT INTO n_messages (`content`,`from`,`user_id`) VALUES ('{}', 'bot', '{}')".format(item['title'],request.form['client_id'])
            cursor.execute(sql)
            db.commit()
        else :
            bot.send_message(results[0][0], replaceText(item['title']), parse_mode='Markdown')
            sql = "INSERT INTO n_messages (`content`,`from`,`user_id`) VALUES ('{}', 'bot', '{}')".format(item['title'],request.form['client_id'])
            cursor.execute(sql)
            db.commit()
    else :
        if item['answers_type'] != '2' :
            i = 1
            for answer in item['answers']:  
                item['title'] += '\n'
                for j in str(i):    
                    item['title'] += addEmoji(j)
                item['title'] += replaceTextWP(answer['content'])
                i += 1
            sql = "INSERT INTO n_messages (`content`,`from`,`user_id`) VALUES ('{}', 'bot', '{}')".format(item['title'], request.form['client_id'])
            cursor.execute(sql)
            db.commit()
            send_message(results[0][0], replaceText(item['title']))
        else :
            sql = "INSERT INTO n_messages (`content`,`from`,`user_id`) VALUES ('{}', 'bot', '{}')".format(item['title'], request.form['client_id'])
            cursor.execute(sql)
            db.commit()
            send_message(results[0][0], replaceText(item['title']))


    answer = "Шаг изменён"
    return answer




@app.route('/KorrespondentyFields/<access_code>/<id>/')
def KorrespondentyFields (access_code, id):
    import iz_func    
    db,cursor = iz_func.connect ()

    import requests
    from requests.auth import HTTPBasicAuth
    response = requests.get("https://doc.nurotan.kz/webservice/json/chat_bot_spisok_korrespondenty",
    auth=HTTPBasicAuth("korrespondenty", "76M#;p&x6-gZxH5A7~Jg"))
    answer = response.json()["data"]["fields"]
    sql = """SELECT korrespondenty_id, COUNT(*) as len 
            FROM korrespondenty WHERE district_id = '{}' 
            GROUP BY korrespondenty_id ORDER BY len LIMIT 1;""".format(id)
    print(sql)
    cursor.execute(sql)
    results = cursor.fetchall()

    if results and len(results):
        return json.dumps({'fields': answer, 'current': results[0][0]})
    else:
        return json.dumps({'fields': answer, 'current': 0})


@app.route('/documentolog/message/<id>/', methods=['POST'])
def DocumentologMessage (id):
    import iz_func    
    import json
    db,cursor = iz_func.connect ()
    form = request.get_json()

    sql = """SELECT c.messanger_id, c.from, c.id FROM n_requests r
            JOIN n_clients c ON c.id = r.client_id
            WHERE r.documentolog_id = '{}' ORDER BY r.id DESC LIMIT 1""".format(id)
    cursor.execute(sql)
    results = cursor.fetchall()

    sql = "INSERT INTO n_messages (`content`,`from`,`user_id`) VALUES (%s, 'bot', '{}')".format(results[0][2])
    cursor.execute(sql, (form['message']))
    db.commit()

    if len(results) == 0:
        response = app.response_class(
            response=json.dumps({'status': 400, 'message': 'No find request with this id'}),
            status=400,
            mimetype='application/json'
        )
        return response
    if results[0][1] == 'tg' :
        import telebot
        token = '1393957889:AAEy0SgED_mt0zooGfgsrUHsQvkoC_7THz0'
        bot   = telebot.TeleBot(token)
        bot.send_message(results[0][0], form['message'], parse_mode='Markdown')
    else :
        send_message(results[0][0], form['message'])

    response = app.response_class(
        response=json.dumps({'status': 200, 'message': "successful"}),
        status=200,
        mimetype='application/json'
    )
    return response


@app.route('/documentolog/changeStatus/', methods=['POST'])
def DocumentoloChangeStatus ():
    import iz_func    
    import json
    db,cursor = iz_func.connect()
    form = request.get_json()

    sql = """SELECT c.messanger_id, c.from, c.id FROM n_requests r
            JOIN n_clients c ON c.id = r.client_id
            WHERE r.documentolog_id = '{}' ORDER BY r.id DESC LIMIT 1""".format(form["docid_chat_bot"])
    cursor.execute(sql)
    results = cursor.fetchall()
    if len(results) == 0:
        response = app.response_class(
            response=json.dumps({'status': 400, 'message': 'No find request with this id'}),
            status=400,
            mimetype='application/json'
        )
        return response
    
    print(form)
    message = "Уведомление\n"
    if str(form.get("na_kakoj_tochke")) == "1":
        message = message + "Ваша заявка доставленна: " + form.get("data_formirovaniya_uvedomleniya")
    elif str(form.get("na_kakoj_tochke")) == "2":
        message = message + "Регистрационный №: " + form.get("regnum") + "\n"
        message = message + "Дата/Время регистрации: " + form.get("regdate")
    elif str(form.get("na_kakoj_tochke")) == "3":
        message = message + "Исполнитель: " + form.get("otvet_ispolnitel__stroka") + "\n"
        message = message + "Телефон исполнителя: " + form.get("telefon_otvet_ispolnitelya")
    elif str(form.get("na_kakoj_tochke")) == "4":
        message = message + replaceTextButton(form.get("tekst_ispolneniya")[0].get("value")) + "\n"
        message = message + "Фактический срок исполнения: " + form.get("fak_srok_isp")
    # elif str(form.get("na_kakoj_tochke")) == "5":
    #     message = message + "Смена исполнителя\n"
    #     message = message + "Исполнитель: " + form.get("ispolnitel") + "\n"
    #     message = message + "Телефон исполнителя: " + form.get("phone_ispolnitel")
    elif str(form.get("na_kakoj_tochke")) == "5":
        message = message + "Отказ в регистрации: " + form.get("otkazano_vremya") + "\n"
        if form.get("prichina") :
            message = message + "Причина: " + "".join(form.get("prichina").get(str(i),"") for i in range(5) if data.get(str(i))) + "\n"
        message = message + form.get("opisanie_prichini")

    sql = "INSERT INTO n_messages (`content`,`from`,`user_id`) VALUES (%s, 'bot', '{}')".format(results[0][2])
    print(sql)
    cursor.execute(sql, (message))
    db.commit()

    if results[0][1] == 'tg' :
        import telebot
        token = '1393957889:AAEy0SgED_mt0zooGfgsrUHsQvkoC_7THz0'
        bot   = telebot.TeleBot(token)
        bot.send_message(results[0][0], message, parse_mode='Markdown')
    else :
        send_message(results[0][0], message)
        
    # return json.dumps({'status': 200, 'message': "successful"})
    response = app.response_class(
        response=json.dumps({'status': 200, 'message': "successful"}),
        status=200,
        mimetype='application/json'
    )
    return response


@app.route('/documentolog/changeStatus/', methods=['GET'])
def DocumentoloChangeStatusGET ():
    return json.dumps({
"status": 1,
"data": {
"title": "Otpravka_uvedomleni",
"description": "",
"fields": {
"regdate": {
"type": "date",
"title": "Регистрационная дата"
},
"regnum": {
"type": "string",
"title": "Регистрационный номер"
},
"fak_srok_isp": {
"type": "date",
"title": "Фактический срок исполнения"
},
"docid_chat_bot": {
"type": "string",
"title": "DOCID chat_bot"
},
"telefon_otvet_ispolnitelya": {
"type": "string",
"title": "Телефон ответ. исполнителя"
},
"tekst_ispolneniya": {
"type": "text",
"title": "Текст исполнения"
},
"otvet_ispolnitel__stroka": {
"type": "string",
"title": "Ответ. исполнитель - строка"
},
"otkazano_vremya": {
"type": "timestamp",
"title": "Отказано (время)"
},
"prichina": {
"type": "enumeration",
"title": "Причина"
},
"opisanie_prichini": {
"type": "string",
"title": "Описание причины"
},
"data_formirovaniya_uvedomleniya": {
"type": "date",
"title": "Дата формирования уведомления"
},
"uvedomleniya_v_chat_bot": {
"type": "string",
"title": "Уведомления в Chat_bot"
},
"na_kakoj_tochke": {
"type": "string",
"title": "На какой точке"
}
}
}
})

if __name__ == '__main__':
    app.run(host='185.22.64.75',port=3143,debug=False)