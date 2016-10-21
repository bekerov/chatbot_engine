#!/usr/bin/env python
import os
import pickle
import argparse

from socket import *
from flask import Flask, render_template, session, request
from flask_restful import Resource, Api, reqparse
from datetime import datetime

from chatbot import Chatbot
app = Flask(__name__)
api = Api(app)

resource_name_list_path = os.environ['CE_SRC'] + '/data/chatbot_info/resource_name_list.pickle'



def init_arg_parser():
    with open(resource_name_list_path, "rb") as f:
        resource_name_list = pickle.load(f)

    ps = reqparse.RequestParser()
    for resource_name in resource_name_list:
        ps.add_argument(resource_name)
    return ps


class Chatbot_rest(Resource):
    
    def __init__(self):
        self.chatbot = Chatbot()
        self.chatbot_instance_path= "./chatbot_instance.dat"
        self.chatbot.load(self.chatbot_instance_path)       
            
    def __del__(self):
        self.chatbot.save(self.chatbot_instance_path)       
        print("dead")

    def get(self,query):

        chatbot =self.chatbot

        print("receive : " + str(query))
        result = chatbot.talk(query)
        print("response : " + str(result))

        return result

    def post(self,user_id):
        #args = parser.parse_args()
        #print(args)
        #query = args['query']
        #date_time = args['date_time']
        #query = args['message']['text']

        msg_from_user= dict(request.get_json(force=True))

        print("receive : " + str(msg_from_user))
        msg = msg_from_user['message']['text']
        msg_to_user = self.chatbot.talk(msg)
        print("response : " + str(msg_to_user))
        return msg_to_user


parser = init_arg_parser()
api.add_resource(Chatbot_rest, '/chatbotinstance/<string:query>')


def main():
    app.run(host='0.0.0.0', port=6070, debug=True)
    #while True:
    #    print(chatbot.talk(input()))


if __name__ == '__main__':
    main()
