#! /usr/bin/env python
# -*- coding: utf-8 -*-
import time
import datetime


def connect ():
    import pymysql
    db = pymysql.connect("127.0.0.1","izofen","podkjf4","main" ,use_unicode=True, charset="utf8mb4" )
    # db = pymysql.connect("185.22.64.75","izofen","podkjf4","main" ,use_unicode=True, charset="utf8mb4" )
    cursor = db.cursor()
    return db,cursor

def get_namekey (name,namebot):  
    answer    = name
    db,cursor = connect ('')
    sql = "select id,name,about from keyname where (namebot = '"+str(namebot)+"' or namebot = '') and name = '"+str(name)+"' limit 1"
    cursor.execute(sql)
    results = cursor.fetchall()    
    for row in results:
        id,name,about = row
        answer    = about
    return answer

def select (user_id,namebot,bot,list):    
    from telebot import types
    markup = types.InlineKeyboardMarkup(row_width=5)
    for line in list:
        n   = 0
        mn1 = ''
        mn2 = ''
        mn3 = ''
        mn4 = ''
        mn5 = ''
        print ('[+]',line)
        for gr in line:
            n = n + 1
            print ('    [+]',n,gr)
            if n == 1:
                mn1 = types.InlineKeyboardButton(text=gr[0],callback_data=gr[1])
            if n == 2:
                mn2 = types.InlineKeyboardButton(text=gr[0],callback_data=gr[1])
            if n == 3:
                mn3 = types.InlineKeyboardButton(text=gr[0],callback_data=gr[1])
            if n == 4:
                mn4 = types.InlineKeyboardButton(text=gr[0],callback_data=gr[1])
            if n == 5:
                mn5 = types.InlineKeyboardButton(text=gr[0],callback_data=gr[1])                
        if mn1  == '' and mn2  == '' and mn3  == '' and mn4  == '' and mn5  == '':
            pass
        if mn1  != '' and mn2  == '' and mn3  == '' and mn4  == '' and mn5  == '':    
            markup.add(mn1)
        if mn1  != '' and mn2  != '' and mn3  == '' and mn4  == '' and mn5  == '':
            markup.add(mn1,mn2)
        if mn1  != '' and mn2  != '' and mn3  != '' and mn4  == '' and mn5  == '':    
            markup.add(mn1,mn2,mn3)
        if mn1  != '' and mn2  != '' and mn3  != '' and mn4  != '' and mn5  == '':    
            markup.add(mn1,mn2,mn3,mn4)
        if mn1  != '' and mn2  != '' and mn3  != '' and mn4  != '' and mn5  != '':    
            markup.add(mn1,mn2,mn3,mn4,mn5)
    return markup    

def menu_command (suf,menu01,menu02,menu03,menu11,menu12,menu13,menu21,menu22,menu23,menu31,menu32,menu33,menu41,menu42,menu43,menu51,menu52,menu53):

    from telebot import types
    markup = types.InlineKeyboardMarkup(row_width=4)

    if menu01 != "":
        mn01 = ""
        mn02 = ""
        mn03 = ""

        if menu01 != "":
            mn01 = types.InlineKeyboardButton(text=menu01,callback_data = suf+'_'+menu01)        
        if menu02 != "":
            mn02 = types.InlineKeyboardButton(text=menu02,callback_data = suf+'_'+menu02)
        if menu03 != "":
            mn03 = types.InlineKeyboardButton(text=menu03,callback_data = suf+'_'+menu03)
            
        if mn01 != '' and mn02 == '' and mn03 == '':
            markup.add(mn01)
        if mn01 != '' and mn02 != '' and mn03 == '':
            markup.add(mn01,mn02)
        if mn01 != '' and mn02 != '' and mn03 != '':
            markup.add(mn01,mn02,mn03)

    if menu11 != "": 
        mn11 = ""
        mn12 = ""
        mn13 = ""

        if menu11 != "":
            mn11 = types.InlineKeyboardButton(text=menu11,callback_data=suf+'_'+menu11)        
        if menu12 != "":
            mn12 = types.InlineKeyboardButton(text=menu12,callback_data=suf+'_'+menu12)
        if menu13 != "":
            mn13 = types.InlineKeyboardButton(text=menu13,callback_data=suf+'_'+menu13)        
        
        if mn11 != '' and mn12 == '' and mn13 == '':
            markup.add(mn11)            
        if mn11 != '' and mn12 != '' and mn13 == '':
            markup.add(mn11,mn12)
        if mn11 != '' and mn12 != '' and mn13 != '':
            markup.add(mn11,mn12,mn13)


    if menu21 != "": 
        mn21 = ""
        mn22 = ""
        mn23 = ""

        if menu21 != "":
            mn21 = types.InlineKeyboardButton(text=menu21,callback_data=suf+'_'+menu21)
        if menu22 != "":
            mn22 = types.InlineKeyboardButton(text=menu22,callback_data=suf+'_'+menu22)
        if menu23 != "":
            mn23 = types.InlineKeyboardButton(text=menu23,callback_data=suf+'_'+menu23)
        
        if mn21 != '' and mn22 == '' and mn23 == '':
            markup.add(mn21)            
        if mn21 != '' and mn22 != '' and mn23 == '':
            markup.add(mn21,mn22)
        if mn21 != '' and mn22 != '' and mn23 != '':
            markup.add(mn21,mn22,mn23)

    if menu31 != "": 
        mn31 = ""
        mn32 = ""
        mn33 = ""

        if menu31 != "":
            mn31 = types.InlineKeyboardButton(text=menu31,callback_data= suf+'_'+menu31)
            pass
        if menu32 != "":
            #mn32 = types.InlineKeyboardButton(text=menu32,callback_data=suf+'_'+menu32)
            pass
        if menu33 != "":
            #mn33 = types.InlineKeyboardButton(text=menu33,callback_data=suf+'_'+menu33)
            pass
        
        if mn31 != '' and mn32 == '' and mn33 == '':
            markup.add(mn31)            
        if mn31 != '' and mn32 != '' and mn33 == '':
            markup.add(mn21,mn22)
        if mn31 != '' and mn32 != '' and mn33 != '':
            markup.add(mn21,mn22,mn23)


    if menu41 != "": 
        mn41 = ""
        mn42 = ""
        mn43 = ""

        if menu41 != "":
            mn41 = types.InlineKeyboardButton(text=menu41,callback_data=suf+'_'+menu41)
            pass
        if menu42 != "":
            #mn42 = types.InlineKeyboardButton(text=menu42,callback_data=suf+'_'+menu42)
            pass
        if menu43 != "":
            #mn43 = types.InlineKeyboardButton(text=menu43,callback_data=suf+'_'+menu43)        
            pass
        
        if mn41 != '' and mn42 == '' and mn43 == '':
            markup.add(mn41)            
        if mn41 != '' and mn42 != '' and mn43 == '':
            markup.add(mn41,mn42)
        if mn41 != '' and mn42 != '' and mn43 != '':
            markup.add(mn41,mn42,mn43)



    if menu51 != "": 
        mn51 = ""
        mn52 = ""
        mn53 = ""

        if menu51 != "":
            #mn51 = types.InlineKeyboardButton(text=menu51,callback_data=suf+'_'+menu51)
            pass
        if menu52 != "":
            #mn52 = types.InlineKeyboardButton(text=menu52,callback_data=suf+'_'+menu52)
            pass
        if menu53 != "":
            #mn53 = types.InlineKeyboardButton(text=menu53,callback_data=suf+'_'+menu53)        
            pass
        
        if mn51 != '' and mn52 == '' and mn53 == '':
            markup.add(mn51)            
        if mn51 != '' and mn52 != '' and mn53 == '':
            markup.add(mn51,mn52)
        if mn51 != '' and mn52 != '' and mn53 != '':
            markup.add(mn51,mn52,mn53)

    return markup  
          
def referal (user_id,namebot,message_in):
    #import pymysql
    #db = pymysql.connect("127.0.0.1","izofen","podkjf4","main" ,use_unicode=True, charset="utf8mb4" )        
    #cursor = db.cursor()  
    db,cursor = connect (namebot)
    sql = "select id,user_id,bot,input,output from referalka where bot = '"+namebot+"' and user_id = '"+str(user_id)+"' limit 10"
    cursor.execute(sql)
    label = False
    data = cursor.fetchall()
    for rec in data: 
        print ('{}[+] Реферальная ссылка обнаружена{}'.format(n,s))
        label = True
        id,user_id,botname,input,output = rec
    if label == False:
        print ('[+] Создаем реферальную ссылку')
        cursor = db.cursor()  
        sql = "INSERT INTO referalka (`user_id`,`bot`,`input`,`output`) VALUES ('{}','{}','{}','{}')".format (user_id,namebot,message_in,'')
        cursor.execute(sql)
        db.commit()        
        lastid = cursor.lastrowid
        ref = 'https://teleg.run/'+namebot+'?start='+str((lastid+1974)*28+3)
        sql = "UPDATE referalka SET output = '"+ref+"' WHERE `id` = '"+str(lastid)+"'"
        cursor.execute(sql)
        db.commit()
        sql = "UPDATE referalka SET `unique` = "+str((lastid+1974)*28+3)+" WHERE `id` = '"+str(lastid)+"'"
        cursor.execute(sql)
        db.commit()

def save_variable (user_id,variable,value,namebot):
    db,cursor = connect ()
    sql = "select id,user_id,variable,namebot,znachen,dateofbirth from setting where user_id = '"+str(user_id)+"' and  variable = '"+variable+"' and namebot = '"+namebot+"' limit 1"
    label = "новый"
    cursor.execute(sql)
    results = cursor.fetchall()    
    for row in results:
        label = "в базе"
    if label == "новый":
        sql = "INSERT INTO setting (`user_id`,`variable`,`namebot`,`znachen`) VALUES ('{}','{}','{}','{}')".format (user_id,variable,namebot,value)
        cursor.execute(sql)
        db.commit()
    else:
        sql = "UPDATE setting SET znachen = '"+value+"' WHERE (`user_id` = '"+str(user_id)+"' and variable = '"+variable+"' and namebot = '"+namebot+"')"
        cursor.execute(sql)
        db.commit()

def load_variable (user_id,variable,namebot):
    db,cursor = connect ()
    variable_out = ''
    sql = "select id,user_id,variable,namebot,znachen,dateofbirth  from setting where user_id = '"+str(user_id)+"' and  variable = '"+variable+"' and namebot = '"+namebot+"' limit 1"
    cursor.execute(sql)
    results = cursor.fetchall()    
    for row in results:
        id,user_id,variable,bot_name,znachen,dateofbirth = row
        variable_out = znachen;
    return variable_out

def save_FIO (user_id,username,namebot,first_name,last_name):
    import time
    timestamp = int(time.time())
    db,cursor = connect ()
    sql = "select id,user_id,username,namebot,firstname,lastname from users where user_id = '"+str(user_id)+"' and namebot = '"+namebot+"'limit 1"
    cursor.execute(sql)
    results = cursor.fetchall()        
    label = "новый"    
    for row in results:    
        label = "в базе"
    if label == "новый":
        timestamp = int(time.time())
        cursor = db.cursor()  
        sql = "INSERT INTO users (`user_id`,`username`,`namebot`,`firstname`,`lastname`,`timestamp`) VALUES ('{}','{}','{}','{}','{}',{})".format (user_id,username,namebot,first_name,last_name,timestamp)
        cursor.execute(sql)
        db.commit()        
    
def load__FIO (user_id): 
    #import pymysql
    #db = pymysql.connect("127.0.0.1","izofen","podkjf4","main" ,use_unicode=True, charset="utf8mb4" )    
    #cursor = db.cursor()
    db,cursor = connect (namebot)
    sql = "select id,user_id,username,bot_name,firstname,lastname from user where user_id = '"+str(user_id)+"' limit 1"
    cursor.execute(sql)
    results = cursor.fetchall()        
    label = "новый"    
    for row in results:    
        id,user_id,username,bot_name,firstname,lastname = row
    return username,first_name,last_name

def menu_key (db,name,namebot):
    from telebot import types
    keyboard = types.InlineKeyboardMarkup(row_width=4)
    #import pymysql
    #db = pymysql.connect("127.0.0.1","izofen","podkjf4","main" ,use_unicode=True, charset="utf8mb4" )    
    #cursor = db.cursor()
    cursor = connect (namebot)
    sql = "select id,name,bot,vid,menu01,menu02,menu03 from menu where line=1 and vid = 'пипка' "
    cursor.execute(sql)
    data = cursor.fetchall()
    for rec in data:  
        id,name,bot,vid,menu01,menu02,menu03 = rec
        if menu01 != "" and menu02 == "" and menu03 == "":
            #markup.row(menu01,menu02,menu03)
            key01 = types.InlineKeyboardButton(text=menu01, callback_data = menu01)
            keyboard.add(key01)
    return keyboard
    
def menu_stat (menu01,menu02,menu03,menu11,menu12,menu13,menu21,menu22,menu23):
    from telebot import types
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    if menu01 != "":
        markup.row(menu01,menu02,menu03)
    if menu11 != "": 
        markup.row(menu11,menu12,menu13)
    if menu21 != "": 
        markup.row(menu21,menu22,menu23)
    return markup
        
def get_token (namebot):
    db,cursor = connect (namebot)
    sql = "select id,name,id_comment,token,about from bots where name = '{}' limit 1;".format(namebot)
    cursor.execute(sql)
    data = cursor.fetchall()
    id = 0
    for rec in data: 
        id,name,id_comment,token,about = rec
    if id != 0:
        return token,about
    else:
        return 'error',''

def save_log (namebot,user_id,message,tip,status,command):
    import time
    timestamp = int(time.time())
    db,cursor = connect (namebot)
    sql = "INSERT INTO log_message (`namebot`,`user_id`,`message`,`tip`,`status`,`command`,`timestamp`,`send`) VALUES ('{}','{}','{}','{}','{}','{}','{}',0)".format (namebot,user_id,message,tip,status,command,timestamp)
    cursor.execute(sql)
    db.commit()

def send_status (user_id,status_in,message_in,namebot,bot):
    db,cursor   = connect (namebot)
    menu        = ''
    picture_s   = ''
    status_out  = '' 
    message_out = ''   
    field       = ''
    sql = "SELECT id,`text`,input,menu,status,picture,status_out,field FROM message where bot_name = '"+str(namebot)+"' and status = '"+str(status_in)+"'"
    print ('sql',sql)
    met_find = 0
    cursor.execute(sql)
    data = cursor.fetchall()
    for rec in data: 
        id_s,text_s,input_s,menu_s,status_s,picture_s,status_out,field = rec
        message_out = text_s
        menu  = menu_s
        met_find = met_find + 1        
    answer = 'не отправлено'
    if met_find != 0:
        print ('[+] {}Ответ: {} {}, {}меню: {}  {}'.format(e,s,message_out,e,s,menu))            
        if menu == '' and message_out != '':
            bot_send (user_id,message_out,"",bot,namebot)
            answer = 'отправлено'
        else:
            sql = "select id,name,bot,vid,menu01,menu02,menu03,menu11,menu12,menu13,menu21,menu22,menu23,menu31,menu32,menu33,menu41,menu42,menu43,menu51,menu52,menu53,line from menu where name = '"+str(menu)+"' and bot = '"+namebot+"'"
            cursor.execute(sql)
            data = cursor.fetchall()
            name_m = ""
            for rec in data: 
                id_m,name_m,bot_m,vid_m,menu01_m,menu02_m,menu03_m,menu11_m,menu12_m,menu13_m,menu21_m,menu22_m,menu23_m,menu31,menu32,menu33,menu41,menu42,menu43,menu51,menu52,menu53,line_m = rec
            if name_m != "":  
                if vid_m == "select":
                    markup = menu_stat (menu01_m,menu02_m,menu03_m,menu11_m,menu12_m,menu13_m,menu21_m,menu22_m,menu23_m)
                if vid_m   == "command": 
                    suf = ''
                    markup = menu_command (suf,menu01_m,menu02_m,menu03_m,menu11_m,menu12_m,menu13_m,menu21_m,menu22_m,menu23_m,menu31,menu32,menu33,menu41,menu42,menu43,menu51,menu52,menu53)
                if message_out != '':    
                    bot_send (user_id,message_out,markup,bot,namebot)
                    answer = 'отправлено'
            else:
                bot_send (user_id,message_out,"",bot,namebot)
                answer = 'отправлено'
        save_variable (user_id,"status",str(status_out),namebot)



        print ('[+] field',field) 
        if field != '':
            print ('[+] Запись информации в базу данных')
            save_variable (user_id,field,str(message_in),namebot)


        if picture_s != '':
            sql = "select  id,name,bot_name,user_id,file,pyth from picture where name = '"+str(picture_s)+"' and bot_name = '"+namebot+"'"
            print ('sql',sql)
            cursor.execute(sql)
            data_p = cursor.fetchall()
            for rec_p in data_p: 
                id_p,name_p,bot_name,user_id_p,file_p,pyth_p = rec_p
                namefile = pyth_p + file_p
                print ('[+] namefile',namefile)
                photo = open(namefile, 'rb')
                bot.send_photo(user_id, photo)  



    return answer

def send_message (user_id,message_in,status,namebot,bot):
    ## Поиск входящего сообщения
    db,cursor   = connect (namebot)
    message_out = message_in
    menu        = ''
    picture_s   = ''
    status_out  = ''
    sql = "SELECT id,`text`,input,menu,status,picture,status_out,`edit` FROM message where bot_name = '"+str(namebot)+"' and input = '"+str(message_in)+"'"
    met_find = 0
    cursor.execute(sql)
    data = cursor.fetchall()
    for rec in data: 
        id_s,text_s,input_s,menu_s,status_s,picture_s,status_out,edit_out = rec
        message_out = text_s
        menu  = menu_s
        met_find = met_find + 1    

        ### Отправляем найденное сообшеие
        message_out = fill_message (user_id,message_out,namebot)
        print ('[+] {}Ответ: {} {}, {}меню: {}  {}'.format(e,s,message_out,e,s,menu))            
        if menu == '' and message_out != '':

            can_message = load_variable (user_id,message_in,namebot)
            print ('[+] Отказано отправлять пользователю: {}: {}: {}'.format(message_in,user_id,can_message))
            if can_message != 'No':
                if edit_out == 1: 
                    message_id = load_variable (user_id,"message_id",namebot)
                    bot_edit_send (user_id,message_id,message_out,'',bot,namebot)
                else:
                    bot_send (user_id,message_out,"",bot,namebot)
                answer = 'отправлено'
            else:
                print ('[!!!] Отказано отправлять пользователю: {}: {}: {}'.format(message_in,user_id,can_message))

        if menu != '' and message_out != '':
            sql = "select id,name,bot,vid,suf,menu01,menu02,menu03,menu11,menu12,menu13,menu21,menu22,menu23,menu31,menu32,menu33,menu41,menu42,menu43,menu51,menu52,menu53,line from menu where name = '"+str(menu)+"' and bot = '"+namebot+"'"
            cursor.execute(sql)
            data   = cursor.fetchall()
            name_m = ""
            markup = ""
            for rec in data: 
                id_m,name_m,bot_m,vid_m,suf,menu01_m,menu02_m,menu03_m,menu11_m,menu12_m,menu13_m,menu21_m,menu22_m,menu23_m,menu31,menu32,menu33,menu41,menu42,menu43,menu51,menu52,menu53,line_m = rec
                if vid_m == "select":
                    markup = menu_stat (menu01_m,menu02_m,menu03_m,menu11_m,menu12_m,menu13_m,menu21_m,menu22_m,menu23_m)
                if vid_m   == "command": 
                    markup = menu_command (suf,menu01_m,menu02_m,menu03_m,menu11_m,menu12_m,menu13_m,menu21_m,menu22_m,menu23_m,menu31,menu32,menu33,menu41,menu42,menu43,menu51,menu52,menu53)

            can_message = load_variable (user_id,message_in,namebot)
            if can_message != 'No':        
                if edit_out == 1:        
                    message_id = load_variable (user_id,"message_id",namebot)
                    bot_edit_send (user_id,message_id,message_out,markup,bot,namebot)
                else:    
                    bot_send (user_id,message_out,markup,bot,namebot)
                answer = 'отправлено'
            else:
                print ('[!!!] Отказано отправлять пользователю: {}: {}: {}'.format(message_in,user_id,can_message))
    

        can_message = load_variable (user_id,message_in,namebot)
        
        if picture_s != '' and can_message != 'No':
            sql = "select  id,name,bot_name,user_id,file,pyth from picture where name = '"+str(picture_s)+"' and bot_name = '"+namebot+"'"
            print ('[sql]',sql)
            cursor.execute(sql)
            data_p = cursor.fetchall()
            for rec_p in data_p: 
                id_p,name_p,bot_name,user_id_p,file_p,pyth_p = rec_p
                namefile = pyth_p + file_p
                print ('[+] namefile',namefile)
                try: 
                    photo = open(namefile, 'rb')
                    bot.send_photo(user_id, photo)  
                except: 
                    print ('[+] Нет такой картинки')

        if status_out != '':
            save_variable (user_id,"status",str(status_out),namebot)
        if status_out == '*':
            save_variable (user_id,"status",'',namebot)




    ### Создаем новое сообщение если стоит команда создать и аналога нет.
    answer = 'не отправлено'
    can_message = load_variable (user_id,message_in,namebot)
    if met_find == 0 and status == 'S' and message_out != '' and can_message != 'No':
        sql = "INSERT INTO message (`bot_name`,`text`,`input`,`menu`,`status`,`tekegram`,`status_out`,`run`,`field`,`picture`,`edit`) VALUES ('{}','{}','{}','{}','{}','','','','','',0)".format (namebot,message_in,message_in,'','')
        cursor.execute(sql)
        db.commit()
        bot_send (user_id,message_out,"",bot,namebot)
        answer = 'отправлено'
  
    if can_message == 'No':
        message_send = send_message (user_id,'В информации отказано','S',namebot,bot) 

    return answer

def bot_send (user_id,message_out,markup,bot,namebot):
    if markup != '':
        try: 
            bot.send_message(user_id,message_out,parse_mode='HTML',reply_markup=markup)
            send = 'send'
        except:    
            send = 'no send'
    else:
        #try:
        if 1==1:
            bot.send_message(user_id,message_out,parse_mode='HTML')
            send = 'send'
        #except:
        #    send = 'no send'   
    save_log (namebot,user_id,message_out,'out message','',send)
    return send

def bot_edit_send (user_id,message_id,message_out,markup,bot,namebot):
    if markup != '':
        try: 
            #bot.send_message(user_id,message_out,parse_mode='HTML',reply_markup=markup)
            bot.edit_message_text(chat_id=user_id, message_id=message_id, text=message_out,parse_mode='HTML',reply_markup=markup)
            send = 'send'
        except:    
            send = 'no send'
    else:
        try:
        #if 1==1:
            #bot.send_message(user_id,message_out,parse_mode='HTML')
            bot.edit_message_text(chat_id=user_id, message_id=message_id, text=message_out,parse_mode='HTML')
            send = 'send'
        except:
            send = 'no send'   
    save_log (namebot,user_id,message_out,'out message','',send)
    return send

def fill_message (user_id,message_out,namebot):
    message = message_out
    while message.find ('%%') != -1:
        nm = message.find ('%%')
        sl_begin = message [nm+2:]
        ng = sl_begin.find ('%%')
        sl_midel = sl_begin [0:ng]
        message =  sl_begin [ng:]
        answer  = load_variable (user_id,sl_midel,namebot) 
        zp = "%%"+str(sl_midel)+"%%"
        message_out = message_out.replace(zp,str(answer))
    return message_out    

def get_message (user_id,message_in,namebot):
    db,cursor   = connect (namebot)
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
    
def get_menu (user_id,menu,namebot):    
    db,cursor   = connect (namebot)
    sql = "select id,name,bot_name,vid,suf,menu01,menu02,menu03,menu11,menu12,menu13,menu21,menu22,menu23,menu31,menu32,menu33,menu41,menu42,menu43,menu51,menu52,menu53 from menu where name = '"+str(menu)+"' and bot = '"+namebot+"'"
    cursor.execute(sql)
    data   = cursor.fetchall()
    name   = ''
    markup = ''
    suf    = ''
    for rec in data: 
        id,name,bot_name,vid,suf,menu01,menu02,menu03,menu11,menu12,menu13,menu21,menu22,menu23,menu31,menu32,menu33,menu41,menu42,menu43,menu51,menu52,menu53 = rec
    if name != "":  
        if vid == "select":
            markup = menu_select (suf,menu01,menu02,menu03,menu11,menu12,menu13,menu21,menu22,menu23,menu31,menu32,menu33,menu41,menu42,menu43,menu51,menu52,menu53)
        if vid == "command": 
            markup = menu_command (suf,menu01,menu02,menu03,menu11,menu12,menu13,menu21,menu22,menu23,menu31,menu32,menu33,menu41,menu42,menu43,menu51,menu52,menu53)
    return markup            

def markup (sts):  
    from telebot import types
    markup = types.InlineKeyboardMarkup(row_width=4)
    for st in sts:
        tx,cl = st
        mn = types.InlineKeyboardButton(text=tx,callback_data = cl)        
        markup.add(mn) 
    return markup      

def get_name ():
    import random
    slovo01 = 'qwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM1234567890'
    sm = ''
    sl = int(random.randint(0, 60))
    sm1 = slovo01 [sl] ##slovo01[]
    sl = int(random.randint(0, 60))
    sm2 = slovo01 [sl] ##slovo01[]
    sl = int(random.randint(0, 60))
    sm3 = slovo01 [sl] ##slovo01[]
    sl = int(random.randint(0, 60))
    sm4 = slovo01 [sl] ##slovo01[]
    sl = int(random.randint(0, 60))
    sm5 = slovo01 [sl] ##slovo01[]
    sl = int(random.randint(0, 60))
    sm6 = slovo01 [sl] ##slovo01[]
    sl = int(random.randint(0, 60))
    sm7 = slovo01 [sl] ##slovo01[]
    sl = int(random.randint(0, 60))
    sm8 = slovo01 [sl] ##slovo01[]
    sl = int(random.randint(0, 60))
    sm9 = slovo01 [sl] ##slovo01[]
    sl = int(random.randint(0, 60))
    sm = sm1+sm2+sm3+sm4+sm5+sm6+sm7+sm8+sm9+'3dot14'
    return (sm)
  