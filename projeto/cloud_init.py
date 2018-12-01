import boto3
import json
from botocore.exceptions import ClientError
import time
import argparse
import os

def jprint(json_dict):
    print(json.dumps(json_dict, sort_keys=True, indent=4))

def keypair_init(ec2):
    print("Limpando chave antiga...")
    #apagar keypair
    response= ec2.delete_key_pair(KeyName='alexandre_keypair')
    #jprint(response)

    print("Gerando nova chave..")
    #criar keypair
    response= ec2.create_key_pair(KeyName='alexandre_keypair')
    #jprint(response)

    #tenho que salvar minha chave privada automaticamente em algum canto
    fname= "private_key.pem"
    f = open(fname, "w")
    f.write(response['KeyMaterial'])
    f.close()

    print("Nova chave salva em "+fname+".")

def secgroup_init(ec2):
    #apagar securitygroup
    print("Limpando o Security Group")
    try:
        response= ec2.delete_security_group(GroupName='alexandre_secgroup')
        #jprint(response)
    except ClientError:
        print("Security Group antigo não encontrado")

    #criar securitygroup
    response = ec2.create_security_group(GroupName='alexandre_secgroup',
                                         Description='alexandre_secgroup')

    secgroup_id = response['GroupId']
    print("Security Group inicializado")
    #jprint(response)


    response= ec2.authorize_security_group_ingress(
        GroupId=secgroup_id,
        IpPermissions=[
            {'IpProtocol': 'tcp',
             'FromPort': 5000,
             'ToPort': 5000,
             'IpRanges': [{'CidrIp': '0.0.0.0/0'}]},
            {'IpProtocol': 'tcp',
             'FromPort': 22,
             'ToPort': 22,
             'IpRanges': [{'CidrIp': '0.0.0.0/0'}]}
        ])

    print("Habilitadas as regras do Security Group")
    #jprint(response)

def load_balancer_init(ec2, init_script):


    instance= ec2.create_instances(
        KeyName='alexandre_keypair',
        SecurityGroups=['alexandre_secgroup'],
        TagSpecifications=[
            {
                'ResourceType': 'instance',
                'Tags':[
                    {
                        'Key': 'Owner',
                        'Value': 'alexandre'
                    },
                    {
                        'Key': 'Service',
                        'Value': 'load_balancer'
                    }
                ]
            }
        ],

        InstanceType='t2.micro',
        ImageId='ami-0ac019f4fcb7cb7e6',

        UserData=init_script,

        MaxCount=1,
        MinCount=1
    )

    print("Criada uma nova instância.")




def create_load_balancer(ec2, init_script):
    #botar minha keypair, security group e setar a mim mesmo como Owner
    #tipo t2.micro com ubuntu 18(.04? Imagino que sim por ser LTS)

    instances= ec2.create_instances(
        KeyName='alexandre_keypair',
        SecurityGroups=['alexandre_secgroup'],
        TagSpecifications=[
            {
                'ResourceType': 'instance',
                'Tags':[
                    {
                        'Key': 'Owner',
                        'Value': 'alexandre'
                    },
                    {
                        'Key': 'Service',
                        'Value': 'load_balancer'
                    }
                ]
            }
        ],

        InstanceType='t2.micro',
        ImageId='ami-0ac019f4fcb7cb7e6',

        UserData=init_script,

        MaxCount=1,
        MinCount=1
    )

    print("Criado um novo Load Balancer.")
    return instances[0]

def get_my_instances(ec2):
    my_instances=[]
    for instance in ec2.instances.all():

        check= 0
        for tag in instance.tags:
            if (tag['Key'] == 'Owner' and tag['Value'] == 'alexandre') or (tag['Key']=='Service' and tag['Value'] == 'task_service'):
                check+=1
        if check == 2:
            my_instances.append(instance)

    return my_instances

def get_load_balancers(ec2):
    load_balancers= []

    for instance in ec2.instances.all():

        check= 0
        for tag in instance.tags:
            if (tag['Key'] == 'Owner' and tag['Value'] == 'alexandre') or (tag['Key']=='Service' and tag['Value'] == 'load_balancer'):
                check+=1
        if check == 2:
            load_balancers.append(instance)

    return load_balancers

def terminate_load_balancer(ec2, wait):
    load_balancers= get_load_balancers(ec2)

    for load_balancer in load_balancers:
        target_codes=[0, 16, 64, 80]
        if load_balancer.state['Code'] in target_codes:
            load_balancer.terminate()
            print("Apagada a instância de IPv4 "+load_balancer.public_ip_address+'.')

    if not wait:
        return;

    need_to_check=True
    wait_time= 4

    print("Esperando Load Balancers terminarem...")
    while need_to_check:
        load_balancers= get_load_balancers(ec2)
        need_to_check= False
        for load_balancer in load_balancers:

            if load_balancer.state['Code'] != 48: #48 marca termination
                print("Esperando Load Balancer de IPv4 "+str(load_balancer.public_ip_address)+' terminar...' )
                need_to_check= True
                break
        time.sleep(wait_time)
        wait_time+= 4

def terminate_my_instances(ec2, wait):

    my_instances= get_my_instances(ec2)

    for instance in my_instances:
        #instance.state é um dicionário com Code e Name associados 1:1
        target_codes=[0, 16, 64, 80]
        if instance.state['Code'] in target_codes:
            instance.terminate()
            print("Apagada a instância de IPv4 "+instance.public_ip_address+'.')

    if not wait:
        return;

    need_to_check=True
    wait_time= 4
    #esperar minhas instâncias teminarem
    print("Esperando instâncias terminarem...")
    while need_to_check:
        my_instances= get_my_instances(ec2)
        need_to_check= False
        for instance in my_instances:

            if instance.state['Code'] != 48: #48 marca termination
                print("Esperando instância de IPv4 "+instance.public_ip_address+' terminar...' )
                need_to_check= True
                break
        time.sleep(wait_time)
        wait_time+= 4

def wait_until_running(load_balancer):
    need_to_check=True
    wait_time= 4

    while need_to_check:
        load_balancer.reload()
        print("Esperando Load Balancer iniciar...")
        if load_balancer.state['Code'] == 16: #48 marca running
            break

        time.sleep(wait_time)
        wait_time+= 4


def cloud_init(instance_amount):

    print('Reinicializando com '+str(instance_amount)+' instâncias a serem mantidas.')

    ec2_client= boto3.client('ec2')
    ec2_resource= boto3.resource('ec2')
    with open('task_service/task_install.sh', 'r') as file_task, open('load_balancer/lb_install.sh', 'r') as file_lb:

        session = boto3.Session()
        credentials = session.get_credentials()
        aws_access_key_id= credentials.access_key
        aws_secret_access_key= credentials.secret_key
        aws_default_region= session.region_name

        install_lb= file_lb.read().format(aws_access_key_id, aws_secret_access_key, aws_default_region, instance_amount)
        install_task= file_task.read()

    terminate_load_balancer(ec2_resource, True) #preciso matar o load balancer antes ou ele vai reinicializar instâncias
    terminate_my_instances(ec2_resource, True)
    keypair_init(ec2_client)
    secgroup_init(ec2_client)
    #for i in range(3):
    #    instance_init(ec2_resource, install_task)
    #Quem inicializa as instâncias agora é meu load balancer
    load_balancer= create_load_balancer(ec2_resource, install_lb)
    #Esperar que esteja estabilizado, pegar IP, setar na variavel de ambiente
    print("Esperando um IP ser provido para o load balancer...")
    wait_until_running(load_balancer)

    print("IP do Load Balancer: "+str(load_balancer.public_ip_address))
    url='http://'+load_balancer.public_ip_address+':5000'
    print("Sete a variável de ambiente TASKSERVICE_URL para '"+url+"' para poder usar o cliente.")
    print("Por conveniência, um script 'taskrc' foi criado, 'source taskrc' setará a variável")
    os.environ["TASKSERVICE_URL"] = url

    #Criar o arquivo
    content='export TASKSERVICE_URL='+url
    with open('taskrc', 'w') as taskrc:
        taskrc.write(content)

    print("Terminado, é necessário esperar alguns minutos até a nuvem se estabilizar antes de utilizá-la.")


#Preciso especificar quantas instâncias quero que meu load balancer mantenha
parser=argparse.ArgumentParser()
parser.add_argument('--amount', type=int, required=False, default=3, help='amount of instances to keep up')

args = parser.parse_args()
cloud_init(args.amount)
