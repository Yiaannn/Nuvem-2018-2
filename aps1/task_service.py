#!/usr/bin/env python3

from flask import Flask, abort
from flask_restful import Api, Resource, reqparse

app = Flask(__name__)
api = Api(app)

task_list = [
    {
        'id': 0,
        'description': u'Primeira tarefa de exemplo: duplicar Tribbles',
        'priority': 0,
        'is_done': False
    },
    {
        'id': 1,
        'description': u'Segunda tarefa de exemplo: Aprender a usar strings unicode em python',
        'priority': 7,
        'is_done': False
    }
]

task_keys=['id', 'description', 'priority', 'is_done']

class TaskGroup(Resource):

    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('description', type=str, location='json')
        self.reqparse.add_argument('priority', type=int, location='json')

        Resource.__init__(self)

    def get(self):
        # lista todas as tarefas do dicionário

        return { 'tasks': task_list}, 200

    def post(self):
        param_dict = self.reqparse.parse_args()

        task = {
            'id': task_list[-1]['id'] + 1,
            'description': param_dict['description'],
            'priority': param_dict['priority'],
            'is_done': False
        } #considerando que no meu init eu requesito esses parametros, o que acontece se eu omitir um?

        task_list.append(task)
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
        task= self.find(id)
        return { 'task': task }, 200

    def put(self, id):
        task= self.find(id)

        param_dict= self.reqparse.parse_args()

        for key in param_dict.keys():
            if key not in task:
                abort(422)

        for key, value in param_dict.items():
            if value is not None:
                task[key]= value
        return { 'task': task }, 200

    def delete(self, id):
        task= self.find(id)
        task_list.remove(task)

        return {'task': task}, 200

    #funções só pra reduzir redundância de código

    def find(self, id):
        found= None
        for task in task_list:
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
