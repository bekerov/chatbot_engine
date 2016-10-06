# Chatbot Engine

## 데모 동영상
[![Alt text for your video](http://img.youtube.com/vi/mCoI7CpSBR0/0.jpg)](https://youtu.be/mCoI7CpSBR0)

+ 클릭하시면 Youtube로 이동합니다.



## 환경 설정
```bash
cd path/to/chatbot_engine
source ./source_it_to_set_envs.sh
```

``` bash
# source_it_to_set_envs.sh
export PYTHONPATH=$PWD/src:$PYTHONPATH
export CE_HOME=$PWD
export CE_SRC=$PWD/src

```

## 디렉토리 구조
```
chatbot_engine
├── readme.md
├── requirements.txt
├── source_it_to_set_envs.sh
└── src
    ├── chatbot_builder
    │   └── chatbot_builder.py
    ├── chatbot_server
    │   ├── chatbot_rest_api_server.py
    │   ├── run_server.sh
    │   ├── static
    │   └── templates
    ├── cli_demo
    │   └── cli_demo.py
    ├── data
    │   ├── chatbot_info
    │   │   ├── resource_name_list.pickle
    │   │   └── story_type_dict_dict.pickle
    │   ├── query_classifier
    │   │   ├── query_classifier.pickle
    │   ├── readme.md
    │   └── story
    │       ├── get_stock.json
    │       ├── get_weather.json
    ├── functions
    │   └── function_a.py
    └── modules
        ├── named_entity_recognizer
        │   ├── modules
        │   │   ├── city_recognizer.py
        │   │   ├── date_time_recognizer.py
        │   ├── named_entity_recognizer.py
        ├── query_classifier.py
        └── various_utils.py
```



# Chatbot Engine

## Chatbot Engine Flow

#### 1. chatbot_builder를 이용하여 story 생성

+ story 생성 예제

```
==================================================
make story start!
target_function (function name) : get_weather
number of parameters to call target_function : 2
parameter name 0 : location:location
parameter name 1 : date_time:date_time
user say like : 오늘 날씨 어때?
--------------------------------------------------
make bot questions

question for [location] : 어디야?
number of choices : 3
choice : 서울
choice : 대구
choice : @text
-------------------------
question for [date_time] : 언제?
number of choices : 3
choice : 오늘
choice : 내일
choice : @date_picker
-------------------------
{'parameter_list': [{'parameter_name': 'location',
                     'parameter_type': 'location'},
                    {'parameter_name': 'date_time',
                     'parameter_type': 'date_time'}],
 'query_list': [{'query': '오늘 날씨 어때?'}],
 'question_list': [{'choice_list': ['서울', '대구', '@text'],
                    'parameter': {'parameter_name': 'location',
                                  'parameter_type': 'location'},
                    'question': '어디야?'},
                   {'choice_list': ['오늘', '내일', '@date_picker'],
                    'parameter': {'parameter_name': 'date_time',
                                  'parameter_type': 'date_time'},
                    'question': '언제?'}],
 'target_function': 'get_weather'}
==================================================

```

ps. @text 또는 @date_picker는 프론트엔드에서 텍스트 필드 혹은 데이트 픽커를 사용자에게 제공할 수 있도록 한다.

#### 2. 생성된 story는 $CE_HOME/src/data/story/ 디렉토리에 json 형태로 저장

+ story 디렉토리에 저장된 story의 예 

```
story
├── get_stock.json
├── get_weather.json
```

+ 저장된 story의 형식

```
# get_weather.json

{ 
    'target_function': 'get_weather'

    'parameter_list': [{'parameter_name': 'location',
                         'parameter_type': 'location'},
                        {'parameter_name': 'date_time',
                         'parameter_type': 'date_time'}],

    'query_list': [{'query': '오늘 날씨 어때?'}],

    

    'question_list': [{'choice_list': ['서울', '대구', '@text'],
                    'parameter': {'parameter_name': 'location',
                                  'parameter_type': 'location'},
                    'question': '어디야?'},
                   {'choice_list': ['오늘', '내일', '@date_picker'],
                    'parameter': {'parameter_name': 'date_time',
                                  'parameter_type': 'date_time'},
                    'question': '언제?'}],
}
```

+ target_function : story가 궁극적으로 제공할 기능, 함수 이름
+ parameter_list : target_function을 실행하기 위한 파라미터 이름과 형식
+ query_list : 해당 story를 실행하기 위한 query 리스트, 질의 분류기 학습에 사용
+ question_list : target_function이 필요한 parameter_list에 대한 정답을 구하기 위한 질문 리스트


#### 3. 챗봇이 제공할 기능을 RESTful API 서버를 제작

+ 날씨 서비스에 대한 RESTful API 서버의 예

```python
#!/usr/bin/env python
import os
import pickle
import argparse
from flask import Flask, render_template, session, request
from flask_restful import Resource, Api,reqparse 
from datetime import datetime
app = Flask(__name__)
api = Api(app)

resource_name_list_path =os.environ['CE_SRC']+'/data/chatbot_info/resource_name_list.pickle'


def init_arg_parser():
    with open(resource_name_list_path, "rb") as f:
        resource_name_list = pickle.load(f)

    parser = reqparse.RequestParser()
    for resource_name in resource_name_list:
        print(resource_name)
        parser.add_argument(resource_name)
    return parser


class WeatherProvider(Resource):
    
    def get(self):
        args = parser.parse_args()
        print(args)
        location = args['location']
        date_time = args['date_time']
    
        date_time = datetime.strptime(date_time,"%Y%m%d_%H%M%S")
        result = ""
        result += date_time.strftime("%Y년%m월%d일 ")
        result += location
        result += "의 날씨는 맑음 입니다."

        result_dict ={ "code":200, 
                        "response":result}

        return result_dict


parser = init_arg_parser()
api.add_resource(WeatherProvider, '/get_weather')

def main():
    app.run(host='0.0.0.0',port=6000, debug=True)


if __name__ == '__main__':
    main()
```   

+ 요청의 예

```
curl -v http://xxx.xxx.xxx.xxx:yyyy/get_weather -d "location=대구" -d "date_time=20160901_235959" -X GET
```

+ 응답의 예

```json
{'response': '2016년10월06일 서울의 날씨는 맑음 입니다.', 'code': 200}
``` 

+ http://xxx.xxx.xxx.xxx:yyyy/get_weather 에 GET 요청으로 location, date_time에 대한 값을 payload에 채워 요청하면 해당 결과를 반환한다. 

#### 4. 완성된 스토리를 제공하는 챗봇

```
==================================================
안녕!!
뭘 원하니? : 오늘 서울 날씨 어때?
response: 2016년 10월 06일 날씨 어때?
{'end': datetime.datetime(2016, 10, 6, 23, 59, 59), 'start': datetime.datetime(2016, 10, 6, 0, 0)}
--------------------------------------------------
어디야?
['서울', '대구', '@text']
response : 서울
--------------------------------------------------
언제?
['오늘', '내일', '@date_picker']
response : 20161006_000000
**************************************************
{'response': '2016년10월06일 서울의 날씨는 맑음 입니다.', 'code': 200}
==================================================
뭘 원하니? : 주식 알려줘
response: 주식 알려줘
{'end': datetime.datetime(2016, 10, 6, 23, 59, 59), 'start': datetime.datetime(2016, 10, 6, 0, 0)}
--------------------------------------------------
주식 이름?
['삼성전자', '엘지', '@text']
response : 삼성전자
**************************************************
This function is not implemented yet
Please implement RESTful API for [get_stock]
==================================================

```

+ 현재 몇가지 도시들에 대한 리스트를 가지고있어 해당 도시들의 이름이 있는 경우 도시에 대한 개체명인식을 자동적으로 수행한다. 그래서 아래와 같은 경우 사용자의 입력을 받지않고 스스로 개체명인식을 수행하여 필드를 채워넣는다.

```
어디야?
['서울', '대구', '@text']
response : 서울
```



## Chatbot Builder

#### 실행
```bash
cd $CE_HOME/chatbot_builder
python3 chatbot_builder.py
```

##
Author : Sung-ju Kim
Email : sjkim@nomadconnection.com, goddoe2@gmail.com
Blog : goddoe.github.com
