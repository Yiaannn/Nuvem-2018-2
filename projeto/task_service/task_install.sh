#!/usr/bin/env bash
#Script de init das instances
cd /home/ubuntu
git clone https://github.com/Yiaannn/Nuvem-2018-2

#Credenciais AWS
export AWS_ACCESS_KEY_ID={}
export AWS_SECRET_ACCESS_KEY={}
export AWS_DEFAULT_REGION={}

sudo apt-get update
sudo apt-get install -y python3-pip
pip3 install flask flask_restful boto3
python3 ./Nuvem-2018-2/projeto/task_service/task_service.py &> task_service.log &
