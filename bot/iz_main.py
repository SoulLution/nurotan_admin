#!/usr/bin/python
# -*- coding: utf-8


def get_pass ():
    import random
    ps = ''
    strSM = "01234567890QWERTYUIOPASDFGHJKLZXCVBNMqwertyuiopasdfghjklzxcvnm"
    for number1 in range(5):
        for number2 in range(4):
            rn = random.randint(0,len(strSM))
            ps = ps + strSM[rn:rn+1]
        ps = ps + '-' 
        for number2 in range(4):
            rn = random.randint(0,len(strSM))
            ps = ps + strSM[rn:rn+1]   
    return ps
        
    