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

story_dir_path = os.environ['CE_SRC']+'/data/story'
query_classifier_path = os.environ['CE_SRC']+'/data/query_classifier/query_classifier.pickle'
story_type_dict_dict_path =os.environ['CE_SRC']+'/data/chatbot_info/story_type_dict_dict.pickle'


async_mode = None

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app, async_mode=async_mode)

host_serv = 'localhost' 
port_serv = 21571
buff_size = 2048
addr_serv = (host_serv, port_serv)

tcpCliSock = socket(AF_INET, SOCK_STREAM)
tcpCliSock.connect(addr_serv) 

@app.route('/')
def index():
    return render_template('index.html', async_mode=socketio.async_mode)

@socketio.on('request', namespace='/test')
def talk(message):
    ret = tcpCliSock.send(message['data'].encode())
    print("ret : " + str(ret))
    print("from web :" + message['data'])
    data = tcpCliSock.recv(buff_size).decode()
    print("from cli server : "+  data)
    emit('response',    {'data': data})


@socketio.on('connect', namespace='/test')
def test_connect():
    emit('response', {'data': 'Connected'})
    print("connected!!!")


@socketio.on('disconnect', namespace='/test')
def test_disconnect():
    print('Client disconnected', request.sid)



if __name__ == '__main__':
    socketio.run(app, port=7000,  debug=True)
