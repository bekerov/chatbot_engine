#!/usr/bin/env python
import os
import pickle
import argparse
from flask import Flask, render_template, session, request
from flask_restful import Resource, Api, reqparse
from datetime import datetime


app = Flask(__name__)
api = Api(app)

resource_name_list_path = os.environ['CE_SRC'] + '/data/chatbot_info/resource_name_list.pickle'


def init_arg_parser():
    with open(resource_name_list_path, "rb") as f:
        resource_name_list = pickle.load(f)

    ps = reqparse.RequestParser()
    for resource_name in resource_name_list:
        print(resource_name)
        ps.add_argument(resource_name)
    return ps


class WeatherProvider(Resource):
    @staticmethod
    def get():
        args = parser.parse_args()
        print(args)
        location = args['location']
        date_time = args['date_time']

        date_time = datetime.strptime(date_time, "%Y%m%d_%H%M%S")
        result = ""
        result += date_time.strftime("%Y년%m월%d일 ")
        result += location
        result += "의 날씨는 맑음 입니다."

        result_dict = {"code": 200, "response": result}

        return result_dict


class NaverShoppingProvider(Resource):
    @staticmethod
    def get():
        args = parser.parse_args()
        print(args)
        query = args['query']
        from chatbot_server.lib.NaverShoppingParser import NaverShoppingParser
        nsp = NaverShoppingParser(query)
        result = nsp.get()
        return result


parser = init_arg_parser()
api.add_resource(WeatherProvider, '/get_weather')
api.add_resource(NaverShoppingProvider, '/get_nshopping')


def main():
    app.run(host='0.0.0.0', port=6000, debug=True)


if __name__ == '__main__':
    main()
