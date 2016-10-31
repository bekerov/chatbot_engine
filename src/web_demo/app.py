#!/usr/bin/env python
import os
import sys
from datetime import datetime
import pickle
import json
from pprint import pprint
from socket import *

import requests

from modules.named_entity_recognizer.named_entity_recognizer import NamedEntityRecognizer
from modules.query_classifier import QueryClassifier
from modules.various_utils import generateLogger, get_time_prefix

from flask import Flask, render_template, session, request
from flask_socketio import SocketIO, emit, join_room, leave_room, \
    close_room, rooms, disconnect


from chatbot.chatbot import Chatbot

story_dir_path = os.environ['CE_SRC']+'/data/story'
query_classifier_path = os.environ['CE_SRC']+'/data/query_classifier/query_classifier.pickle'
story_type_dict_dict_path =os.environ['CE_SRC']+'/data/chatbot_info/story_type_dict_dict.pickle'

async_mode = None

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app, async_mode=async_mode)

chatbot_server_protocol = 'http://'
chatbot_server_host = 'localhost'
chatbot_server_port = 6070

chatbot_server_url = chatbot_server_protocol + chatbot_server_host + ':' + str(chatbot_server_port) + '/chatbotinstance'
                        


def msg_to_generic_template(msg):
    result = ''

    element_list = msg['elements']

    result += '<div>'

    for elem in element_list:
        result += '<a href="'+elem['item_url']+'" >'
        result += '<div class="">'
        result += '<h4>'+elem['title']+'</h4>'
        result += '<p>'+elem['subtitle']+'</p>'
        result += '<img width="200" height="200" class="img-responsive" src="'+elem['image_url']+'"/>' 

        result += '</div>'
        result += '</a>'

    result += '</div>'

    return result

def msg_to_text_template(msg):

    return msg['text']


def msg_to_button_template(msg):
    return msg['text']


def make_proper_response(msg):
    msg_type_function_dict = {
                        'generic':msg_to_generic_template,
                        'text':msg_to_text_template,
                        'button':msg_to_button_template,
                    }

    template_maker = msg_type_function_dict[msg['template_type']]

    result = template_maker(msg)

    return result




@app.route('/')
def index():
    return render_template('index.html', async_mode=socketio.async_mode)

@socketio.on('request', namespace='/test')
def talk(message):

    print("from web :" + message['data'])

    msg_from_user = {
            'code' : 200,
            'message':{
                        'text':''
                        }
            }

    
    url = chatbot_server_url + '/' + '1234'

    msg_from_user['message']['text'] = message['data']

    msg_to_user= requests.post(url,json=msg_from_user).json()
    msg_to_user = dict(msg_to_user)
    print(msg_to_user)


    result = ''

    for msg in msg_to_user['message']:
        result += make_proper_response(msg)
        result += '<br/>'


    #refined_msg_to_user = make_proper_response(msg_to_user['message'][0])


    msg_to_user['data'] = result
    #msg_to_user['data'] = refined_msg_to_user
    #msg_to_user['data'] = msg_to_user['message'][0]['text']

    print("from chatbot server : "+  str(msg_to_user))

    emit('response',    msg_to_user)


@socketio.on('connect', namespace='/test')
def test_connect():
    #emit('response', {'data': 'Connected'})
    print("connected!!!")


@socketio.on('disconnect', namespace='/test')
def test_disconnect():
    print('Client disconnected', request.sid)



if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=6050,  debug=True)
