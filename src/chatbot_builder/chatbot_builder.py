# Author : Sung-ju Kim
# Email : goddoe2@gmail.com
import os
from datetime import datetime
import pickle
import json
from pprint import pprint

from modules.query_classifier import QueryClassifier
from modules.various_utils import generateLogger, get_time_prefix

#logger = generateLogger("./chatbot_builder.log","chatbot_builder")
story_dir_path = os.environ['CE_SRC']+'/data/story'
query_classifier_path = os.environ['CE_SRC']+'/data/query_classifier/query_classifier.pickle'
story_type_dict_dict_path =os.environ['CE_SRC']+'/data/chatbot_info/story_type_dict_dict.pickle'
resource_name_list_path =os.environ['CE_SRC']+'/data/chatbot_info/resource_name_list.pickle'

class ChatbotBuilder(object):

    def __init__(self):

        self.function_dict = {
                            "get_weather":get_weather,
                        }

        self.story_type_dict = {}
        self.reverse_story_type_dict = {}
        self.resource_name_list= []

        self.query_classifier = None

    def build_stories(self):

        story_path_list = [story_dir_path+'/'+ story for story in os.listdir(story_dir_path) if story[-5:] == '.json'] 
        
        print(story_path_list)

        story_list = []

        for story_path in story_path_list:
            with open(story_path, "rt") as f:
                story = json.loads(f.read())
                story_list.append(story)
                print(story)

        # make train set
        sentence_list = []
        label_list  =[]

        for i, story in enumerate(story_list) :

            # add resource_name_list
            parameter_list = story['parameter_list']
            for parameter in parameter_list:
                self.resource_name_list.append(parameter['parameter_name'])

            self.story_type_dict[i] = story['target_function']
            self.reverse_story_type_dict['target_function'] = i

            for query in story['query_list']:
                sentence_list.append(query['query'])
                label_list.append(i)

                #should be deleted
                sentence_list.append(query['query'])
                label_list.append(i)
                sentence_list.append(query['query'])
                label_list.append(i)
                #/should be deleted

        query_classifier = QueryClassifier()
        query_classifier.train(sentence_list, label_list)

        self.query_classifier = query_classifier

        # save query_classifier
        with open(query_classifier_path,"wb") as f:
            query_classifier.save(query_classifier_path)

        # save story_type_dict
        with open(story_type_dict_dict_path, "wb") as f:
            story_type_dict_dict = {
                                        "story_type_dict":self.story_type_dict,
                                        "reverse_story_type_dict":self.reverse_story_type_dict,
                                    }

            pickle.dump(story_type_dict_dict, f)

        # save parameter_list
        self.resource_name_list = list(set(self.resource_name_list))
        with open(resource_name_list_path, "wb") as f:
            pickle.dump(self.resource_name_list,f)


    def make_story(self):

        print("="*50)
        print("make story start!")
   
        print("target_function (function name) : ", end='')
        target_function = input() 

        print("number of parameters to call target_function : ", end='')
        num_para = int(input())

        parameter_list = []
        for i in range(num_para):
            print("parameter name "+ str(i)+ " : ", end='')

            parameter_info = input()

            parameter, parameter_type = parameter_info.split(":")

            parameter_dict = { 'parameter_name': parameter,
                                'parameter_type': parameter_type
                                }
            parameter_list.append(parameter_dict)   

        query_list=[]

        print("make user query")
        print("to exit: exit")
        while True:
            print("user say like : ", end='')
            query = {}
            q = input().strip()
            if q == 'exit':
                break 

            query['query']= q
            query_list.append(query)
        

        print("-"*50)
        print("make bot questions\n")

        question_list=[]
        
        for i, parameter_dict in enumerate(parameter_list):
            question = {}
            
            parameter = parameter_dict['parameter_name']
            question['parameter'] = parameter_dict

            print("question for ["+parameter+"] : ", end='')
            question['question'] = input()

            print("number of choices : " ,end ='')
            num_choices = int(input())
            
            choice_list = [] 
            for i in range(num_choices):
                print("choice : ", end='') 
                choice = input()
                choice_list.append(choice)

            question['choice_list'] = choice_list
            question_list.append(question)
            print("-"*25)

        story = {
                    "target_function":target_function,
                    "parameter_list":parameter_list,
                    "query_list":query_list,
                    "question_list":question_list,
                }

        pprint(story)

        # save story
        save_path_pickle =story_dir_path+"/"+story['target_function']+".pickle" 
        save_path_json =story_dir_path+"/"+story['target_function']+".json" 

        #with open(save_path_pickle, "wb") as f:
        #    pickle.dump(story, f)
        
        with open(save_path_json, "wt") as f:
            f.write(str(story).replace("'",'"'))


def get_weather(location, date_time):
   
    print(location)
    print(date_time)

    return "return weather"


def test(chatbot_builder, query):
    result = chatbot_builder.query_classifier.classify(query)
    function_name = chatbot_builder.story_type_dict[int(result)]
    
    print("="*50)
    print("query : "+ query)
    print("matched function : "+function_name)


def main():
    os.system("clear")
    chatbot_builder = ChatbotBuilder()
    chatbot_builder.make_story()
    chatbot_builder.make_story()
    chatbot_builder.build_stories() 

    test(chatbot_builder, "오늘 날씨 어때?")
    test(chatbot_builder, "주식 알려줘 ?")
    test(chatbot_builder, "테스트?")


if __name__ == '__main__':
    main()

