#!/usr/bin/env bash

source ./source_it_to_set_envs.sh
source ./envCE/bin/activate

nohup python ./src/chatbot_server/chatbot_rest_api_server.py &
nohup python ./src/chatbot_server/chatbot_rest_instance_server.py &
nohup python ./src/web_demo/app.py &
