#!/usr/bin/python
# -*- coding: utf-8

import time
import random
import iz_func
import telebot
import pymysql    
import json
from telebot import types
from telebot import apihelper
from bs4 import BeautifulSoup


namebot = "@ask314_bot"    
token = '1393957889:AAEy0SgED_mt0zooGfgsrUHsQvkoC_7THz0'
bot   = telebot.TeleBot(token)
print ('[+] Запуск бота:',namebot)

def replaceText(text):
    return BeautifulSoup(text.replace('<p>','\n').replace('<br>','\n').replace('<strong>','*').replace('</strong>','*').replace('<em>','_').replace('</em>','_').strip(), "html.parser").get_text()
def replaceTextButton(text):
    return BeautifulSoup(text.strip(), "html.parser").get_text()
 
@bot.message_handler(commands=['start'])
def welcome(message):
    import iz_func 
    db,cursor = iz_func.connect ()

    sql = """SELECT id
    FROM n_clients
    WHERE messanger_id = {}
    LIMIT 1
    """.format(message.from_user.id)
    cursor.execute(sql)
    results = cursor.fetchall()  
    user = {}
    if len(results) == 0 : 
        sql = "SELECT * FROM n_users WHERE is_admin = 'No' ORDER BY RAND() LIMIT 1"
        cursor.execute(sql)
        results2 = cursor.fetchall()  
        sql = """INSERT INTO n_clients 
        (`name`,`from`,`user_id`,`branch_id`,`messanger_id`) 
        VALUES ('{}','tg','{}','{}','{}')
        """.format(message.from_user.first_name + (message.from_user.last_name or ''),  results2[0][0], 1, message.from_user.id)  
        cursor.execute(sql)
        db.commit()  
        user = {
            'id': cursor.lastrowid
        }
    else :
        user = {
            'id': results[0][0]
        }

    sql = "UPDATE n_clients SET branch_id = '1' WHERE `id` = '"+str(user['id'])+"'"
    cursor.execute(sql)
    db.commit()
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
        ) answers 
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
        'answers': json.loads(results2[0][3])
    }

    # keyboard
    if item['answers_type'] == '0' :
        markup = types.InlineKeyboardMarkup(row_width=2)
        for answer in item['answers']:  
            mark_item = types.InlineKeyboardButton(text=replaceTextButton(answer['content']), callback_data=(answer['id']))
            markup.add(mark_item)
        bot.send_message(message.chat.id, replaceText(item['title']), parse_mode='Markdown', reply_markup=markup)
        sql = "INSERT INTO n_messages (`content`,`from`,`user_id`) VALUES ('{}', 'bot', '{}')".format(item['title'], user['id'])
        cursor.execute(sql)
        db.commit()

    elif item['answers_type'] == '1' :
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        for answer in item['answers']:    
            mark_item = types.KeyboardButton(text=replaceTextButton(answer['content']))
            markup.add(mark_item)
        bot.send_message(message.chat.id, replaceText(item['title']), parse_mode='Markdown', reply_markup=markup)
        sql = "INSERT INTO n_messages (`content`,`from`,`user_id`) VALUES ('{}', 'bot', '{}')".format(item['title'], user['id'])
        cursor.execute(sql)
        db.commit()

    else :
        bot.send_message(message.chat.id, replaceText(item['title']), parse_mode='Markdown')
        sql = "INSERT INTO n_messages (`content`,`from`,`user_id`) VALUES ('{}', 'bot', '{}')".format(item['title'], user['id'])
        cursor.execute(sql)
        db.commit()
 
@bot.message_handler(content_types=['text'])
def messageHandler(message):
    import iz_func 
    db,cursor = iz_func.connect ()
    if message.chat.type == 'private':
        sql = """SELECT id, branch_id
        FROM n_clients
        WHERE messanger_id = {}
        LIMIT 1
        """.format(message.from_user.id)
        cursor.execute(sql)
        user = cursor.fetchall()  
        user = {
            'id': user[0][0],
            'branch_id': user[0][1]
        }
        sql = "INSERT INTO n_messages (`content`,`from`,`user_id`) VALUES ('{}', 'client', '{}')".format(message.text, user['id'])
        cursor.execute(sql)
        db.commit()
        sql = """SET SESSION group_concat_max_len = 1000000"""
        cursor.execute(sql)
    
        sql = """SELECT b.id, b.answers_type, b.to_branch,
            CONCAT(
            '[',
                GROUP_CONCAT(
                    JSON_OBJECT('id', a.id, 'to_branch', a.to_branch,'content', a.content, 'tag_id',a.tag_id, 'documentolog_id',a.documentolog_id)
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
        cur_answer = {'id': 0}
        item = {'is_request': 0}
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
            # if current['answers_type'] == '0' :
            #     bot.edit_message_reply_markup(message.chat.id, message_id = message.message_id-1, reply_markup = '')
            if item['answers_type'] == '0' :
                markup = types.InlineKeyboardMarkup(row_width=2)
                for answer in item['answers']:      
                    markup_item = types.InlineKeyboardButton(text=replaceTextButton(answer['content']), callback_data=(answer['id']))
                    markup.add(markup_item)
                bot.send_message(message.chat.id, replaceText(item['title']), parse_mode='Markdown', reply_markup=markup)
                sql = "INSERT INTO n_messages (`content`,`from`,`user_id`) VALUES ('{}', 'bot', '{}')".format(item['title'], user['id'])
                cursor.execute(sql)
                db.commit()

            elif item['answers_type'] == '1' :
                markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
                for answer in item['answers']:    
                    markup_item = types.KeyboardButton(text=replaceTextButton(answer['content']))
                    markup.add(markup_item)
                bot.send_message(message.chat.id, replaceText(item['title']), parse_mode='Markdown', reply_markup=markup)
                sql = "INSERT INTO n_messages (`content`,`from`,`user_id`) VALUES ('{}', 'bot', '{}')".format(item['title'], user['id'])
                cursor.execute(sql)
                db.commit()

            else :
                bot.send_message(message.chat.id, replaceText(item['title']), parse_mode='Markdown')
                sql = "INSERT INTO n_messages (`content`,`from`,`user_id`) VALUES ('{}', 'bot', '{}')".format(item['title'], user['id'])
                cursor.execute(sql)
                db.commit()

        else:
            for answer in current['answers']: 
                if message.text == replaceTextButton(answer['content']) :
                    cur_answer = answer
                    if answer['to_branch'] and answer['to_branch'] != 'null' :
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
                    # if current['answers_type'] == '0' :
                    #     bot.edit_message_reply_markup(message.chat.id, message_id = message.message_id-1, reply_markup = '')
                    if item['answers_type'] == '0' :
                        markup = types.InlineKeyboardMarkup(row_width=2)
                        for answer in item['answers']:    
                            markup_item = types.InlineKeyboardButton(text=replaceTextButton(answer['content']), callback_data=(answer['id']))
                            markup.add(markup_item)
                        bot.send_message(message.chat.id, replaceText(item['title']), parse_mode='Markdown', reply_markup=markup)
                        sql = "INSERT INTO n_messages (`content`,`from`,`user_id`) VALUES ('{}', 'bot', '{}')".format(item['title'], user['id'])
                        cursor.execute(sql)
                        db.commit()

                    elif item['answers_type'] == '1' :
                        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
                        for answer in item['answers']:    
                            markup_item = types.KeyboardButton(text=replaceTextButton(answer['content']))
                            markup.add(markup_item)
                        bot.send_message(message.chat.id, replaceText(item['title']), parse_mode='Markdown', reply_markup=markup)
                        sql = "INSERT INTO n_messages (`content`,`from`,`user_id`) VALUES ('{}', 'bot', '{}')".format(item['title'], user['id'])
                        cursor.execute(sql)
                        db.commit()

                    else :
                        bot.send_message(message.chat.id, replaceText(item['title']), parse_mode='Markdown')
                        sql = "INSERT INTO n_messages (`content`,`from`,`user_id`) VALUES ('{}', 'bot', '{}')".format(item['title'], user['id'])
                        cursor.execute(sql)
                        db.commit()

        
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
                sql = "UPDATE n_request_content SET answer = '{}' WHERE `id` = {}".format(replaceTextButton(message.text), results[0][0])
                cursor.execute(sql)
                db.commit()
                sql = "UPDATE n_request_content SET branch_id = '{}' WHERE `id` = {}".format(current['id'], results[0][0])
                cursor.execute(sql)
                db.commit()
                if(cur_answer['id']):
                    sql = "UPDATE n_request_content SET documentolog_id = '{}' WHERE `id` = {}".format(cur_answer['documentolog_id'], results[0][0])
                    cursor.execute(sql)
                    db.commit()
            else :
                if(cur_answer['id'] and cur_answer['documentolog_id']):
                    sql = "INSERT INTO n_request_content (`request_id`,`title`,`answer`, `branch_id`, `documentolog_id`) VALUES ('{}','{}','{}','{}','{}')".format(request['id'], current['is_request'], replaceTextButton(message.text), current['id'], cur_answer['documentolog_id'])
                else:
                    sql = "INSERT INTO n_request_content (`request_id`,`title`,`answer`, `branch_id`) VALUES ('{}','{}','{}','{}')".format(request['id'], current['is_request'], replaceTextButton(message.text), current['id'])
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



@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    import iz_func 
    db,cursor = iz_func.connect ()
    try:
        item = {}
        sql = """SELECT id, branch_id
        FROM n_clients
        WHERE messanger_id = {}
        LIMIT 1
        """.format(call.from_user.id)
        cursor.execute(sql)
        user = cursor.fetchall()  
        user = {
            'id': user[0][0],
            'branch_id': user[0][1]
        }
        sql = """SET SESSION group_concat_max_len = 1000000"""
        cursor.execute(sql)
            
        sql = """SELECT b.id, b.answers_type, b.to_branch,
            CONCAT(
            '[',
                GROUP_CONCAT(
                    JSON_OBJECT('id', a.id, 'to_branch', a.to_branch,'content', a.content, 'tag_id',a.tag_id,'documentolog_id',a.documentolog_id)
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
            if item['answers_type'] == '0' :
                markup = types.InlineKeyboardMarkup(row_width=2)
                for answer in item['answers']:    
                    markup_item = types.InlineKeyboardButton(text=replaceTextButton(answer['content']), callback_data=(answer['id']))
                    markup.add(markup_item)
                bot.send_message(call.message.chat.id, replaceText(item['title']), parse_mode='Markdown', reply_markup=markup)
                sql = "INSERT INTO n_messages (`content`,`from`,`user_id`) VALUES ('{}', 'bot', '{}')".format(item['title'], user['id'])
                cursor.execute(sql)
                db.commit()

            elif item['answers_type'] == '1' :
                markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
                for answer in item['answers']:    
                    markup_item = types.KeyboardButton(text=replaceTextButton(answer['content']))
                    markup.add(markup_item)
                bot.send_message(call.message.chat.id, replaceText(item['title']), parse_mode='Markdown', reply_markup=markup)
                sql = "INSERT INTO n_messages (`content`,`from`,`user_id`) VALUES ('{}', 'bot', '{}')".format(item['title'], user['id'])
                cursor.execute(sql)
                db.commit()

            else :
                bot.send_message(call.message.chat.id, replaceText(item['title']), parse_mode='Markdown')
                sql = "INSERT INTO n_messages (`content`,`from`,`user_id`) VALUES ('{}', 'bot', '{}')".format(item['title'], user['id'])
                cursor.execute(sql)
                db.commit()

        else:
            for answer in current['answers']: 
                if str(call.data) == str(answer['id']) :
                    sql = "INSERT INTO n_messages (`content`,`from`,`user_id`) VALUES ('{}', 'client', '{}')".format(answer['content'], user['id'])
                    cursor.execute(sql)
                    db.commit()
                    if answer['to_branch'] and answer['to_branch'] != 'null' :
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
                                    JSON_OBJECT('id', a.id, 'content', a.content)
                                    order by a.position
                                ),
                            ']') answers,
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
                    # if current['answers_type'] == '0' :
                    #     bot.edit_message_reply_markup(call.message.chat.id, message_id = call.message.message_id-1, reply_markup = '')
                    if item['answers_type'] == '0' :
                        markup = types.InlineKeyboardMarkup(row_width=2)
                        for answer in item['answers']:   
                            markup_item = types.InlineKeyboardButton(text=replaceTextButton(answer['content']), callback_data=(answer['id']))
                            markup.add(markup_item)
                        bot.send_message(call.message.chat.id, replaceText(item['title']), parse_mode='Markdown', reply_markup=markup)
                        sql = "INSERT INTO n_messages (`content`,`from`,`user_id`) VALUES ('{}', 'bot', '{}')".format(item['title'], user['id'])
                        cursor.execute(sql)
                        db.commit()

                    elif item['answers_type'] == '1' :
                        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
                        for answer in item['answers']:    
                            markup_item = types.KeyboardButton(text=replaceTextButton(answer['content']))
                            markup.add(markup_item)
                        bot.send_message(call.message.chat.id, replaceText(item['title']), parse_mode='Markdown', reply_markup=markup)
                        sql = "INSERT INTO n_messages (`content`,`from`,`user_id`) VALUES ('{}', 'bot', '{}')".format(item['title'], user['id'])
                        cursor.execute(sql)
                        db.commit()

                    else :
                        bot.send_message(call.message.chat.id, replaceText(item['title']), parse_mode='Markdown')
                        sql = "INSERT INTO n_messages (`content`,`from`,`user_id`) VALUES ('{}', 'bot', '{}')".format(item['title'], user['id'])
                        cursor.execute(sql)
                        db.commit()


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
            for answer in current['answers']: 
                if str(call.data) == str(answer['id']) :
                    sql = """SELECT rc.id FROM n_requests r
                            JOIN n_request_content rc ON rc.request_id = r.id
                            WHERE rc.title = '{}' 
                            AND r.status = 0
                            AND r.client_id = {}
                            """.format(current['is_request'], user['id'])
                    cursor.execute(sql)
                    results = cursor.fetchall()     
                    if len(results) > 0 :
                        sql = "UPDATE n_request_content SET answer = '{}' WHERE `id` = {}".format(replaceTextButton(answer['content']), results[0][0])
                        cursor.execute(sql)
                        db.commit()
                        sql = "UPDATE n_request_content SET branch_id = '{}' WHERE `id` = {}".format(current['id'], results[0][0])
                        cursor.execute(sql)
                        db.commit()
                        sql = "UPDATE n_request_content SET documentolog_id = '{}' WHERE `id` = {}".format(answer['documentolog_id'], results[0][0])
                        cursor.execute(sql)
                        db.commit()
                    else :
                        sql = "INSERT INTO n_request_content (`request_id`,`title`,`answer`, `branch_id`, `documentolog_id`) VALUES ('{}','{}','{}','{}','{}')".format(request['id'], current['is_request'], replaceTextButton(answer['content']),current['id'],answer['documentolog_id'])
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
 
    except Exception as e:
        print(repr(e))

def botSendMessage (id, message) :
    bot.send_message(id, replaceText(message), parse_mode='Markdown')
    return True
# RUN
bot.polling()