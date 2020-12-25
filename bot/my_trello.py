#!/usr/bin/python

from datetime import datetime
from trello import TrelloClient, Board

import iz_func

import pymysql
db = pymysql.connect("127.0.0.1","izofen","podkjf4","main" ,use_unicode=True, charset="utf8mb4" )       

client = TrelloClient(
    api_key='6cf0afa3dc5bb11830154d2fa55e2928',   ## your-key
    api_secret='8b46323d797ff507d88a5d028744ae1e5c7669d388ce888ce94f5da9c4746b1e',  ## your-secret
    token='',  ## your-oauth-token-key
    token_secret=''  ## your-oauth-token-secret
)


def new_message_trello (name_board,name_message,test_message):
    all_boards = client.list_boards()
    for board in all_boards:
        if board.name.find (name_board) != -1: ## @bb_c_bot   
            for list in board.list_lists():
                if list.name == 'Список сообщений':        
                    newCard = list.add_card(name_message)
                    newCard.set_description (test_message)

def get_message_trello (name_board):
    messages = []
    all_boards = client.list_boards()
    #print ('[+]',board.name)
    for board in all_boards:
        if board.name.find (name_board) != -1: ## @bb_c_bot
            for list in board.list_lists():
                if list.name == 'Список сообщений':
                    for card in list.list_cards():
                        message = []
                        message.append(card.name)
                        message.append(card.desc)
                        messages.append(message)
                        print ('        [cn]',card.name)
                        print ('        [cd]',card.desc)
                        #checklists = card.get_checklists()
    return messages
    
def get_message_base (name_board):
    cursor = db.cursor()  
    sql = "select input,text from message where tekegram = '"+name_board+"'"
    cursor.execute(sql)
    data = cursor.fetchall()
    #for rec in data:
    #    print ('[+]',rec)
    return data


def check_in_trello (message_trello,message_base):
    answer = False
    name_base,desc_base =  message_base
    for message_trello in messages_trello:
        name_trello,desc_trello =  message_trello
        if name_trello == name_base:
            answer = True
    return answer        

print ('[!] Проверка изменений в трелло')
messages_trello = get_message_trello ('@bb_c_bot')
for message_trello in messages_trello:
    name_trello,desc_trello =  message_trello
    print (    '[+]',name_trello)
    print (    '[+]',desc_trello)
    iz_func.update_message (db,'@bb_c_bot',name_trello,desc_trello);

messages_base = get_message_base ('@bb_c_bot')
for message_base in messages_base:
    name_base,desc_base =  message_base
    print ('[+]',name_base)
    print ('[+]',desc_base)
    result = check_in_trello (message_trello,message_base)
    if result == False:
        new_message_trello ('@bb_c_bot',name_base,desc_base)
## @AMLSbot
