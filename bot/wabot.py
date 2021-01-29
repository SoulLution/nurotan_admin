#!/usr/bin/python
# -*- coding: utf-8

import json
import requests
import datetime
from bs4 import BeautifulSoup


def replaceText(text):
    return BeautifulSoup(text.replace('<p>','\n').replace('<br>','\n').replace('<strong>','*').replace('</strong>','*').replace('<em>','_').replace('</em>','_').strip(), "html.parser").get_text()
def replaceTextButton(text):
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

class WABot():    
    def __init__(self, json):
        self.json = json
        self.APIUrl = 'https://eu188.chat-api.com/instance209738/'
        self.token = 't76l2xhbiudrs3uv'

   
    def send_requests(self, method, data):
        url = "{}{}?token={}".format(self.APIUrl, method, self.token)
        headers = {'Content-type': 'application/json'}
        answer = requests.post(url, data=json.dumps(data), headers=headers)
        print(answer.json())
        return answer.json()

    def send_message(self, chatID, text):
        data = {"chatId" : chatID,
                "body" : text}  
        answer = self.send_requests('sendMessage', data)
        print(answer)
        return answer


    def processing(self):
        import iz_func 
        db,cursor = iz_func.connect ()
        message = self.json['messages'][0]
        text = message['body'].split()
        # text[0].lower()
        if not message['fromMe']:
            id  = message['chatId']
            sql = """SELECT id, branch_id
            FROM n_clients
            WHERE messanger_id = '{}'
            LIMIT 1
            """.format(id)
            cursor.execute(sql)
            results = cursor.fetchall()
            user = {}
            item = {'is_request': 0}
            if len(results) == 0 : 
                sql = "SELECT * FROM n_users WHERE is_admin = 'No' ORDER BY RAND() LIMIT 1"
                cursor.execute(sql)
                results2 = cursor.fetchall()  
                sql = """INSERT INTO n_clients 
                (`name`,`from`,`user_id`,`branch_id`,`messanger_id`) 
                VALUES ('{}','wp','{}','{}','{}')
                """.format(message['senderName'],  results2[0][0], 1, id)  
                cursor.execute(sql)
                db.commit()  
                user = {
                    'id': cursor.lastrowid,
                    'branch_id': 1
                }
                sql = """SET SESSION group_concat_max_len = 1000000"""
                cursor.execute(sql)
                sql = """SELECT b.id, b.title, b.answers_type,
                    CONCAT(
                    '[',
                        GROUP_CONCAT(
                            JSON_OBJECT('id',a.id,'content', a.content)
                            order by a.position
                        ),
                    ']'
                    ) answers,
                    b.is_request
                    FROM n_branch b
                    LEFT JOIN n_answers a ON  a.branch_id = b.id
                    WHERE b.id = 1
                    GROUP BY b.id
                    LIMIT 1"""
                cursor.execute(sql)
                results2 = cursor.fetchall()     
                item = {
                    'id': results2[0][0],
                    'title': results2[0][1],
                    'answers_type': results2[0][2],
                    'answers': json.loads(results2[0][3]),
                    'is_request': results2[0][4]
                }
                if item['answers_type'] != '2' :
                    i = 1
                    for answer in item['answers']:  
                        item['title'] += '\n'
                        for j in str(i):    
                            item['title'] += addEmoji(j)
                        item['title'] += replaceTextButton(answer['content'])
                        i += 1
                    sql = "INSERT INTO n_messages (`content`,`from`,`user_id`) VALUES ('{}', 'bot', '{}')".format(item['title'], user['id'])
                    cursor.execute(sql)
                    db.commit()
                    self.send_message(id, replaceText(item['title']))
                else :
                    sql = "INSERT INTO n_messages (`content`,`from`,`user_id`) VALUES ('{}', 'bot', '{}')".format(item['title'], user['id'])
                    cursor.execute(sql)
                    db.commit()
                    self.send_message(id, replaceText(item['title']))
                return {'status': 200}
            else :
                user = {
                    'id': results[0][0],
                    'branch_id': results[0][1]
                }
            sql = "INSERT INTO n_messages (`content`,`from`,`user_id`) VALUES ('{}', 'client', '{}')".format(text[0].lower(), user['id'])
            cursor.execute(sql)
            db.commit()
            sql = """SET SESSION group_concat_max_len = 1000000"""
            cursor.execute(sql)
            sql = """SELECT b.id, b.answers_type, b.to_branch,
                CONCAT(
                '[',
                    GROUP_CONCAT(
                        JSON_OBJECT('id', a.id, 'to_branch', a.to_branch,'content', a.content, 'tag_id',a.tag_id, 'documentolog_id', a.documentolog_id)
                        order by a.position
                    ),
                ']'
                ) answers,
                b.is_request
                FROM n_branch b
                LEFT JOIN n_answers a ON  a.branch_id = b.id
                WHERE b.id = {}
                GROUP BY b.id
                LIMIT 1""".format(user['branch_id'])
                
            cursor.execute(sql)
            results2 = cursor.fetchall()     
            current = {
                'id': results2[0][0],
                'answers_type': results2[0][1],
                'to_branch': results2[0][2],
                'answers': json.loads(results2[0][3]),
                'is_request': results2[0][4]
            }
            ans_i = 0
            if current['answers_type'] == '2':
                if current['to_branch'] and current['to_branch'] != 'null' :
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
                        LIMIT 1""".format(current['to_branch'])
                    cursor.execute(sql)
                    results2 = cursor.fetchall()     
                    item = {
                        'id': results2[0][0],
                        'title': results2[0][1],
                        'answers_type': results2[0][2],
                        'answers': json.loads(results2[0][3]),
                        'is_request': results2[0][4]
                    }
                else:
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
                        WHERE b.id = 1
                        GROUP BY b.id
                        LIMIT 1"""
                    cursor.execute(sql)
                    results2 = cursor.fetchall()     
                    item = {
                        'id': results2[0][0],
                        'title': results2[0][1],
                        'answers_type': results2[0][2],
                        'answers': json.loads(results2[0][3]),
                        'is_request': results2[0][4]
                    }
                if item['answers_type'] != '2' :
                    i = 1
                    for answer in item['answers']:  
                        item['title'] += '\n'
                        for j in str(i):    
                            item['title'] += addEmoji(j)
                        item['title'] += replaceTextButton(answer['content'])
                        i += 1
                    sql = "INSERT INTO n_messages (`content`,`from`,`user_id`) VALUES ('{}', 'bot', '{}')".format(item['title'], user['id'])
                    cursor.execute(sql)
                    db.commit()
                    self.send_message(id, replaceText(item['title']))
                else :
                    sql = "INSERT INTO n_messages (`content`,`from`,`user_id`) VALUES ('{}', 'bot', '{}')".format(item['title'], user['id'])
                    cursor.execute(sql)
                    db.commit()
                    self.send_message(id, replaceText(item['title']))

            else:
                ans_i = 1
                for answer in current['answers']: 
                    if text[0].lower() == str(ans_i) :
                        if answer['to_branch'] and answer['to_branch'] != 'null' :
                            sql = """SET SESSION group_concat_max_len = 1000000"""
                            cursor.execute(sql)
                            sql = """SELECT b.id, b.title, b.answers_type,
                                CONCAT(
                                '[',
                                    GROUP_CONCAT(
                                        JSON_OBJECT('id',a.id,'content', a.content)
                                        order by a.position
                                    ),
                                ']'
                                ) answers,
                                b.is_request
                                FROM n_branch b
                                LEFT JOIN n_answers a ON  a.branch_id = b.id
                                WHERE b.id = {}
                                GROUP BY b.id
                                LIMIT 1""".format(answer['to_branch'])
                            cursor.execute(sql)
                            results2 = cursor.fetchall()     
                            item = {
                                'id': results2[0][0],
                                'title': results2[0][1],
                                'answers_type': results2[0][2],
                                'answers': json.loads(results2[0][3]),
                                'is_request': results2[0][4]
                            }
                        else:
                            sql = """SET SESSION group_concat_max_len = 1000000"""
                            cursor.execute(sql)
                            sql = """SELECT b.id, b.title, b.answers_type,
                                CONCAT(
                                '[',
                                    GROUP_CONCAT(
                                        JSON_OBJECT('id',a.id,'content', a.content)
                                        order by a.position
                                    ),
                                ']'
                                ) answers,
                                b.is_request
                                FROM n_branch b
                                LEFT JOIN n_answers a ON  a.branch_id = b.id
                                WHERE b.id = 1
                                GROUP BY b.id
                                LIMIT 1"""
                            cursor.execute(sql)
                            results2 = cursor.fetchall()     
                            item = {
                                'id': results2[0][0],
                                'title': results2[0][1],
                                'answers_type': results2[0][2],
                                'answers': json.loads(results2[0][3]),
                                'is_request': results2[0][4]
                            }
                        if item['answers_type'] != '2' :
                            j = 1
                            for answer in item['answers']:  
                                item['title'] += '\n'
                                for k in str(j):    
                                    item['title'] += addEmoji(k)
                                item['title'] += replaceTextButton(answer['content'])
                                j += 1
                            sql = "INSERT INTO n_messages (`content`,`from`,`user_id`) VALUES ('{}', 'bot', '{}')".format(item['title'], user['id'])
                            cursor.execute(sql)
                            db.commit()
                            self.send_message(id, replaceText(item['title']))
                        else :
                            sql = "INSERT INTO n_messages (`content`,`from`,`user_id`) VALUES ('{}', 'bot', '{}')".format(item['title'], user['id'])
                            cursor.execute(sql)
                            db.commit()
                            self.send_message(id, replaceText(item['title']))
                        break
                    ans_i += 1

            if current['is_request'] and current['is_request'] != 'undefined' :
                sql = "SELECT id FROM n_requests WHERE client_id = {} AND status = 0".format(user['id'])
                cursor.execute(sql)
                results = cursor.fetchall()     
                request = {}
                if len(results) > 0 :
                    request = {
                        'id': results[0][0]
                    }
                else :
                    sql = "INSERT INTO n_requests (`status`,`checked`,`client_id`) VALUES (0,0,'{}')".format(user['id'])
                    cursor.execute(sql)
                    db.commit()
                    request = {
                        'id': cursor.lastrowid
                    }
                    
                sql = """SELECT rc.id FROM n_requests r
                        JOIN n_request_content rc ON rc.request_id = r.id
                        WHERE rc.title = '{}' 
                        AND r.status = 0
                        AND r.client_id = {}
                        """.format(current['is_request'], user['id'])
                cursor.execute(sql)
                results = cursor.fetchall()     
                if len(results) > 0 :
                    if ans_i == 0:
                        sql = "UPDATE n_request_content SET answer = '{}' WHERE `id` = {}".format(replaceTextButton(text[0].lower()), results[0][0])
                    else:
                        sql = "UPDATE n_request_content SET answer = '{}' WHERE `id` = {}".format(replaceTextButton(current['answers'][ans_i-1]['content']), results[0][0])
                        sql = "UPDATE n_request_content SET documentolog_id = '{}' WHERE `id` = {}".format(current['answers'][ans_i-1]['documentolog_id'], results[0][0])
                    cursor.execute(sql)
                    db.commit()
                    sql = "UPDATE n_request_content SET branch_id = '{}' WHERE `id` = {}".format(current['id'], results[0][0])
                    cursor.execute(sql)
                    db.commit()
                else :
                    if ans_i == 0:
                        sql = "INSERT INTO n_request_content (`request_id`,`title`,`answer`, `branch_id`) VALUES ('{}','{}','{}','{}')".format(request['id'], current['is_request'], replaceTextButton(text[0].lower()), current['id'])
                    else:
                        sql = "INSERT INTO n_request_content (`request_id`,`title`,`answer`, `branch_id`, `documentolog_id`) VALUES ('{}','{}','{}','{}','{}')".format(request['id'], current['is_request'], replaceTextButton(current['answers'][ans_i-1]['content']), current['id'], current['answers'][ans_i-1]['documentolog_id'])
                    cursor.execute(sql)
                    db.commit()
            if item['is_request'] and item['is_request'] == 'undefined' :
                sql = "SELECT id FROM n_requests WHERE client_id = '{}' AND status = '0'".format(user['id'])
                cursor.execute(sql)
                results = cursor.fetchall()
                if len(results) > 0 :
                    sql = "UPDATE n_requests SET status = '1' WHERE `id` = '"+str(results[0][0])+"'"
                    cursor.execute(sql)
                    db.commit()
                    sql = "UPDATE n_requests SET date = now() WHERE `id` = '"+str(results[0][0])+"'"
                    cursor.execute(sql)
                    db.commit()


            sql = "UPDATE n_clients SET branch_id = "+str(item['id'])+" WHERE `id` = '"+str(user['id'])+"'"
            cursor.execute(sql)
            db.commit()
        return {'status': 200}