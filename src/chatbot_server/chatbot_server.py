#!/usr/bin/env python3

from flask import Flask, make_response
from flask_restful import Resource, Api
from flast_socketio import SocketIO, emit, join_room, leave_room, close_room, rooms, disconnect

from datetime import datetime
from chatbot import Chatbot
from various_util.various_util import generateLogger
import argparse
from urllib.parse import unquote

logger = generateLogger("./log_chatbot.log", "serverLog")

parser = argparse.ArgumentParser()
parser.add_argument("--mode", help="mode [production|development] Default: development")
args = parser.parse_args()

class ChatbotServer(Resource):
    
    def __init__(self):

        mode='development'
        if args.mode == "development":
            mode = 'development'
        elif args.mode ==  'production':
            mode = 'production'

        logger.debug("mode : " + mode)
        self.chatbot = Chatbot(config_path="./config.ini", mode=mode)
        

    def get(self,query):
        logger.debug("query : "+unquote(query))
        result = self.chatbot.ask(unquote(query))
    
        return result

def main():

    logger.debug("server start!")
    app = Flask(__name__)
    api = Api(app)
    api.add_resource(ChatbotServer, '/<string:query>')
    app.run(host='0.0.0.0', port=8000, debug=True) 

if __name__ == '__main__':
    main()
