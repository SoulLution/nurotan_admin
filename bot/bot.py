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
from pprint import pprint
from bs4 import BeautifulSoup


namebot = "@ask314_bot"    
token = '1455208962:AAGhAGxhgQfxM4O251tsc3ZuJEnBTO_J9KY'
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
    print('-----------------')
    print(len(results))
    pprint(results)
    print('-----------------')
    if len(results) == 0 : 
        sql = "SELECT * FROM n_users WHERE is_admin = 'No' ORDER BY RAND() LIMIT 1"
        cursor.execute(sql)
        results2 = cursor.fetchall()  
        pprint(results2[0][0])
        sql = """INSERT INTO n_clients 
        (`name`,`from`,`user_id`,`branch_id`,`messanger_id`) 
        VALUES ('{}','tg','{}','{}','{}')
        """.format(message.from_user.first_name + (message.from_user.last_name or ''),  results2[0][0], 1, message.from_user.id)  
        cursor.execute(sql)
        db.commit()  

    sql = """SELECT b.id, b.title, b.answers_type,
          JSON_ARRAYAGG(JSON_OBJECT('id', a.id, 'content', a.content)) AS answers
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

    pprint(item['answers_type'])
    # keyboard
    if item['answers_type'] == '0' :
        markup = types.InlineKeyboardMarkup(row_width=2)
        for answer in item['answers']:  
            mark_item = types.InlineKeyboardButton(text=replaceTextButton(answer['content']), callback_data=(answer['id']))
            markup.add(mark_item)
        bot.send_message(message.chat.id, replaceText(item['title']), parse_mode='Markdown', reply_markup=markup)

    elif item['answers_type'] == '1' :
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        for answer in item['answers']:    
            mark_item = types.KeyboardButton(text=replaceTextButton(answer['content']))
            markup.add(mark_item)
        bot.send_message(message.chat.id, replaceText(item['title']), parse_mode='Markdown', reply_markup=markup)

    else :
        bot.send_message(message.chat.id, replaceText(item['title']), parse_mode='Markdown')
 
@bot.message_handler(content_types=['text'])
def messageHandler(message):
    import iz_func 
    db,cursor = iz_func.connect ()
    print('message--------------------------------------')
    pprint(message)
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
        sql = """SELECT b.answers_type, b.to_branch,
            JSON_ARRAYAGG(JSON_OBJECT('id', a.id, 'to_branch', a.to_branch,'content', a.content, 'tag_id',a.tag_id)) AS answers
            FROM n_branch b
            LEFT JOIN n_answers a ON  a.branch_id = b.id
            WHERE b.id = {}
            GROUP BY b.id
            LIMIT 1""".format(user['branch_id'])
            
        cursor.execute(sql)
        results2 = cursor.fetchall()     
        current = {
            'answers_type': results2[0][0],
            'to_branch': results2[0][1],
            'answers': json.loads(results2[0][2])
        }
        if current['answers_type'] == '2':
            print('popal*********************************1')
            if current['to_branch'] :
                sql = """SELECT b.id, b.title, b.answers_type,
                    JSON_ARRAYAGG(JSON_OBJECT('id', a.id, 'content', a.content)) AS answers
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
                    'answers': json.loads(results2[0][3])
                }
            else:
                sql = """SELECT b.id, b.title, b.answers_type,
                    JSON_ARRAYAGG(JSON_OBJECT('id', a.id, 'content', a.content)) AS answers
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
            if item['answers_type'] == '0' :
                markup = types.InlineKeyboardMarkup(row_width=2)
                for answer in item['answers']:      
                    pprint(answer)
                    markup_item = types.InlineKeyboardButton(text=replaceTextButton(answer['content']), callback_data=(answer['id']))
                    markup.add(markup_item)
                bot.send_message(message.chat.id, replaceText(item['title']), parse_mode='Markdown', reply_markup=markup)

            elif item['answers_type'] == '1' :
                markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
                for answer in item['answers']:    
                    markup_item = types.KeyboardButton(text=replaceTextButton(answer['content']))
                    markup.add(markup_item)
                bot.send_message(message.chat.id, replaceText(item['title']), parse_mode='Markdown', reply_markup=markup)

            else :
                bot.send_message(message.chat.id, replaceText(item['title']), parse_mode='Markdown')

        else:
            for answer in current['answers']: 
                if message.text == replaceTextButton(answer['content']) :
                    if answer['to_branch'] :
                        sql = """SELECT b.id, b.title, b.answers_type,
                            JSON_ARRAYAGG(JSON_OBJECT('id', a.id, 'content', a.content)) AS answers
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
                            'answers': json.loads(results2[0][3])
                        }
                    else:
                        sql = """SELECT b.id, b.title, b.answers_type,
                            JSON_ARRAYAGG(JSON_OBJECT('id', a.id, 'content', a.content)) AS answers
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
                    if item['answers_type'] == '0' :
                        markup = types.InlineKeyboardMarkup(row_width=2)
                        for answer in item['answers']:    
                            markup_item = types.InlineKeyboardButton(text=replaceTextButton(answer['content']), callback_data=(answer['id']))
                            markup.add(markup_item)
                        bot.send_message(message.chat.id, replaceText(item['title']), parse_mode='Markdown', reply_markup=markup)

                    elif item['answers_type'] == '1' :
                        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
                        for answer in item['answers']:    
                            markup_item = types.KeyboardButton(text=replaceTextButton(answer['content']))
                            markup.add(markup_item)
                        bot.send_message(message.chat.id, replaceText(item['title']), parse_mode='Markdown', reply_markup=markup)

                    else :
                        bot.send_message(message.chat.id, replaceText(item['title']), parse_mode='Markdown')

        sql = "UPDATE n_clients SET branch_id = "+str(item['id'])+" WHERE `id` = '"+str(user['id'])+"'"
        cursor.execute(sql)
        db.commit()



@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    import iz_func 
    db,cursor = iz_func.connect ()
    print('call--------------------------------------')
    pprint(call)
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
        sql = """SELECT b.answers_type, b.to_branch,
            JSON_ARRAYAGG(JSON_OBJECT('id', a.id, 'to_branch', a.to_branch,'content', a.content, 'tag_id',a.tag_id)) AS answers
            FROM n_branch b
            LEFT JOIN n_answers a ON  a.branch_id = b.id
            WHERE b.id = {}
            GROUP BY b.id
            LIMIT 1""".format(user['branch_id'])
            
        cursor.execute(sql)
        results2 = cursor.fetchall()     
        current = {
            'answers_type': results2[0][0],
            'to_branch': results2[0][1],
            'answers': json.loads(results2[0][2])
        }
        if current['answers_type'] == '2':
            if current['to_branch'] :
                sql = """SELECT b.id, b.title, b.answers_type,
                    JSON_ARRAYAGG(JSON_OBJECT('id', a.id, 'content', a.content)) AS answers
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
                    'answers': json.loads(results2[0][3])
                }
            else:
                sql = """SELECT b.id, b.title, b.answers_type,
                    JSON_ARRAYAGG(JSON_OBJECT('id', a.id, 'content', a.content)) AS answers
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
            if item['answers_type'] == '0' :
                markup = types.InlineKeyboardMarkup(row_width=2)
                for answer in item['answers']:    
                    markup_item = types.InlineKeyboardButton(text=replaceTextButton(answer['content']), callback_data=(answer['id']))
                    markup.add(markup_item)
                bot.send_message(call.message.chat.id, replaceText(item['title']), parse_mode='Markdown', reply_markup=markup)

            elif item['answers_type'] == '1' :
                markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
                for answer in item['answers']:    
                    markup_item = types.KeyboardButton(text=replaceTextButton(answer['content']))
                    markup.add(markup_item)
                bot.send_message(call.message.chat.id, replaceText(item['title']), parse_mode='Markdown', reply_markup=markup)

            else :
                bot.send_message(call.message.chat.id, replaceText(item['title']), parse_mode='Markdown')

        else:
            for answer in current['answers']: 
                if str(call.data) == str(answer['id']) :
                    pprint(answer)
                    if answer['to_branch'] :
                        sql = """SELECT b.id, b.title, b.answers_type,
                            JSON_ARRAYAGG(JSON_OBJECT('id', a.id, 'content', a.content)) AS answers
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
                            'answers': json.loads(results2[0][3])
                        }
                    else:
                        sql = """SELECT b.id, b.title, b.answers_type,
                            JSON_ARRAYAGG(JSON_OBJECT('id', a.id, 'content', a.content)) AS answers
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
                    if item['answers_type'] == '0' :
                        markup = types.InlineKeyboardMarkup(row_width=2)
                        for answer in item['answers']:   
                            markup_item = types.InlineKeyboardButton(text=replaceTextButton(answer['content']), callback_data=(answer['id']))
                            markup.add(markup_item)
                        bot.send_message(call.message.chat.id, replaceText(item['title']), parse_mode='Markdown', reply_markup=markup)

                    elif item['answers_type'] == '1' :
                        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
                        for answer in item['answers']:    
                            markup_item = types.KeyboardButton(text=replaceTextButton(answer['content']))
                            markup.add(markup_item)
                        bot.send_message(call.message.chat.id, replaceText(item['title']), parse_mode='Markdown', reply_markup=markup)

                    else :
                        bot.send_message(call.message.chat.id, replaceText(item['title']), parse_mode='Markdown')

        pprint(call.data)
        pprint(user)
        print('ids-----------------', item['id'], user['id'])
        sql = "UPDATE n_clients SET branch_id = "+str(item['id'])+" WHERE `id` = '"+str(user['id'])+"'"
        cursor.execute(sql)
        db.commit()
 
    except Exception as e:
        print(repr(e))
 
# RUN
bot.polling(none_stop=True)