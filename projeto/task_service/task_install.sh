#!/usr/bin/env bash
#Script de init das instances
cd /home/ubuntu
git clone https://github.com/Yiaannn/Nuvem-2018-2

sudo apt-get update
sudo apt-get install -y python3-pip
pip3 install flask flask_restful
python3 ./Nuvem-2018-2/projeto/task_service/task_service.py &> task_service.log &
