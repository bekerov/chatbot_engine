#!/usr/bin/env python
from flask import Flask, render_template, session, request
from flask_restful import Resource, Api,reqparse 
from datetime import datetime
app = Flask(__name__)
api = Api(app)


parser = reqparse.RequestParser()
parser.add_argument('date_time')
parser.add_argument('location')
class WeatherProvider(Resource):
    
    def get(self):
        args = parser.parse_args()
        print(args)
        location = args['location']
        date_time = args['date_time']
    
        date_time = datetime.strptime(date_time,"%Y%m%d_%H%M%S")
        result = ""
        result += location +"의 "
        result += date_time.strftime("%Y년%m월%d일")
        result += "의 날씨는 맑음 입니다."

        result_dict ={ "code":200, 
                        "response":result}

        return result_dict


def main():
    api.add_resource(WeatherProvider, '/get_weather')
    app.run(host='0.0.0.0',port=6000, debug=True)


if __name__ == '__main__':
    main()
