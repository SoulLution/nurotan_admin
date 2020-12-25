#!/usr/bin/python
# -*- coding: utf-8

k = '\033[37m\033[44m\033[1m'
s = "\033[0;37m"
e = "\033[1;33m" 
r = '\033[31m\033[44m\033[1m'
i = '\033[0;32m'
n = '\033[1;35m'

def main (message,namebot,bot):
    import iz_func
    username   = message.from_user.username
    first_name = message.from_user.first_name
    last_name  = message.from_user.last_name
    user_id    = message.from_user.id
    date       = message.date
    message_in = message.text
    print ('{}[+] Входящие сообщение:{} {}'.format(e,s,message_in))
    print ('{}[+] Обнуление параметров{}'.format(n,s))
    iz_func.save_variable (user_id,"status","",namebot)
    status = ''
    print ('{}[+] Запись пользователя в базу:{} {} {} {} {} {}{}'.format(n,s,i,user_id,username,first_name,last_name,s))
    iz_func.save_FIO (user_id,username,namebot,first_name,last_name)
    iz_func.referal  (user_id,namebot,message_in)
    iz_func.save_log (namebot,user_id,message_in,'in message','','text')
    return user_id,message_in,status

def next (message,namebot,bot):
    import iz_func
    user_id     = message.from_user.id
    message_in  = message.text
    username    = message.from_user.username
    first_name  = message.from_user.first_name
    last_name   = message.from_user.last_name
    date        = message.date
    status      = iz_func.load_variable (user_id,"status",namebot)
    print ('{}[+] Входящие сообшение:{} {}, Статус {}{}{}, {}{} {} {} {}{} '.format(e,s,message_in,e,status,s,i,user_id,username,first_name,last_name,s))
    iz_func.save_log (namebot,user_id,message_in,'in message',status,'text')       
    return user_id,message_in,status




