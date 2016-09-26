#!/usr/bin/env python
from flask import Flask, render_template, session, request
from flask_wtf import Form
from flask_restful import Resource, Api
from pymongo import MongoClient
app = Flask(__name__)
api = Api(app)

db_address = "ec2-52-78-112-141.ap-northeast-2.compute.amazonaws.com" 
db_port = 27017

@app.route('/')
def index():
    return render_template('index.html',)


@app.route('/select_location')
def select_location():
    return render_template('select_location.html',)


@app.route('/detail', methods=['POST'])
def detail():
    carryspot = request.form['carryspot'] 
    return render_template('detail.html', carryspot=carryspot)


@app.route('/find_jim_put_name')
def find_jim_put_name():
    return render_template("find_jim_put_name.html")


@app.route('/find_jim', methods=['POST'])
def find_jim():
    user_name = request.form['user_name']

    client = MongoClient(db_address,db_port)
    coll = client['jc']['jim']
    
    jim_data_list = []
    for jim_data in coll.find({'user_name': user_name}):
        jim_data_list.append(jim_data)

    return render_template("find_jim.html", jim_data_list=jim_data_list)


@app.route('/summary', methods=['POST'])
def summary():

    user_name = request.form['user_name']
    identifier = request.form['identifier']

    carryspot = request.form['carryspot']
    take_time_start = request.form['take_time_start']
    take_time_end = request.form['take_time_end']
    airport = request.form['airport']

    jim_data = { 'user_name': user_name,
                    'identifier' : identifier,
                    'carryspot' : carryspot,
                    'take_time_start' : take_time_start,
                    'take_time_end' : take_time_end,
                    'airport' : airport,
                }

    client = MongoClient(db_address,db_port)
    coll = client['jc']['jim']

    coll.insert_one(jim_data)
    return render_template('summary.html', user_name=user_name, identifier=identifier, carryspot=carryspot,take_time_start=take_time_start,take_time_end=take_time_end, airport=airport)


@app.route('/done')
def done():
    return render_template('done.html')

class SpotManager(Resource):

    def get(self):
        client = MongoClient(db_address,db_port)
        db = client['jc']        
        coll = db['carry_spot']
        spot_info = {"code":200, "spot_list":[]}

        for spot in coll.find():
            spot_info['spot_list'].append(spot)

        return spot_info


def main():
    api.add_resource(SpotManager, '/get_spot')
    app.run(host='0.0.0.0',port=8000,debug=True)


if __name__ == '__main__':
    main()
