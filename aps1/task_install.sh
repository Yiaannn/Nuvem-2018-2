#!/usr/bin/env bash
sudo apt-get update
sudo apt-get install -y python3-pip
pip3 install flask flask_restful
python3 task_service.py &> task_service.log &
sleep 3
curl -Is http://127.0.0.1:5000/healthcheck | head -1
