#!/usr/bin/env bash
#Script de init das instances
git clone https://github.com/Yiaannn/Nuvem-2018-2

sudo apt-get update
sudo apt-get install -y python3-pip
pip3 install flask flask_restful
python3 ./Nuvem-2018-2/aps1/task_service.py &> task_service.log &
sleep 3
curl -Is http://127.0.0.1:5000/healthcheck | head -1
