#!/usr/bin/env python
import os
import pickle
import argparse

from socket import *
from flask import Flask, render_template, session, request
from flask_restful import Resource, Api, reqparse
from datetime import datetime

from cli_demo import Chatbot


app = Flask(__name__)
api = Api(app)

resource_name_list_path = os.environ['CE_SRC'] + '/data/chatbot_info/resource_name_list.pickle'

chatbot = Chatbot()
chatbot.save("./cb_instance.dict")

#@app.route('/chatbotinstance/<string:query>', methods =['GET'])
#def chatbotinstance(query):
#    print("receive : " + str(query))
#    chatbot = Chatbot() 
#    result = chatbot.talk(query)
#    print("response : " + str(result))
#
#    return result['text']
#    #return "test"


def init_arg_parser():
    with open(resource_name_list_path, "rb") as f:
        resource_name_list = pickle.load(f)

    ps = reqparse.RequestParser()
    for resource_name in resource_name_list:
        print(resource_name)
        ps.add_argument(resource_name)
    return ps


class Chatbot_rest(Resource):
    
    def __init__(self):
        pass
       
            
    def __del__(self):
        #print("chat bot dead!!")
        pass

    def get(self,query):
        chatbot = Chatbot()
        chatbot.load("./cb_instance.dict")

        print("receive : " + str(query))
        result = chatbot.talk(query)
        print("response : " + str(result))


        return result

    def post(self,query):
        args = parser.parse_args()
        #print(args)
        #query = args['query']
        #date_time = args['date_time']
        query = args['message']['text']
        ret = self.tcpCliSock.send(query.encode())
        data = self.tcpCliSock.recv(self.buff_size).decode()
        print(data)


        return data

parser = init_arg_parser()
api.add_resource(Chatbot_rest, '/chatbotinstance/<string:query>')



def main():
    app.run(host='0.0.0.0', port=6070, debug=True)
    #while True:
    #    print(chatbot.talk(input()))



if __name__ == '__main__':
    main()
