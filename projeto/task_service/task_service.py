#!/usr/bin/env python3

from flask import Flask, abort
from flask_restful import Api, Resource, reqparse
import boto3
import json
import time

app = Flask(__name__)
api = Api(app)

task_keys=['id', 'description', 'priority', 'is_done']

bucket_name= 'alexandre-bucket'

class DBManager():

    s3_resource= boto3.resource('s3')
    s3_client= boto3.client('s3')

    def lock():
        lock= '1'

        while lock == '1':
            time.sleep(1)

            DBManager.s3_resource.Bucket(bucket_name).download_file('dblock', 'dblock')
            with open('dblock', 'r') as f:
                lock= f.read(1)
                #Esperar por lock == 0

        lock='1'
        with open('dblock', 'w') as f:
            f.write(lock)
        DBManager.s3_client.upload_file('dblock', bucket_name, 'dblock')

    def unlock():
        lock= '0'
        with open('dblock', 'w') as f:
            f.write(lock)
        DBManager.s3_client.upload_file('dblock', bucket_name, 'dblock')

    def get_tasks():

        DBManager.s3_resource.Bucket(bucket_name).download_file('tasksdb.json', 'tasksdb.json')
        with open('tasksdb.json', 'r') as f:
            body = json.load(f)
        return body

    def save_tasks(body):
        with open('tasksdb.json', 'w') as f:
            json.dump(body, f)
        DBManager.s3_client.upload_file('tasksdb.json', bucket_name, 'tasksdb.json')

class TaskGroup(Resource):

    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('description', type=str, location='json')
        self.reqparse.add_argument('priority', type=int, location='json')

        Resource.__init__(self)

    def get(self):
        DBManager.lock()
        # lista todas as tarefas do dicionário
        tasksdb= DBManager.get_tasks()

        DBManager.unlock()
        return tasksdb, 200

    def post(self):
        DBManager.lock()

        param_dict = self.reqparse.parse_args()
        tasksdb= DBManager.get_tasks()

        task = {
            'id': tasksdb['tasks'][-1]['id'] + 1,
            'description': param_dict['description'],
            'priority': param_dict['priority'],
            'is_done': False
        } #considerando que no meu init eu requesito esses parametros, o que acontece se eu omitir um?


        tasksdb['tasks'].append(task)
        DBManager.save_tasks(tasksdb)

        DBManager.unlock()
        return {'task': task}, 201

class Task(Resource): #mudei o nome pra task só pelo bem de manter todo o código não-comentado em inglês
    #Fazer pelo menos dois atributos

    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('description', type=str, location='json') #Atributo 1
        self.reqparse.add_argument('priority', type=int, location='json') #Atributo 2
        self.reqparse.add_argument('is_done', type=bool, location='json') #Atributo 3
        Resource.__init__(self)

    def get(self, id):
        DBManager.lock()

        tasksdb= DBManager.get_tasks()
        task= self.find(tasksdb, id)

        DBManager.unlock()
        return { 'task': task }, 200

    def put(self, id):
        DBManager.lock()

        tasksdb= DBManager.get_tasks()
        task= self.find(tasksdb, id)

        param_dict= self.reqparse.parse_args()

        for key in param_dict.keys():
            if key not in task:
                abort(422)

        for key, value in param_dict.items():
            if value is not None:
                task[key]= value

        DBManager.save_tasks(tasksdb)

        DBManager.unlock()
        return { 'task': task }, 200

    def delete(self, id):
        DBManager.lock()

        tasksdb= DBManager.get_tasks()
        task= self.find(tasksdb, id)

        tasksdb['tasks'].remove(task)

        DBManager.save_tasks(tasksdb)

        DBManager.unlock()
        return {'task': task}, 200

    #funções só pra reduzir redundância de código

    def find(self, tasksdb, id):
        found= None
        for task in tasksdb['tasks']:
            if id == task['id']:
                found= task
                break

        if found is None:
            abort(404)

        return found

class HealthCheck(Resource):
    #não entendi a necessidade deste, mas enfim

    def get(self):
        return ('', 200) #se não retorno conteúdo, não deveria ser 204?

api.add_resource(Task, '/Tarefa/<int:id>')#, endpoint = 'task_dict')
api.add_resource(TaskGroup, '/Tarefa')#, endpoint = 'task_dict')
api.add_resource(HealthCheck, '/healthcheck')#, endpoint = 'task_dict')

app.run(debug=True,host="0.0.0.0",port = 5000)
