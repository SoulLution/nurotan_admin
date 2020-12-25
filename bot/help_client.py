#!/usr/bin/python
# -*- coding: utf-8
# ОПИСАНИЕ БОТА: %%ОписаниеБота%%
# АВТОР БОТА   : %%АвторБота%%
# ТЕЛЕГРАММ АВТОРА : %%ТелеграмиАвтора%%
# Доработки:

import telebot
import time
from telebot import apihelper
from telebot import types

import json

ip   = '196.18.15.10'
port = '8000'
password  = 'ExejJZ'
userproxy = 'J22FvE'
proxy = {'https':'http://{}:{}@{}:{}'.format(password,userproxy,ip,port)}
print ('[+]',proxy)
apihelper.proxy = proxy 

namebot = "@BT_trader_bot"
token = '455101142:AAFwuOUG4FEIvFnIFO6PoRIRLBFAQtz8uMI'

#import pymysql
#db = pymysql.connect("127.0.0.1","izofen","podkjf4","main" ,use_unicode=True, charset="utf8mb4" )   



def fill_menu (user_id,menu_command):
    namebot = "@Help_client_bot"
    if menu_command.find ('%%sell_id%%') != -1:
        sell_id = iz_func.load_variable (user_id,"Покупка_id",namebot)
        menu_command = menu_command.replace("%%sell_id%%", "_"+str(sell_id))
    return menu_command    

def fill_message (user_id,message_out):
    namebot = "@BT_trader_bot"
    return message_out

def get_price (user_id):
    return 0.01
    
def get_message (user_id,message_in):
    namebot = "@BT_trader_bot"
    import pymysql
    db = pymysql.connect("127.0.0.1","izofen","podkjf4","main" ,use_unicode=True, charset="utf8mb4" )  
    cursor = db.cursor()
    message_out = message_in
    menu = ''
    sql = "SELECT id,tekegram,text,input,menu,status FROM message where tekegram = '"+str(namebot)+"' and input = '"+str(message_in)+"'"
    cursor.execute(sql)
    data = cursor.fetchall()
    for rec in data: 
        id_s,tekegram_s,text_s,input_s,menu_s,status_s = rec
        message_out = text_s
        menu  = menu_s
    return message_out,menu
    
def send_message (user_id,message_in,status):
    ## Поиск входящего сообщения
    import pymysql
    db = pymysql.connect("127.0.0.1","izofen","podkjf4","main" ,use_unicode=True, charset="utf8mb4" )  
    cursor = db.cursor()
    message_out = message_in
    menu = ''
    sql = "SELECT id,tekegram,text,input,menu,status FROM message where tekegram = '"+str(namebot)+"' and input = '"+str(message_in)+"' and status = '"+str(status)+"'"
    met_find = 0
    cursor.execute(sql)
    data = cursor.fetchall()
    for rec in data: 
        id_s,tekegram_s,text_s,input_s,menu_s,status_s = rec
        message_out = text_s
        menu  = menu_s
        met_find = met_find + 1
        
    answer = 'не отправлено'
    if met_find == 0:
        print ('[+] Сообщения не найдено в базе данных')
        if status == 'S':
            bot.send_message(user_id,message_out,parse_mode='HTML')
            answer = 'отправлено'
            print ('[+] Запись нового сообщения в базу')
            #sql = "INSERT INTO message (tekegram,input,menu,status,text) VALUES ('{}','{}','{}','{}','{}')".format (namebot,message_in,'',"S",message_in)
            #cursor.execute(sql)
            #db.commit()
    else:
        message_out = fill_message (user_id,message_out)
        print ('[+] Ответ: {}, меню: {}'.format(message_out,menu))            

        if menu == '':
            bot.send_message(user_id,message_out,parse_mode='HTML')
            answer = 'отправлено'
        else:
            cursor = db.cursor()
            sql = "select id,name,bot,vid,menu01,menu02,menu03,menu11,menu12,menu13,menu21,menu22,menu23,line from menu where name = '"+str(menu)+"' and bot = '"+namebot+"'"
            cursor.execute(sql)
            data = cursor.fetchall()
            name_m = ""
            for rec in data: 
                id_m,name_m,bot_m,vid_m,menu01_m,menu02_m,menu03_m,menu11_m,menu12_m,menu13_m,menu21_m,menu22_m,menu23_m,line_m = rec
            if name_m != "":  
                if vid_m == "select":
                    markup = iz_func.menu_stat (menu01_m,menu02_m,menu03_m,menu11_m,menu12_m,menu13_m,menu21_m,menu22_m,menu23_m)
                if vid_m == "command": 
                    menu01_m = fill_menu (user_id,menu01_m)
                    #print ('menu01_m',menu01_m)
                    markup = iz_func.menu_command (menu01_m,menu02_m,menu03_m,menu11_m,menu12_m,menu13_m,menu21_m,menu22_m,menu23_m)
                bot.send_message(user_id,message_out,parse_mode='HTML',reply_markup=markup)
                answer = 'отправлено'
    return answer





def get_info_order (id_order):


    import pymysql
    db = pymysql.connect("127.0.0.1","izofen","podkjf4","main" ,use_unicode=True, charset="utf8mb4" )   
    cursor = db.cursor()

    sql = "select id,exchange,piar,side,price,answer,status,user_id,demo,robot,amount,next,test_order,test_time from exchange where id = "+str(id_order)+""
    cursor.execute(sql)
    data = cursor.fetchall()
    for rec in data: 
        id_exchange,exchange_exchange,piar_exchange,side_exchange,price_exchange,answer_exchange,status_exchange,user_id_exchange,demo_exchange,robot_exchange,amount_exchange,next_exchange,test_order,test_time = rec
    return id_exchange,exchange_exchange,piar_exchange,side_exchange,price_exchange,answer_exchange,status_exchange,user_id_exchange,demo_exchange,robot_exchange,amount_exchange,next_exchange,test_order,test_time       


if __name__ == "__main__":
    import iz_func
    bot   = telebot.TeleBot(token)
    print (iz_func.c8+"[+]",namebot,iz_func.c0)
    print ('Ver 3.1.0, Аvtor: @Pi_3dot141 (https://t.me/Pi_3dot141)')

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    print ('===================================')
    username   = message.from_user.username
    first_name = message.from_user.first_name
    last_name  = message.from_user.last_name
    user_id    = message.from_user.id
    date       = message.date
    message_in = message.text
    print ('[+] Входящие сообшеие: {}'.format(message_in))
    import pymysql
    db = pymysql.connect("127.0.0.1","izofen","podkjf4","main" ,use_unicode=True, charset="utf8mb4" )  
    print ('[+] Новый пользователь в боте: {}'.format(user_id))
    iz_func.save_variable (user_id,"status","",namebot)
    iz_func.save_FIO (user_id,username,namebot,first_name,last_name)
    iz_func.referal  (user_id,namebot,message_in)
    message_send = send_message (user_id,message_in,'*')

@bot.message_handler(content_types=["text"])
def repeat_all_messages(message):
    user_id     = message.from_user.id
    message_in  = message.text
    username    = message.from_user.username
    first_name  = message.from_user.first_name
    last_name   = message.from_user.last_name
    date        = message.date
    status      = iz_func.load_variable (user_id,"status",namebot)
    print ('[+] Входящие сообшение: {}'.format(message_in))
    message_send = send_message (user_id,message_in,'*')

    print ('==================================')

    if status.find ('Фильтр') != -1:
        iz_func.save_variable (user_id,"Фильтр",message_in,namebot) 
        iz_func.save_variable (user_id,"status","",namebot) 
        message_send = send_message (user_id,"Фильтр включен",'*')
        message_out,keyboard = list_tovar (user_id)
        bot.send_message(user_id,message_out,parse_mode='HTML',reply_markup=keyboard)
 
    if message_in.find ('➕Купить') != -1:
        iz_func.save_variable (user_id,"Номер товара",str(0),namebot)
        message_out,keyboard = list_tovar (user_id)
        bot.send_message(user_id,message_out,parse_mode='HTML',reply_markup=keyboard)


    if message_in.find ('Выставленные роботы') != -1:
        print ('[+] Вывод найденных роботов')
        import pymysql
        db = pymysql.connect("127.0.0.1","izofen","podkjf4","main" ,use_unicode=True, charset="utf8mb4" )  
        cursor = db.cursor()
        sql = "select * from robots where 1=1"
        cursor.execute(sql)
        data = cursor.fetchall()

        for rec in data: 
            id_l,exchange_l,piar,name,user_id_l,order,exchange_id_buy,status,demo,buy,sell,amount,exchange_id_sell,comment,V1,V2,name_V1,name_V2,robot_up,robot_down,active,step = rec
            message_out,menu = get_message (user_id,'Описание робота')
            print ('l=',exchange_l)
            message_out = message_out.replace ('%%id%%',str(id_l))
            message_out = message_out.replace ('%%exchange%%',str(exchange_l))
            message_out = message_out.replace ('%%piar%%',str(piar))
            message_out = message_out.replace ('%%name%%',str(name))
            message_out = message_out.replace ('%%user_id_l%%',str(user_id_l))
            message_out = message_out.replace ('%%exchange_id_buy%%',str(exchange_id_buy))
            message_out = message_out.replace ('%%exchange_id_sell%%',str(exchange_id_sell))
            message_out = message_out.replace ('%%status%%',str(status))
            message_out = message_out.replace ('%%demo%%',str(demo))
            message_out = message_out.replace ('%%buy%%',str(buy))
            message_out = message_out.replace ('%%sell%%',str(sell))
            message_out = message_out.replace ('%%amount%%',str(amount))
            
            message_out = message_out.replace ('%%comment%%',str(comment))
            message_out = message_out.replace ('%%step%%',str(step))
    
 
            if exchange_id_buy == None:
                exchange_id_buy  = 0

            id_order = 0
            st = ''
            if exchange_id_buy == 0:
                id_order = exchange_id_sell
                st = 'Продажа'    


            if exchange_id_sell == 0:
                id_order = exchange_id_buy
                st = 'Покупка'  



            print ('[+] exchange_id_buy ',exchange_id_buy,'exchange_id_sell',exchange_id_sell)      
                        
            id_exchange,exchange_exchange,piar_exchange,side_exchange,price_exchange,answer_exchange,status_exchange,user_id_exchange,demo_exchange,robot_exchange,amount_exchange,next_exchange,test_order,test_time = get_info_order (id_order)

            message_out = message_out.replace ('%%id_exchange%%',str(id_exchange))
            message_out = message_out.replace ('%%exchange_exchange%%)',str(exchange_exchange))
            message_out = message_out.replace ('%%piar_exchange%%',str(piar_exchange))
            message_out = message_out.replace ('%%side_exchange%%',str(side_exchange))
            message_out = message_out.replace ('%%price_exchange%%',str(price_exchange))


            answer = answer_exchange
            answer = answer.replace("%%<1>%%","'")
            answer = answer.replace('%%<2>%%','"')
            response = json.loads(answer)

            orderId = ''
            status  = ''

            if answer.find ('error') != -1:   ### Ошибка в выставлении ордера
                status = "error"
            else:    
                orderId = response['id']
                status  = response['status']

            message_out = message_out.replace ('%%orderId%%',str(orderId))
            message_out = message_out.replace ('%%status%%',str(status))        

            message_out = message_out.replace ('%%answer_exchange%%',str(answer_exchange))

            message_out = message_out.replace ('%%status_exchange%%',str(status_exchange))
            message_out = message_out.replace ('%%user_id_exchange%%',str(user_id_exchange))
            message_out = message_out.replace ('%%demo_exchange%%',str(demo_exchange))
            message_out = message_out.replace ('%%robot_exchange%%',str(robot_exchange))
            message_out = message_out.replace ('%%amount_exchange%%',str(amount_exchange))
            message_out = message_out.replace ('%%next_exchange%%',str(next_exchange))

            message_out = message_out.replace ('%%test_time%%',str(test_time))
            message_out = message_out.replace ('%%test_time%%',str(test_time))




            print ('[+] message_out',message_out)

            bot.send_message(user_id,message_out,parse_mode='HTML')                    
    

 

@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    if call.message:
        user_id = call.message.chat.id
        message_in = call.data
        status      = iz_func.load_variable (user_id,"status",namebot)
        status      = iz_func.load_variable (user_id,"status",namebot)
        print ('[+] user_id',user_id)
        print ('[+] message_in',message_in)
        print ('[+] status',status)
        message_send = send_message (user_id,message_in,'*')
        
        if call.data.find ("BTC") != -1:
            #message_send = send_message (user_id,"Счет на опллату в  BTC",'L')
            
            amount_s = 0.001
            if call.data == "0.001 BTC":
                amount_s = 0.001
            if call.data == "0.002 BTC":
                amount_s = 0.002
            if call.data == "0.003 BTC":
                amount_s = 0.003
                
                
            iz_func.save_variable (user_id,"Сумма пополнения",str(amount_s),namebot) 
            lastid,checkout_url,user_id,address,amount = chek (amount_s,user_id)
            
            iz_func.save_variable (user_id,"НомерСчета",str(lastid),namebot) 
            iz_func.save_variable (user_id,"checkout_url",str(checkout_url),namebot) 
            iz_func.save_variable (user_id,"address",str(address),namebot) 
            iz_func.save_variable (user_id,"Сумма оплаты",str(amount),namebot) 
            
            #message_out = message_out.replace("%%НомерСчета0.001%%", str(lastid))
            #message_out = message_out.replace("%%checkout_url%%", str(checkout_url))
            #message_out = message_out.replace("%%user_id%%", str(user_id))
            #message_out = message_out.replace("%%address%%", str(address))
            #message_out = message_out.replace("%%Сумма оплаты%%", str(amount)+" BTC")
            message_send = send_message (user_id,"Счет на опллату в  BTC",'*')
        
        if call.data.find ("Назад") != -1:
            message_out,keyboard = list_tovar (user_id)
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=message_out,parse_mode='HTML',reply_markup=keyboard) ## ,reply_markup=markup

        if call.data.find ("Проверить") != -1:
            id_sdelki = message_in.replace("Проверить_","")
            import pymysql
            db = pymysql.connect("127.0.0.1","izofen","podkjf4","main" ,use_unicode=True, charset="utf8mb4" )  
            cursor = db.cursor()
            sql = "select id,user_id,name,comment,pl01,pl02,pl03,pl04,pl05,pl06,pl07,pl08,pl09,pl10,pl11,pl12,pl13,pl14,pl15,pl16,data_buy  from product where id = '"+str(id_sdelki)+"' limit 1"
            cursor.execute(sql)
            data = cursor.fetchall()
            for rec in data: 
                id,user_id_l,name_l,comment,pl01,pl02,pl03,pl04,pl05,pl06,pl07,pl08,pl09,pl10,pl11,pl12,pl13,pl14,pl15,pl16,data_buy = rec
            print ("[+]",id,user_id_l,name_l,comment,pl01,pl02,pl03,pl04,pl05,pl06,pl07,pl08,pl09,pl10,pl11,pl12,pl13,pl14,pl15,pl16,data_buy)  


            import time
            timestamp = int(time.time())
            longT = (timestamp - data_buy)//60
            
            print ('[+] longT',longT)
            
            if longT < 5:
                url  = "http://192.168.0.85";
                url  = url + "/pl4/api.try2.example.php";
                url  = url + "?cards="+str(name_l)+"<->"+str(pl02)+"<->"+str(pl03)
                url  = url + "&rid="+str(id)
                url  = url + "&metod=set"
                print (url)    
                import requests
                r = requests.get(url)
                testID = r.text
                print (testID)
                message_send = send_message (user_id,"Тестирование товара",'*')
                time.sleep(60)
                url  = "http://192.168.0.85";
                url  = url + "/pl4/api.try2.example.php";
                url  = url + "?cards="+str(testID);
                url  = url + "&rid="+str(id)
                url  = url + "&metod=get"
                print (url)    
                r = requests.get(url)
                answer = r.text
                print (answer)
                iz_func.save_variable (user_id,"Ответ тестирования",str(answer),namebot) 
                message_send = send_message (user_id,"Ответ тестирования",'*')
                sql = "UPDATE product SET answer = '"+str(answer)+"' WHERE `id` = "+str(id_sdelki)+""
                cursor.execute(sql)
                db.commit()
            else:  
                message_send = send_message (user_id,"Тестирование невозможно",'*')            
            
        if call.data.find ("Купить") != -1:
            id_sdelki = message_in.replace("Купить_","")
            import pymysql
            db = pymysql.connect("127.0.0.1","izofen","podkjf4","main" ,use_unicode=True, charset="utf8mb4" )  
            cursor = db.cursor()
            sql = "select id,user_id,name,comment,pl01,pl02,pl03,pl04,pl05,pl06,pl07,pl08,pl09,pl10,pl11,pl12,pl13,pl14,pl15,pl16  from product where id = '"+str(id_sdelki)+"' limit 1"
            cursor.execute(sql)
            data = cursor.fetchall()
            for rec in data: 
                id,user_id_l,name_l,comment,pl01,pl02,pl03,pl04,pl05,pl06,pl07,pl08,pl09,pl10,pl11,pl12,pl13,pl14,pl15,pl16 = rec
                iz_func.save_variable (user_id,"name",str(name_l),namebot)
                iz_func.save_variable (user_id,"pl01",str(pl01),namebot)
                iz_func.save_variable (user_id,"pl02",str(pl02),namebot)
                iz_func.save_variable (user_id,"pl03",str(pl03),namebot)
                iz_func.save_variable (user_id,"pl04",str(pl04),namebot)
                iz_func.save_variable (user_id,"pl05",str(pl05),namebot)
                iz_func.save_variable (user_id,"pl06",str(pl06),namebot)
                iz_func.save_variable (user_id,"pl07",str(pl07),namebot)
                iz_func.save_variable (user_id,"pl08",str(pl08),namebot)
                iz_func.save_variable (user_id,"pl09",str(pl09),namebot)
                iz_func.save_variable (user_id,"pl10",str(pl10),namebot)
                iz_func.save_variable (user_id,"pl11",str(pl11),namebot)
                iz_func.save_variable (user_id,"pl12",str(pl12),namebot)
                iz_func.save_variable (user_id,"pl13",str(pl13),namebot)
                iz_func.save_variable (user_id,"pl14",str(pl14),namebot)
                iz_func.save_variable (user_id,"pl15",str(pl15),namebot)
                iz_func.save_variable (user_id,"pl16",str(pl16),namebot)        
            price = get_price (pl04)
            balansBTC   = iz_func.load_variable (user_id,"balansBTC",namebot)
            if balansBTC == '':balansBTC = 0
            balansBTC = float(balansBTC)
            if balansBTC >= price:
                message_out,munu = get_message (user_id,"Вы купили товар")
                message_out = fill_message (user_id,message_out)    
                keyboard = types.InlineKeyboardMarkup(row_width=4)
                key01 = types.InlineKeyboardButton(text="Назад", callback_data  = "Назад")
                key02 = types.InlineKeyboardButton(text="Проверить", callback_data  = "Проверить_"+str(id_sdelki))
                keyboard.add(key01,key02)
                bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=message_out,parse_mode='HTML',reply_markup=keyboard) ## ,reply_markup=markup        
                sql = "UPDATE product SET user_id = '"+str(user_id)+"' WHERE `id` = "+str(id_sdelki)+""
                cursor.execute(sql)
                db.commit()
                import time
                timestamp = int(time.time())
                sql = "UPDATE product SET data_buy = '"+str(timestamp)+"' WHERE `id` = "+str(id_sdelki)+""
                cursor.execute(sql)
                db.commit()
                balansBTC = balansBTC - price
                iz_func.load_variable (user_id,"balansBTC",str(balansBTC),namebot)
                
            else:
                message_out,munu = get_message (user_id,"Недостаточно средств") 
                keyboard = types.InlineKeyboardMarkup(row_width=4)
                key01 = types.InlineKeyboardButton(text="Назад", callback_data  = "Назад")
                key02 = types.InlineKeyboardButton(text="Пополнить", callback_data  = "Пополнить")
                keyboard.add(key01,key02)
                message_out = fill_message (user_id,message_out)
                bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=message_out,parse_mode='HTML',reply_markup=keyboard) ## ,reply_markup=markup        
            
        if call.data.find ("Сменить вернуться") != -1:
            nomerbase = iz_func.load_variable (user_id,"Номер товара",namebot)
            if nomerbase == '': nomerbase = 0
            nomerbase = int(nomerbase)
            nomerbase = nomerbase - 1
            iz_func.save_variable (user_id,"Номер товара",str(nomerbase),namebot)
            message_out,keyboard = list_tovar (user_id)
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=message_out,parse_mode='HTML',reply_markup=keyboard) ## ,reply_markup=markup

        if call.data.find ("Сменить вперед") != -1:
            nomerbase = iz_func.load_variable (user_id,"Номер товара",namebot)
            if nomerbase == '': nomerbase = 0
            nomerbase = int(nomerbase)
            nomerbase = nomerbase + 1
            iz_func.save_variable (user_id,"Номер товара",str(nomerbase),namebot)
            message_out,keyboard = list_tovar (user_id)
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=message_out,parse_mode='HTML',reply_markup=keyboard) ## ,reply_markup=markup
        
        if call.data.find ("Пополнить") != -1:
            message_send = send_message (user_id,"🚀Пополнить",'*')

        if call.data.find ("Внести сумму в ручную") != -1:
            iz_func.save_variable (user_id,"status","Внести сумму в ручную",namebot)
            message_send = send_message (user_id,"Внести сумму в ручную",'L')





bot.polling()    



















