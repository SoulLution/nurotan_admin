#! /usr/bin/env python
# -*- coding: utf-8 -*-

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


from bs4 import BeautifulSoup
def replaceText(text):
    return BeautifulSoup(text.replace('<p>','\n').replace('<br>','\n').replace('<strong>','*').replace('</strong>','*').replace('<em>','_').replace('</em>','_').strip(), "html.parser").get_text()
def replaceTextButton(text):
    return BeautifulSoup(text.strip(), "html.parser").get_text()

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
    #sql = "select id,blocked,email,full_name,is_admin,password,phone from n_users where 1=1 "
    #cursor.execute(sql)
    #results2 = cursor.fetchall()        
    #for row2 in results2:    
    #    id,blocked,email,full_name,is_admin,password,phone = row2
    #    list.append ([id,region,region_kaz,rion,rion_kaz]) 
    #answer = json.dumps(list)    

    # full_name = full_name.encode('utf8')
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


@app.route('/n_CreateAnswer/<access_code>/<branch_id>/<content>/<tag_id>/<to_branch>/')
def n_CreateAnswer (access_code,branch_id,content,tag_id,to_branch):
    import iz_func    
    import json
    db,cursor = iz_func.connect ()
    # content = content.encode('utf8')
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
    _from = "'tg' OR c.from = 'wp'"
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
                AND (c.from = {})
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
                WHERE (c.from = {})
                AND (c.name LIKE '%{}%' OR c.phone LIKE '%{}%')
                GROUP BY c.id
                LIMIT 7 OFFSET {}
                """.format(_from,request.form['find'], request.form['find'], request.form['page'])

    print ('[sql10] :',sql)
    cursor.execute(sql)
    results2 = cursor.fetchall()        
    for row2 in results2:    
        id,name,phone,_from,manager,messages = row2
        list.append ({
            'id':id,
            'from': _from,
            'name': name,
            'phone': phone,
            'manager': manager,
            'messages': messages
            }) 
    answer = json.dumps(list)    
    return answer



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
        sql = """SELECT r.id, r.date, r.status, r.checked, r.client_id, c.name, c.phone, c.from as _from,
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

    
    if(checked == '3'): 
        sql = """SELECT JSON_ARRAYAGG(JSON_OBJECT(0, rc.title, 1, rc.answer)) AS content
                FROM n_requests r
                JOIN n_request_content rc ON rc.request_id = r.id
                WHERE r.id = '{}'
                GROUP BY r.id
                LIMIT 1""".format(id)
        cursor.execute(sql)
        results = cursor.fetchall() 
        content = json.loads(results[0][0])
        data = {}
        for item in content:
            data[item['0']] = item['1']
        data = {
            'dom': data['Адрес'].split(' ')[1] if len(data['Адрес'].split(' ')) >= 2 else '-',
            'familiya': data['ФИО'].split(' ')[1] if len(data['ФИО'].split(' ')) >= 2 else '-',
            'gorod': data['Регион'] or '-',
            'harakter_voprosa': data['Характер вопроса'] or '-',
            'imya': data['ФИО'].split(' ')[0] if len(data['ФИО'].split(' ')) >= 1 else '-',
            'kategoriya_vozrasta': data['Возраст'] or '-',
            'komu': '-',
            'kratkoe_soderzhanie': data['Вопрос'] or '-',
            'kvartira': data['Адрес'].split(' ')[2] if len(data['Адрес'].split(' ')) >= 3 else '-',
            'mobilnij_telefon':  data['Телефон'] or '-',
            'oblast': data['Район'] or '-',
            'otchestvo': data['ФИО'].split(' ')[2] if len(data['ФИО'].split(' ')) >= 3 else '-',
            'pol': data['Пол'] or '-',
            'region': data['Регион'] or '-',
            'status_obrativshegosya_litsa': data['Статус обращающегося'] or '-',
            'tematika_voprosa': data['Тип вопроса'] or '-',
            'trebuet_otveta': 'Да' if data['Статус обращающегося'] else 'Нет',
            'ulitsa': data['Адрес'].split(' ')[0] if len(data['Адрес'].split(' ')) >= 1 else '-',
            'vlozheniya': [],
            'yazik_dokumenta': data['Язык'] or '-',
            'whatsapp_telegram': 'Telegram'
        }         
        import requests
        from requests.auth import HTTPBasicAuth
        response = requests.post('https://doc.nurotan.kz/webservice/json/82be1ae3-5131-47ab-ae04-5fcc8a8a0161',
        auth=HTTPBasicAuth('Chatbot', "password"),
        data=data)

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
    sql = "SELECT messanger_id FROM n_clients WHERE id = '{}' LIMIT 1".format(request.form['user_id'])
    cursor.execute(sql)
    results = cursor.fetchall()
    
    import telebot
    token = 'token'
    bot   = telebot.TeleBot(token)
    bot.send_message(results[0][0], request.form['message'], parse_mode='Markdown')
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
    
    sql = """SELECT b.id, b.title, b.answers_type,
        JSON_ARRAYAGG(JSON_OBJECT('id', a.id, 'content', a.content)) AS answers,
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
    import telebot
    from telebot import types
    token = 'token'
    bot   = telebot.TeleBot(token)
    sql = "SELECT messanger_id FROM n_clients WHERE id = '{}' LIMIT 1".format(request.form['client_id'])
    cursor.execute(sql)
    results = cursor.fetchall()
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

    answer = "Шаг изменён"
    return answer







if __name__ == '__main__':
    app.run(host='185.22.64.75',port=3143,debug=False)