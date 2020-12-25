#!/usr/bin/python
# -*- coding: utf-8

def get_proxy (namebot,proxy_t):
    print ('[+] namebot:',namebot)
    print ('[+] proxy_t:',proxy_t)
    import random
    import time
    import iz_func
 
    db,cursor = iz_func.connect (namebot)

    ### Очищаем от предедущей информации
    sql = "UPDATE proxy SET bot_used = '' WHERE bot_used = '"+str(namebot)+"'"
    cursor.execute(sql)
    db.commit()


    ### mem - выставляем что запомнили, если нет выбираем любую    
    ip    = ''
    port  = 0
    proxy_tip = ''
    start_n = 0
    get_proxy = ''

    sql = "select id,name,ip,port,proxy_tip,get_proxy from bots where name = '"+str(namebot)+"';"
    print ('[sql]',sql)
    cursor.execute(sql)
    data = cursor.fetchall()
    for rec in data: 
        id,name,ip,port,proxy_tip,get_proxy = rec 

    print ('[+],get_proxy:',get_proxy)    
        

    if ip != '' and port != 0 and proxy_tip != '' and proxy_t == 'mem' and proxy_t != 'best':        
        if proxy_tip == 'http':
            proxy = {'https':'http://{}:{}'.format(ip,port)}
        if proxy_tip == 'socks5':
            proxy = {'https':'socks5://{}:{}'.format(ip,port)} 
        
    if proxy_t == 'db' and get_proxy != '':
        db,cursor = iz_func.connect (namebot)
        sql = "select id,ip,login,password,port,status,time_start,time_finish,time_long,bot_used,proxy from proxy where status = '"+get_proxy+"' limit 1"
        proxy_tip = ''
        ip        = ''
        port      = 0
        cursor.execute(sql)
        data = cursor.fetchall()
        for rec in data: 
            id,ip,login,password,port,status,time_start,time_finish,time_long,bot_used,proxy_tip = rec  
        if ip != '' and  port != 0:
            if proxy_tip == 'http':
                proxy = {'https':'http://{}:{}'.format(ip,port)}        
            if proxy_tip == 'socks5':
                proxy = {'https':'socks5://{}:{}'.format(ip,port)}                 




    ### mem - выставляем лутшею, если нет выбираем любую
    if proxy_t == 'best':
        db,cursor = iz_func.connect (namebot)
        sql = "select id,ip,login,password,port,status,time_start,time_finish,time_long,bot_used,proxy from proxy where status = 'test' and bot_used = '' ORDER BY time_long DESC  limit 1"
        proxy_tip = ''
        ip        = ''
        port      = 0
        cursor.execute(sql)
        data = cursor.fetchall()
        for rec in data: 
            id,ip,login,password,port,status,time_start,time_finish,time_long,bot_used,proxy_tip = rec  
        if ip != '' and  port != 0:
            if proxy_tip == 'http':
                proxy = {'https':'http://{}:{}'.format(ip,port)}        
            if proxy_tip == 'socks5':
                proxy = {'https':'socks5://{}:{}'.format(ip,port)}         
        
    ### Выставлем строго указанную прокси
    if proxy_t != 'new' or proxy_t != 'mem' or proxy_t != 'best'  or proxy_t != 'db': 
        sql = "select id,ip,login,password,port,status,time_start,time_finish,time_long,bot_used,proxy from proxy where status = '"+str(proxy_t)+"';"
        cursor.execute(sql)
        data = cursor.fetchall()
        for rec in data: 
            id,ip,login,password,port,status,time_start,time_finish,time_long,bot_used,proxy_tip = rec    

        if proxy_tip == 'http':
            proxy = {'https':'http://{}:{}'.format(ip,port)}        
        if proxy_tip == 'socks5':
            proxy = {'https':'socks5://{}:{}'.format(ip,port)}         
        
    ### new - выставляем любую, Если не прошло предедушая
    if proxy_t == 'new' or (ip == '' and port == 0):
        db,cursor = iz_func.connect (namebot)
        sql = "select id,ip,login,password,port,status,time_start,time_finish,time_long,bot_used,proxy,start_n from proxy where status = 'test' and bot_used = '';"
        cursor.execute(sql)
        data = cursor.fetchall()
        list = []
        for rec in data: 
            id,ip,login,password,port,status,time_start,time_finish,time_long,bot_used,proxy_tip,start_n = rec    
            list.append([id,ip,port,proxy_tip])

        id,ip,port,proxy_tip = random.choice(list)

        proxy = ''
        if proxy_tip == 'http':
            proxy = {'https':'http://{}:{}'.format(ip,port)}
        if proxy_tip == 'socks5':
            proxy = {'https':'socks5://{}:{}'.format(ip,port)} 

    ### Указываем что прокси тестируется 
    timestamp = int(time.time())
    sql = "UPDATE proxy SET bot_used = '"+namebot+"' WHERE id = '"+str(id)+"'"
    cursor.execute(sql)
    db.commit()        
    sql = "UPDATE proxy SET time_start = '"+str(timestamp)+"' WHERE id = '"+str(id)+"'"
    cursor.execute(sql)
    db.commit()     
    sql = "UPDATE proxy SET start_n = "+str(start_n+1)+" WHERE id = '"+str(id)+"'"        
    cursor.execute(sql)
    db.commit()  

    ### Записываем в бота для отображения в админке
    sql = "UPDATE bots SET set_tip_proxy  = '"+str(proxy_t)+" : "+str(get_proxy)+"' WHERE name = '"+str(namebot)+"'"
    cursor.execute(sql)
    db.commit()
    sql = "UPDATE bots SET set_ip_proxy   = '"+str(ip)+"'      WHERE name = '"+str(namebot)+"'"
    cursor.execute(sql)
    db.commit()
    sql = "UPDATE bots SET set_port_proxy = '"+str(port)+"'    WHERE name = '"+str(namebot)+"'"
    cursor.execute(sql)
    db.commit()


    return proxy

def main (namebot,proxy_t):
    import iz_func
    import telebot
    from telebot import apihelper
    #ip   = '196.19.9.179'
    #port = '8000'
    #proxy = {'https':'http://{}:{}'.format(ip,port)}   
    #proxy = get_proxy (namebot,proxy_t)    
    #apihelper.proxy = proxy
    proxy = ''
    token,about = iz_func.get_token (namebot)
    print ('[+] token',token)
    print ('[+] about',about)
    bot   = telebot.TeleBot(token)
    return bot,proxy

def begin (namebot,proxy):  
    import iz_func
    k = '\033[37m\033[44m\033[1m'
    s = '\033[0;37m'
    e = '\033[1;33m' 
    r = '\033[31m\033[44m\033[1m'
    i = '\033[0;32m'
    n = '\033[1;35m'

    db,cursor = iz_func.connect (namebot)
    sql = "select id,set_ip_proxy,set_port_proxy,set_tip_proxy from bots where name = '"+str(namebot)+"';"
    cursor.execute(sql)
    data = cursor.fetchall()
    prt = ''

    set_ip_proxy = ''
    for rec in data: 
        id,set_ip_proxy,set_port_proxy,set_tip_proxy = rec

    if set_ip_proxy != '':    
        prt = set_ip_proxy+':'+set_port_proxy+'-'+set_tip_proxy
    else:
        print ('[+] Прокси не указано')    
        exit (0)



    print ('{}╔══════════════════════════════════════════════════════════════════════════════════════════════════════════════════╗{}'.format(k,s))
    print ('{}║                                      {}Всем привет!👋👋!    {}                                           {}   ║{}'.format(k,r,k,iz_func.RealData,s))
    print ('{}║                                                                                                               ║{}'.format(k,s))  
    print ('{}║  Название программы:            {}{}{}                                                                 ║{}'.format(k,e,namebot,k,s))
    print ('{}║  Описание:                      {}Бот для работы с клиентами{}                                                       ║{}'.format(k,e,k,s))
    print ('{}║  Версия                         {}23.2.0{}                                                                           ║{}'.format(k,e,k,s))
    print ('{}║                                                                                   ║{}'.format(k,s))
    print ('{}║  Proxy:                         {}{}{}                                             ║{}'.format(k,e,prt,k,s))     
    print ('{}║  Автор:                         {}@izofen (https://t.me/izofen){}                                                    ║{}'.format(k,e,k,s))    
    print ('{}║  Админка:                       {}http://3dot14.ru/admin/pages/tables/profile.php{}                                  ║{}'.format(k,e,k,s))
    print ('{}║  Резервная копия дата:          {}20 января 2020{}                                                                   ║{}'.format(k,e,k,s))
    print ('{}║  Текущих пользователей:         {}10{}                                                                               ║{}'.format(k,e,k,s))
    print ('{}║  Статистика использования:      {}10{}                                                                               ║{}'.format(k,e,k,s))
    print ('{}║                                                                                                                  ║{}'.format(k,s))  
    print ('{}║  Оповещенние при новых пользователях          {}Включено{}                                                           ║{}'.format(k,e,k,s))
    print ('{}║  Оповещенние при перезапуске                  {}Включено{}                                                           ║{}'.format(k,e,k,s))
    print ('{}║  Оповещенние при активности                   {}Включено{}                                                           ║{}'.format(k,e,k,s))
    print ('{}║                                                                                                                  ║{}'.format(k,s))  
    print ('{}║  Тестирование прокси:                         {}Включено{}                                                           ║{}'.format(k,e,k,s))
    print ('{}║  Тестирование работы программы                {}Включено{}                                                           ║{}'.format(k,e,k,s)) 
    print ('{}║  Протоколирование работы                      {}Включено{}                                                           ║{}'.format(k,e,k,s)) 
    print ('{}║  Реферальная программа                        {}Включено{}                                                           ║{}'.format(k,e,k,s))
    print ('{}║  Прием оплаты                                 {}Включено{}                                                           ║{}'.format(k,e,k,s))
    print ('{}║  Интеграция AMO CRM                           {}Включено{}                                                           ║{}'.format(k,e,k,s))
    print ('{}║  Интеграция Trello                            {}Включено{}                                                           ║{}'.format(k,e,k,s))
    print ('{}║  Интеграция 1С Предприятие                    {}Включено{}                                                           ║{}'.format(k,e,k,s))
    print ('{}║  Рассылка сообщения клиентам                  {}Включено{}                                                           ║{}'.format(k,e,k,s))
    print ('{}║                                                                                                                  ║{}'.format(k,s)) 
    print ('{}║  Группа фанатов разработки:     {}https://t.me/izofen{}                                                              ║{}'.format(k,e,k,s))
    print ('{}║  Для остановки нажмите {}CTRL+C{}                                                                                    ║{}'.format(k,e,k,s)) 
    print ('{}╚══════════════════════════════════════════════════════════════════════════════════════════════════════════════════╝{}'.format(k,s))



