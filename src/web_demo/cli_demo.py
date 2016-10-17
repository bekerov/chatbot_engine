# Author : Sung-ju Kim
# Email : goddoe2@gmail.com
import os
import sys
from datetime import datetime
import pickle
import json
from pprint import pprint

import requests

from socket import *
from time import ctime

from modules.named_entity_recognizer.named_entity_recognizer import NamedEntityRecognizer
from modules.query_classifier import QueryClassifier
from modules.various_utils import generateLogger, get_time_prefix

story_dir_path = os.environ['CE_SRC']+'/data/story'
query_classifier_path = os.environ['CE_SRC']+'/data/query_classifier/query_classifier.pickle'
story_type_dict_dict_path =os.environ['CE_SRC']+'/data/chatbot_info/story_type_dict_dict.pickle'



def main():
    os.system("clear")

    # config 
    protocol = "http://" 
    server_address ="localhost" 
    server_port = 6000 
    #server_url = protocol+server_address+":"+str(server_port)

    
    # load query_classifier
    query_classifier = QueryClassifier()
    query_classifier.load(query_classifier_path)

    # load story_type_dict_dict
    with open(story_type_dict_dict_path,"rb") as f:
        story_type_dict_dict = pickle.load(f) 
    story_type_dict = story_type_dict_dict['story_type_dict']
    reverse_story_type_dict = story_type_dict_dict['reverse_story_type_dict']

    # load story
    story_path_list = [story_dir_path+'/'+ story for story in os.listdir(story_dir_path) if story[-5:] == '.json'] 

    story_dict = {}

    for story_path in story_path_list:
        with open(story_path, "rt") as f:
            story = json.loads(f.read())
            story_dict[story['target_function']] = story

    # generate NamedEntityRecognizer

    #path_dict
    path_dict = { 'stock_dict_path':str(os.environ['CE_SRC'])+"/data/modules/stock_dict_from_db.pickle"
            
                }

    named_entity_recognizer = NamedEntityRecognizer(path_dict)

    pprint(story_dict)    
    pprint("="*50)

    host_serv = '' 
    port_serv = 21571
    buff_size = 2048
    addr_serv = (host_serv, port_serv)
    
    tcpSerSock = socket(AF_INET, SOCK_STREAM)  
    tcpSerSock.bind(addr_serv) 
    tcpSerSock.listen(10)

    tcpCliSock, addr_client = tcpSerSock.accept()

    def recv():
        pprint("here")
        result =tcpCliSock.recv(buff_size).decode() 
        pprint(result)
        pprint("here end")
        return result

    def send(src):
        return tcpCliSock.send(src.encode())

    input = recv
    print = send


    # chatbot start!
    #print("안녕!!")
    while(True):
        #print("뭘 원하니? : ")
        
        query = input()
        pprint(query)
        label = query_classifier.classify(query)
        function_name = story_type_dict[int(label)]

        # recognize named entities
        entity_dict = named_entity_recognizer.recognize(query)

        question_list =story_dict[function_name]['question_list'] 

        answer_dict = {}

        #request_string =""
        #request_string += function_name

        for question in question_list :
            print("-"*50)
            print(question['question']) 
            
            param_type = question['parameter']['parameter_type']
            param_name = question['parameter']['parameter_name']
            answer = None
            if param_type in entity_dict:
                answer = entity_dict[param_type]

            print(question['choice_list']) 
            print("response : ")

            if answer == None:
                response = input()
            else:
                response = answer
                print(response)
            
            answer_dict[param_name] = response

        print("*"*50)
        try:
            server_url = protocol +story_dict[function_name]['api_server_address']+':'+str(story_dict[function_name]['api_server_port'])
            print(server_url)            
            result = requests.get(server_url+"/"+function_name, params=answer_dict)
            pprint(result.json())
        except Exception as e:
            print("This function is not implemented yet")
            print("Please implement RESTful API for ["+function_name+"]")
            #print(e)
          
        print("="*50)
    tcpCliSock.close()
if __name__=="__main__":
    main()
