import boto3
import json
from botocore.exceptions import ClientError
import time

def jprint(json_dict):
    print(json.dumps(json_dict, sort_keys=True, indent=4))

def keypair_init(ec2):
    print("Limpango chave antiga...")
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

def instance_init(ec2, init_script):
    #botar minha keypair, security group e setar a mim mesmo como Owner
    #tipo t2.micro com ubuntu 18(.04? Imagino que sim por ser LTS)

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

def get_my_instances(ec2):
    my_instances=[]
    for instance in ec2.instances.all():

        tag= instance.tags[0]
        if tag['Key'] == 'Owner' and tag['Value'] == 'alexandre':
            my_instances.append(instance)

    return my_instances

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
        for instance in my_instances:
            my_instances= get_my_instances(ec2)
            need_to_check= False

            if instance.state['Code'] != 48: #48 marca termination
                print("Esperando instância de IPv4 "+instance.public_ip_address+' terminar.' )
                need_to_check= True
                break
        time.sleep(wait_time)
        wait_time+= 4

def cloud_init():

    print('Reinicializando.')

    ec2_client= boto3.client('ec2')
    ec2_resource= boto3.resource('ec2')
    with open('task_install.sh', 'r') as file:
        init_script=file.read()

        terminate_my_instances(ec2_resource, True)
        keypair_init(ec2_client)
        secgroup_init(ec2_client)
        for i in range(3):
            instance_init(ec2_resource, init_script)

cloud_init()
