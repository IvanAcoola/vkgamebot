from random import randint, choice
from config import *
import requests
from os import listdir
import json
from pictures import picsinfo

#msg from group
def sendMsgGroup(id, text):
    randomid = randint(0, 1000000000)
    session.method("messages.send", {"user_id": id, "message": text, "random_id": randomid})

#msg from group with keyboard
def sendMsgGroupKeyb(id, text, keyb):
    randomid = randint(0, 10000000)
    session.method("messages.send", {"user_id": id, "message": text, "random_id": randomid, 'keyboard': keyb})

#create button
def get_but(text, color):
    return {
                "action": {
                    "type": "text",
                    "payload": "{\"button\": \"" + "1" + "\"}",
                    "label": f"{text}"
                },
                "color": f"{color}"
            }

#send file (document)
def sendFile(id, file_path, upload_name):
    a = session.method("docs.getMessagesUploadServer", {"type": "doc", "peer_id": id})['upload_url']
    files = {'file': open(file_path, 'rb')}
    r = requests.post(a, files=files).json()
    c = session.method('docs.save', {"file": r["file"], "title": upload_name})
    d = 'doc{}_{}'.format(c['doc']['owner_id'], c['doc']['id'])
    randomid = randint(1, 10000000)
    session.method("messages.send", {"user_id": id, "attachment": d,  "random_id": randomid})

def sendFileK(id, file_path, upload_name, keyb):
    a = session.method("docs.getMessagesUploadServer", {"type": "doc", "peer_id": id})['upload_url']
    files = {'file': open(file_path, 'rb')}
    r = requests.post(a, files=files).json()
    c = session.method('docs.save', {"file": r["file"], "title": upload_name})
    d = 'doc{}_{}'.format(c['doc']['owner_id'], c['doc']['id'])
    randomid = randint(1, 10000000)
    session.method("messages.send", {"user_id": id, "attachment": d,  "random_id": randomid, "keyboard": keyb})

def give_pict_test(id, denied=''):
    choised_pict = choice(listdir('pict/'))
    pict_name = choised_pict.replace('.jpg', '')

    while pict_name == denied:
        choised_pict = choice(listdir('pict/'))
        pict_name = choised_pict.replace('.jpg', '')

    ans_var = list(picsinfo[pict_name].keys())
    keyboard = {
        "one_time": False,
        "inline": True,
        "buttons": [
            [get_but(ans_var[0], 'positive')],
            [get_but(ans_var[1], 'positive')],
            [get_but(ans_var[2], 'positive')],
            [get_but(ans_var[3], 'positive')]
        ]
    }
    keyboard = json.dumps(keyboard, ensure_ascii=False).encode('utf-8')
    keyboard = str(keyboard.decode('utf-8'))
    sendFileK(id, 'pict/' + choised_pict, 'test.jpg', keyboard)
    return pict_name