#!/usr/bin/python
# -*- coding: utf-8
# ОПИСАНИЕ БОТА: Информирование клиентов о новых поступлениях
# АВТОР БОТА   : Купинов Вадим
# ТЕЛЕГРАММ АВТОРА : @izofen

import time
import iz_func

namebot = "@BT_trader_bot"
if __name__ == "__main__":
    db,cursor = iz_func.connect (namebot)
    sql = "select id,ip,login,password,port,status,time_start,time_finish,time_long,bot_used from proxy where bot_used = '"+str(namebot)+"';"
    cursor.execute(sql)
    data = cursor.fetchall()
    for rec in data: 
        id,ip,login,password,port,status,time_start,time_finish,time_long,bot_used = rec    
        print ('[+]',ip,port)
        timestamp = int(time.time())
        sql = "UPDATE proxy SET bot_used = '' WHERE id = '"+str(id)+"'"
        cursor.execute(sql)
        db.commit()  
        sql = "UPDATE proxy SET time_finish = "+str(timestamp)+" WHERE id = '"+str(id)+"'"
        cursor.execute(sql)
        db.commit()  
        time_long = timestamp - time_start  

        if time_finish == 0:
            sql = "UPDATE proxy SET time_long = "+str(time_long)+" WHERE id = '"+str(id)+"'"
            cursor.execute(sql)
            db.commit()
            print ('[+]',time_long)
        else:
            sred = (time_long + time_long)/2
            sql = "UPDATE proxy SET time_long = "+str(sred)+" WHERE id = '"+str(id)+"'"
            cursor.execute(sql)
            db.commit()
            print ('[+]',time_long,sred)




            