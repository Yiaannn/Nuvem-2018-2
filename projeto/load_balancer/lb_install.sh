#!/usr/bin/env bash
#este script precisa ser formatado antes pelo cloud_init para que ele adicione as variaveis de ambiente
cd /home/ubuntu
git clone https://github.com/Yiaannn/Nuvem-2018-2

#Credenciais AWS
export AWS_ACCESS_KEY_ID={}
export AWS_SECRET_ACCESS_KEY={}
export AWS_DEFAULT_REGION={}

#Quantas instancias quero que meu load balancer mantenha
export LOAD_BALANCER_INSTANCE_AMOUNT={}

sudo apt-get update
sudo apt-get install -y python3-pip
pip3 install flask flask_restful requests boto3
#Load Balancer precisa do script de install do task service também, passar ele pro home
cp ./Nuvem-2018-2/projeto/task_service/task_install.sh .
echo > active_ips.txt
python3 ./Nuvem-2018-2/projeto/load_balancer/lb_monitor.py &> lb_monitor.log &
python3 ./Nuvem-2018-2/projeto/load_balancer/lb_service.py &> lb_service.log &
