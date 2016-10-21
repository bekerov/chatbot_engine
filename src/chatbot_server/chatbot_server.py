#!/usr/bin/env python
import os
import pickle
import argparse

from socket import *
from flask import Flask, render_template, session, request
from flask_restful import Resource, Api, reqparse
from datetime import datetime

from chatbot.chatbot import Chatbot
app = Flask(__name__)
api = Api(app)

resource_name_list_path = os.environ['CE_SRC'] + '/data/chatbot_info/resource_name_list.pickle'
chatbot_instance_dir_path = os.environ['CE_SRC'] + '/data/chatbot_instance'


def init_arg_parser():
    with open(resource_name_list_path, "rb") as f:
        resource_name_list = pickle.load(f)

    ps = reqparse.RequestParser()
    for resource_name in resource_name_list:
        ps.add_argument(resource_name)
    return ps


class Chatbot_rest(Resource):
    
    def __init__(self):
        self.chatbot_instance_path = ''
        pass
            

    def __del__(self):
        pass


    def get(self,user_id):
        user_id, query = user_id.split('_') 
        print(query)

        self.load_chatbot(user_id)

        chatbot =self.chatbot

        print("receive : " + str(query))
        result = chatbot.talk(query)
        print("response : " + str(result))

        self.save_chatbot()

        return result


    def post(self,user_id):
        self.load_chatbot(user_id)

        msg_from_user= dict(request.get_json(force=True))

        print("receive : " + str(msg_from_user))
        msg = msg_from_user['message']['text']
        msg_to_user = self.chatbot.talk(msg)
        msg_to_user['code'] = 200
        msg_to_user['parameter'] = {}
        print("response : " + str(msg_to_user))

        self.save_chatbot()

        return msg_to_user


    def load_chatbot(self,user_id):
        self.chatbot_instance_path = chatbot_instance_dir_path + '/'+str(user_id)
        self.chatbot_instance_path += '.cbinstance'

        self.chatbot = Chatbot()
        self.chatbot.load(self.chatbot_instance_path)       

    def save_chatbot(self):
        self.chatbot.save(self.chatbot_instance_path)       

parser = init_arg_parser()
api.add_resource(Chatbot_rest, '/chatbotinstance/<string:user_id>')


def main():
    app.run(host='0.0.0.0', port=6070, debug=True)
    #while True:
    #    print(chatbot.talk(input()))


if __name__ == '__main__':
    main()
