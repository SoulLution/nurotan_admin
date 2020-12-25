#!/usr/bin/python
# -*- coding: utf-8
# ОПИСАНИЕ БОТА: Бот для разработок новых ботов
# АВТОР БОТА   : Купинов Вадим
# ТЕЛЕГРАММ АВТОРА : @izofen

import random
import iz_func
import iz_proxy
import iz_main
import iz_telegram
import time
import requests
import json 
import telebot
import iz_func

print ('[+] Запускаем отправку сообшений')
namebot = "@BT_trader_bot"
user_id = '399838806'
token,about = iz_func.get_token (namebot)
bot   = telebot.TeleBot(token)
markup  = ''
message_out  = '<b> Отчетность по выставленным счетам </b>'
message_send = iz_func.bot_send (user_id,message_out,markup,bot,namebot)

db,cursor = iz_func.connect (namebot)
sql = "select id,exchange,symbol,torg,price,demo,procent,robot,strateg from openorder where status = 'open' "
cursor.execute(sql)
data = cursor.fetchall()
for rec in data: 
    id,exchange,symbol,torg,price,demo,procent,robot,strateg = rec
    print (' ')
    print ('    [+] procent',procent)
    print ('    [+] price',price)
    print ('    [+] symbol',symbol)
    print ('    [+] procent',procent)
    print ('    [+] torg',torg)
    print ('    [+] robot',robot)
    print ('    [+] strateg',strateg)
    ### Выставляем цену согласно процента
    if procent != 0 and price == 0: 
        if torg == 'Купить':
            url = 'http://192.168.0.85:5000/exchanges_ask/1111-2222-1111-3333-5555/binance/'+symbol+'/'
            r = requests.get(url)
            parsed_string = json.loads(r.text)
            ask = float(str((parsed_string)))          
            new_price = ask * (100 + float(procent)) / 100
            print ('        [+] Проставляем цену. Текущая:',ask,'Новая:',new_price)
            price = new_price
            sql = "UPDATE openorder SET price = "+str(new_price)+" WHERE id = "+str(id)+""
            cursor.execute(sql)
            db.commit()
    act = ''
    ask_bid = 0


    ### Проставляем цену на паре. Которыя есть в ордере
    if torg == 'Купить':
        url = 'http://192.168.0.85:5000/exchanges_ask/1111-2222-1111-3333-5555/binance/'+symbol+'/'
        r = requests.get(url)
        parsed_string = json.loads(r.text)
        ask = float(str((parsed_string)))
        if ask >= price and strateg == '':
            act = 'Ожидаем понижение цены (Покупка)'
        else:    
            act = 'Выполнение ордера'
            sql = "UPDATE openorder SET price_t = "+str(ask)+" WHERE id = "+str(id)+""
            cursor.execute(sql)
            db.commit()
            sql = "UPDATE openorder SET status = 'closed' WHERE id = "+str(id)+""
            cursor.execute(sql)
            db.commit()
        print ('        [+]',act)    
        ask_bid = ask


    if torg == 'Продать':
        url = 'http://192.168.0.85:5000/exchanges_bid/1111-2222-1111-3333-5555/binance/'+symbol+'/'
        r = requests.get(url)
        parsed_string = json.loads(r.text)
        bid = float(str((parsed_string)))
        if bid <= price and strateg == '':
            act = 'Ожидаем повышение цены  (Продажа)'
        else:    
            act = 'Выполнение ордера'
            sql = "UPDATE openorder SET price_t = "+str(ask)+" WHERE id = "+str(id)+""
            cursor.execute(sql)
            db.commit()
            sql = "UPDATE openorder SET status = 'closed' WHERE id = "+str(id)+""
            cursor.execute(sql)
            db.commit()
        print ('        [+]',act)      
        ask_bid = bid

    if demo == 'Yes':
        demo_list = 'Демо режим'
    else:
        demo_list = demo
    sql = "select id,name from cripto_robot where id = "+str(robot)+" limit 1"
    cursor.execute(sql)
    data_robot = cursor.fetchall()

    id_robot    = 0
    name_robot  = ''
    for rec_robot in data_robot: 
        id_robot,name_robot = rec_robot

    message_out = ''
    message_out = message_out + '[+] <b>'+str(symbol)+':'+str(ask_bid)+'</b>' + '\n'
    message_out = message_out + 'Информация № '+str(id)+'' + '\n'
    message_out = message_out + str(exchange)+' - '+str(symbol) + '\n'
    message_out = message_out + str(torg)+' - '+str(demo_list) + '\n'
    message_out = message_out + 'Price:{:15.8f}'.format(price) +'  -  ' + '{:15.8f}'.format(ask_bid) + '\n'
    message_out = message_out + str(act) + '\n'
    message_out = message_out + 'Стратегия: ' +str(strateg)+ '\n'
    message_out = message_out + '\n'


    if id_robot != 0: 
        message_out = message_out + '<b>Робот</b>' + '\n'
        message_out = message_out + 'Номер робота: ' + str(id_robot)+' - '+str(name_robot)+'\n'
        message_out = message_out + 'Выполнение циклов: ' + '\n'
        message_out = message_out + 'Стоп: ' + '\n'

        from telebot import types
        markup = types.InlineKeyboardMarkup(row_width=4)
        tx1    = iz_func.get_namekey ('Отключить робота',namebot)
        cl1    = 'Отключить_'+str(id)
        mn2    = types.InlineKeyboardButton(text=tx1,callback_data = cl1)
        markup.add(mn2)     
   
    if id_robot == 0:  
        from telebot import types
        markup = types.InlineKeyboardMarkup(row_width=4)
        tx1    = iz_func.get_namekey ('Отключить ордер',namebot)
        cl1    = 'Отключить_'+str(id)
        mn2    = types.InlineKeyboardButton(text=tx1,callback_data = cl1)
        markup.add(mn2)     

    message_send = iz_func.bot_send (user_id,message_out,markup,bot,namebot)



sql = "select id,symbol,price_buy,torg from cripto_robot where strateg = 'RSI' and (torg = 'Buy') "  ### torg = 'Sell' or 
cursor.execute(sql)
data = cursor.fetchall()
message_out2 = ''
message_out2 = message_out2 + '<b>Итоговый отчет RSI №' +str(1)+'</b>\n'
message_out2 = message_out2 + '\n'
kl = 0
kl2 = 0
nm = 1

from telebot import types
markup = types.InlineKeyboardMarkup(row_width=4)
tx1    = iz_func.get_namekey ('Продать ордер',namebot)
cl1    = 'Продать ордер'+str(id)
mn2    = types.InlineKeyboardButton(text=tx1,callback_data = cl1)
markup.add(mn2)   

for rec in data:     
    kl = kl + 1
    kl2 = kl2 +1
    id,symbol,price_buy,torg = rec
    print ('[+]',kl,symbol,torg)

    if torg == 'Buy':
        url = 'http://192.168.0.85:5000/exchanges_bid/1111-2222-1111-3333-5555/binance/'+symbol+'/'
        r = requests.get(url)
        parsed_string = json.loads(r.text)
        bid = float(str((parsed_string)))
        procent = bid * 100 / price_buy
        if procent > 100:
            message_out2 = message_out2 +'<b>'+ str(kl2)+' '+ str(symbol) +'  '+str(procent)+'</b>\n'
        else:    
            message_out2 = message_out2 + str(kl2)+' '+ str(symbol) +'  '+str(procent)+'\n'

        if procent < 98:
            markup = ''
            message_out3 = ''
            message_out3 = message_out3 + '<b>Cтоплос</b>' + '\n'
            message_out3 = message_out3 + '' + '\n'
            message_out3 = message_out3 + str(symbol) + '\n'
            message_send = iz_func.bot_send (user_id,message_out3,markup,bot,namebot)    
            message_out2 = message_out2 + '<b>Cтоплос</b>' + '\n'
            print ('    [+] Запускаем ордер на стоплос',procent)
            print ('    [+] ',id)
            print ('    [+] symbol:',symbol)
            print ('    [+] torg:',torg)
            sql = "UPDATE cripto_robot SET `torg` = 'StopLoss' WHERE `id` = '"+str(id)+"'"
            cursor.execute(sql)
            db.commit()   
            sql = "UPDATE cripto_robot SET `price_sell` = "+str(bid)+" WHERE `id` = '"+str(id)+"'"
            cursor.execute(sql)
            db.commit() 
            timestamp = int(time.time())
            id_rob = id
            sql = "INSERT INTO openorder (`strateg`,`robot`,`dateofbirth`,`status`,`symbol`,`exchange`,`amount_sell`,`price`,`user_id`,`amount_buy`,`torg`,`demo`) VALUES ('RSI','{}',{},'{}','{}','{}','{}','{}','{}','{}','{}','{}')".format (id_rob,timestamp,'closed',symbol,'binance',0,bid,'399838806',0,'Продать','Yes')                                                                                                                                                                               
            cursor.execute(sql)
            db.commit()  
            lastid = cursor.lastrowid
            sql = "UPDATE cripto_robot SET `sell_order` = "+str(lastid)+" WHERE `id` = '"+str(id)+"'"
            cursor.execute(sql)
            db.commit() 

        if procent > 102:
            markup = ''
            message_out3 = ''
            message_out3 = message_out3 + '<b>Закрытие</b>' + '\n'
            message_out3 = message_out3 + '' + '\n'
            message_out3 = message_out3 + str(symbol) + '\n'
            message_send = iz_func.bot_send (user_id,message_out3,markup,bot,namebot)    
            message_out2 = message_out2 + '<b>Закрытие</b>' + '\n'
            print ('    [+] Запускаем ордер на закрытие',procent)        
            print ('    [+] ',id)
            print ('    [+] symbol:',symbol)
            print ('    [+] torg:',torg)
            sql = "UPDATE cripto_robot SET `torg` = 'Profit' WHERE `id` = '"+str(id)+"'"
            cursor.execute(sql)
            db.commit()   
            sql = "UPDATE cripto_robot SET `price_sell` = "+str(bid)+" WHERE `id` = '"+str(id)+"'"
            cursor.execute(sql)
            db.commit() 
            timestamp = int(time.time())
            id_rob = id
            sql = "INSERT INTO openorder (`strateg`,`robot`,`dateofbirth`,`status`,`symbol`,`exchange`,`amount_sell`,`price`,`user_id`,`amount_buy`,`torg`,`demo`) VALUES ('RSI','{}',{},'{}','{}','{}','{}','{}','{}','{}','{}','{}')".format (id_rob,timestamp,'closed',symbol,'binance',0,bid,'399838806',0,'Продать','Yes')                                                                                                                                                                               
            cursor.execute(sql)
            db.commit()  
            lastid = cursor.lastrowid
            sql = "UPDATE cripto_robot SET `sell_order` = "+str(lastid)+" WHERE `id` = '"+str(id)+"'"
            cursor.execute(sql)
            db.commit()         

        if kl>40:
            print ('    [+] Обнуление')
            message_send = iz_func.bot_send (user_id,message_out2,markup,bot,namebot)    
            kl = 0
            message_out2 = ''
            nm = nm + 1
            message_out2 = message_out2 + '<b>Итоговый отчет RSI № ' +str(nm) + '</b>\n'
            message_out2 = message_out2 + '\n'    

    if torg == 'Buy':
        pass       



message_send = iz_func.bot_send (user_id,message_out2,markup,bot,namebot)    

print ('[+] Ожидаем 15 мин')
time.sleep (60*15)        
exit (0)



