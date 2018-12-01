import boto3
import requests
import time
from datetime import datetime as dt
from datetime import timezone

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

def create_instance(ec2, init_script):
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
                    },
                    {
                        'Key': 'Service',
                        'Value': 'task_service'
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


def filter_active(my_instances):
    active_instances= []
    for instance in my_instances:
        target_codes=[0, 16] #pending ou running
        if instance.state['Code'] in target_codes:
            active_instances.append(instance)

    return active_instances

def filter_stable(my_instances):
    stable_instances= []
    for instance in my_instances:
        if instance.state['Code'] == 16: #running

            #checar agora se ela ainda não está no mercy time de inicialização
            mercy_time= 5 #em minutos
            utc_uptime = dt.now(timezone.utc) - instance.launch_time
            delta_minutes= utc_uptime.total_seconds() / 60

            if delta_minutes > mercy_time:
                stable_instances.append(instance)

    return stable_instances

def healthcheck(my_instances):
    health_failed_instances=[]

    for instance in my_instances:
        url="http://"+instance.public_ip_address+':5000'+'/healthcheck'
        try:
            response= requests.get(url)
            if response.status_code != 200:
                health_failed_instances.append(instance)
        except:
            #Não recebo uma resposta
            health_failed_instances.append(instance)

    return health_failed_instances

def main():
    #Monitora as instâncias, a saúde delas, reinicializa conforme necessário, guarda o ip das stable

    ec2_client= boto3.client('ec2')
    ec2_resource= boto3.resource('ec2')

    with open('task_install.sh', 'r') as install_task:
        init_script= install_task.read()

    while(True):
        print("Rechecando...")

        my_instances= get_my_instances(ec2_resource)
        active_instances= filter_active(my_instances)

        #cria novas
        instances_to_create= INSTANCES_AMOUNT - len(active_instances)
        for i in range(instances_to_create):
            create_instance(ec2_resource, init_script)
            pass

        #apaga caídas
        stable_instances= filter_stable(my_instances)
        health_failed_instances= healthcheck(stable_instances)
        for instance in health_failed_instances:
            print("Instância de IPv4 "+instance.public_ip_address+" falhou o healthcheck, apagando...")
            stable_instances.remove(instance)
            #instance.terminate()


        #salva os IPs
        ips_string= ""

        if stable_instances:
            for instance in stable_instances:
                ips_string+= instance.public_ip_address+'\n'
            ips_string= ips_string[:-1]
        with open('active_ips.txt', 'w') as ips_file:
            ips_file.write(ips_string)

        time.sleep(10)

INSTANCES_AMOUNT= int(os.environ.get('LOAD_BALANCER_INSTANCE_AMOUNT'))

main()
