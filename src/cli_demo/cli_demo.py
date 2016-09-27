# Author : Sung-ju Kim
# Email : goddoe2@gmail.com
import os
import sys
from datetime import datetime
import pickle
import json
from pprint import pprint

from modules.query_classifier import QueryClassifier
from modules.various_utils import generateLogger, get_time_prefix


story_dir_path = os.environ['CE_SRC']+'/data/story'
query_classifier_path = os.environ['CE_SRC']+'/data/query_classifier/query_classifier.pickle'
story_type_dict_dict_path =os.environ['CE_SRC']+'/data/chatbot_info/story_type_dict_dict.pickle'

def main():
    os.system("clear")
    
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


    pprint(story_dict)    
    print("="*50)

    # chatbot start!
    print("안녕!!")
    while(True):
        print("뭘 원하니? : ", end='')
        
        query = input()
        label = query_classifier.classify(query)
        function_name = story_type_dict[int(label)]
        #pprint(story_dict[function_name])

        question_list =story_dict[function_name]['question_list'] 
        for question in question_list :
            print("-"*25)
            print(question['question']) 
            print(question['choice_list']) 
            print("respose : ", end='')
            response = input()
            print("-"*25)

        print("="*50)
if __name__=="__main__":
    main()
