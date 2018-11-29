from shade import *
import json

simple_logging(debug=True)
conn= openstack_cloud(cloud='maas')

#Listar as opcoes disponiveis de imagens e flavors

def list_options():
	images= conn.list_images()
	for image in images:
		print(json.dumps(image, indent=4))

	flavors= conn.list_flavors()
	for flavor in flavors:
		print(json.dumps(flavor, indent=4))

#Lancar uma instancia minimalista

def launch_minimal():
	image_id= '9821864e-ba71-4988-9dc4-1b56d5fdd0d1'
	image= conn.get_image(image_id)
	print(json.dumps(image, indent=4))

	flavor_id= '0cb1f143-8b9a-4367-8ab3-9be101ceb305'
	flavor= conn.get_flavor(flavor_id)
	print(json.dumps(image, indent=4))

	#

	instance_name= 'alexandre-proto2'
	test_instance= conn.create_server(wait=True, auto_ip=True, name=instance_name, image=image_id, flavor=flavor_id)
	print(json.dumps(test_instance, indent=4))

#Listar as instancias

def list_instances():
	instances= conn.list_servers()
	for instance in instances:
		print(json.dumps(instance, indent=4))

#Destruir as minhas instancias

def destroy_instances(instance_id_list):
	for instance_id in instance_id_list:
		conn.delete_server(instance_id)

#Preparar/Validar minha keypair

def prepare_keypair():
	print('Checking for existing SSH keypair...')
	keypair_name= 'maaskey'
	pub_key_file= '/home/cloud/.ssh/id_rsa.pub'

	if conn.search_keypairs(keypair_name):
		print('Keypair already exists. Skipping Import.')
	else:
		print('Adding keypair...')
		conn.create_keypair(keypair_name, open(pub_key_file, 'r').read().strip())

	for keypair in conn.list_keypairs():
		print(json.dumps(keypair, indent=4))

#Preparar/Validar meu security group

def prepare_sec_group():
	print('Checking for existing security groups...')
	sec_group_name= 'alexandre-security'

	if conn.search_security_groups(sec_group_name):
		print('Security group already exists. Skipping creation.')
	else:
		print('Creating security group.')
		conn.create_security_group(sec_group_name, 'Security Group Teste feito durante o tutorial Shade.')
		conn.create_security_group_rule(sec_group_name, 80, 80, 'TCP')
		conn.create_security_group_rule(sec_group_name, 22, 22, 'TCP')

	conn.search_security_groups(sec_group_name)

#Lancar uma instancia pre-configurada

def launch_configured():
	ex_userdata = '''#!/usr/bin/env bash

curl -L -s https://git.openstack.org/cgit/openstack/faafo/plain/contrib/install.sh | bash -s -- \
-i faafo -i messaging -r api -r worker -r demo
'''

	instance_name = 'alexandre-all-in-one'
	image_id= '9821864e-ba71-4988-9dc4-1b56d5fdd0d1'
	flavor_id= '0cb1f143-8b9a-4367-8ab3-9be101ceb305'
	keypair_name= 'maaskey'
	sec_group_name= 'alexandre-security'

	testing_instance = conn.create_server(wait=True, auto_ip=False,
		name=instance_name,
		image=image_id,
		flavor=flavor_id,
		key_name=keypair_name,
		security_groups=[sec_group_name],
		userdata=ex_userdata)


#Listar meus IPs flutuantes disponiveis

def list_floating_ips():

	f_ip = conn.available_floating_ip(network='7196d7d8-426a-4d1b-9be4-4355acf59172')
	print(json.dumps(f_ip, indent=4))
