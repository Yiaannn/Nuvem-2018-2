#!/usr/bin/env python3

from flask import Flask, abort, redirect, request
from flask_restful import Api, Resource, reqparse
from random import randint
import requests

app = Flask(__name__)
api = Api(app)

class Rerouter(Resource):

    def get(self, id):
        pass

    def post(self, id):
        pass

    def put(self, id):
        pass

    def delete(self, id):
        pass

    def __init__(self):
        self.get= self.catch_all
        self.patch= self.catch_all
        self.post= self.catch_all
        self.put= self.catch_all
        self.delete= self.catch_all
        self.copy= self.catch_all
        self.head= self.catch_all
        self.options= self.catch_all
        self.link= self.catch_all
        self.unlink= self.catch_all
        self.purge= self.catch_all
        self.lock= self.catch_all
        self.unlock= self.catch_all
        self.propfind= self.catch_all
        self.view= self.catch_all

        Resource.__init__(self)

    def get_ips(self):
        with open('active_ips.txt', 'r') as f:
            ips= []
            print("IPs ativos:")
            for line in f:
                ips.append(line.strip())
                print(ips[-1])
        return ips

    def choose_ip_randomly(self, ips):
        chosen_index= randint(0, len(ips)-1)
        print("IP a ser redirecionado: "+ips[chosen_index])
        return ips[chosen_index]

    def reroute(self, url, body, method):

        reroute_dict={
            'GET': requests.get,
            'PUT': requests.put,
            'POST': requests.post,
            'DELETE': requests.delete
        }

        response= reroute_dict[method](url, json=body)

        return response.json(), response.status_code

class RerouteTaskID(Rerouter):

    def catch_all(self, id):
        print("Redirecionando chamada.")
        ips= self.get_ips()
        if ips:
            ip= self.choose_ip_randomly(ips)

            id_url= '/'+str(id)
            url="http://"+ip+':5000'+'/Tarefa'+id_url

            return self.reroute(url, request.get_json(), request.method)
        return '', 423


class RerouteTask(Rerouter):

    def catch_all(self):
        print("Redirecionando chamada.")
        ips= self.get_ips()
        if ips:
            ip= self.choose_ip_randomly(ips)

            url="http://"+ip+':5000'+'/Tarefa'

            return self.reroute(url, request.get_json(), request.method)
        return '', 423

class RerouteHealthCheck (Rerouter):

    def catch_all(self):
        print("Redirecionando chamada.")
        ips= self.get_ips()
        if ips:
            ip= self.choose_ip_randomly(ips)

            url="http://"+ip+':5000'+'/healthcheck'

            return self.reroute(url, request.get_json(), request.method)
        return '', 423


api.add_resource(RerouteTaskID, '/Tarefa/<int:id>')
api.add_resource(RerouteTask, '/Tarefa')
api.add_resource(RerouteHealthCheck, '/healthcheck')

app.run(debug=True,host="0.0.0.0",port = 5000)
