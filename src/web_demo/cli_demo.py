# Author : Sung-ju Kim
# Email : goddoe2@gmail.com
import os
import sys
from datetime import datetime
import pickle
import json
from pprint import pprint
import time
import requests

from socket import *
from time import ctime

from modules.named_entity_recognizer.named_entity_recognizer import NamedEntityRecognizer
from modules.query_classifier import QueryClassifier
from modules.various_utils import generateLogger, get_time_prefix

story_dir_path = os.environ['CE_SRC']+'/data/story'
query_classifier_path = os.environ['CE_SRC']+'/data/query_classifier/query_classifier.pickle'
story_type_dict_dict_path =os.environ['CE_SRC']+'/data/chatbot_info/story_type_dict_dict.pickle'


class Chatbot(object):

    def __init__(self):

        self.step_idx = 0
        self.step_idx_max = 0
        self.question_idx= 0
        self.question_idx_max = 0

        self.process = []

        self.function_name = ''
        self.question_list = []
        self.current_story = None

        self.process = [ ]
        self.process.append(self.classify_query)

        self.protocol = "http://"
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

        self.query_classifier = query_classifier
        self.story_dict = story_dict
        self.story_type_dict = story_type_dict
        self.named_entity_recognizer = named_entity_recognizer

    def init_chatbot(self):
        self.step_idx = 0
        self.step_idx_max = 0
        self.question_idx= 0
        self.question_idx_max = 0

        self.function_name = ''
        self.question_list = []
        self.current_story = None
        self.process = []
        self.process.append(self.classify_query)

    def talk(self, query):

        while True :

            current_task = self.process[self.step_idx]
            msg = current_task(query)
            
            if msg == 'next' :
                continue

            return msg
            

    def classify_query(self,query):
        label = self.query_classifier.classify(query)

        function_name = self.story_type_dict[int(label)]

        # recognize named entities
        entity_dict = self.named_entity_recognizer.recognize(query)

        question_list =self.story_dict[function_name]['question_list'] 

        answer_dict = {}

        self.current_story = self.story_dict[function_name] 

        parameter_name_list = [ item['parameter_name'] for item in self.current_story['parameter_list']] 
        for key, value in entity_dict.items(): 
            if value != None and key in parameter_name_list:
                answer_dict[key] = value

        for i in range(len(question_list)):
            self.process.append(self.get_question)
            self.process.append(self.receive_answer)
        self.process.append(self.get_result)

        self.step_idx_max = len(self.process)
        self.question_idx_max = len(question_list)

        self.function_name = function_name
        self.question_list = question_list
        self.answer_dict = answer_dict
        self.step_idx = 1

        return 'next'

    def receive_answer(self, query):
        self.answer_dict[self.current_question_parameter] = query
        self.step_idx += 1

        return 'next'


    def get_question(self,query):

        msg = {
                'text': '',
                'choice_list':[]
                }
        
        while True: 
            current_question = self.question_list[self.question_idx] 
            current_parameter_name = current_question['parameter']['parameter_name'] 
            self.current_question_parameter = current_question['parameter']['parameter_name'] 

            if current_parameter_name in self.answer_dict:
                self.question_idx += 1
                self.step_idx += 2
                return 'next'


            self.question_idx += 1
            self.step_idx += 1
            msg['text'] = current_question['question']
            msg['choice_list'] = current_question['choice_list']

            return msg


    def get_result(self,query):
        msg = {
                'text': '',
                }
        
        try:
            server_url = self.protocol +self.current_story['api_server_address']+':'+str(self.current_story['api_server_port'])
            if len(self.current_story['additional_path'].strip()) > 0:
                server_url += '/'+self.current_story['additional_path']

            result = requests.get(server_url+"/"+self.function_name, params=self.answer_dict)

            msg['text'] =str(result.json())  
            return msg

        except Exception as e:
            #pprint("This function is not implemented yet")
            #print("Please implement RESTful API for ["+function_name+"]")

            msg['text'] = str(e)  
            print("error")
            return msg
        finally:
            self.init_chatbot()

    def save(self, path):
        chatbot_data_dict = {
                    'step_idx' :self.step_idx,
                    'step_idx_max' : self.step_idx_max, 
                    'question_idx' : self.question_idx,
                    'question_idx_max' : self.question_idx_max ,

                    'process' : self.process ,

                    'process' : self.function_name,
                    'question_list' : self.question_list,
                    'current_story' : self.current_story,

                    'process' : self.process ,
                    }
        with open(path, "wb") as f:
            pickle.dump(chatbot_data_dict,f)


    def load(self, path): 
        with open(path, "rb") as f:
            chatbot_data_dict = pickle.load(f)

        self.step_idx = chatbot_data_dict['step_idx']
        self.step_idx_max = chatbot_data_dict['step_idx_max']
        self.question_idx= chatbot_data_dict['question_idx']
        self.question_idx_max =chatbot_data_dict['question_idx_max'] 

        self.function_name = chatbot_data_dict['function_name'] 
        self.question_list = chatbot_data_dict['question_list']
        self.current_story = chatbot_data_dict['current_story']
        self.process = chatbot_data_dict['process'] 


def main():
    chatbot = Chatbot()
    while True:
        print(chatbot.talk(input()))

if __name__=="__main__":
    main()
