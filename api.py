#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import Flask, jsonify, url_for, redirect, request
from flask_pymongo import PyMongo
from flask_restful import Api, Resource

app = Flask(__name__)
# app.config["MONGO_DBNAME"] = "santa_secret_db"
# mongo = PyMongo(app, config_prefix='MONGO')
# APP_URL = "http://127.0.0.1:5000"


PARTICIPANT = [
    {
        "name": "juan",
        "age": "32",
    },
    {
        "name": "carlos",
        "age": "30",
    },
    {
        "name": "ana",
        "age": "28",
    }

]

PAIR = [
    {
        "giver": "",
        "reciver": "",
    }
]


class Participant(Resource):
    def get(self):
        return jsonify({"status": "ok", "data": PARTICIPANT})

    def post(self):    

class Pair(Resource):
    def get(self, name):
        pass

api = Api(app)
# api.add_resource(Index, "/", endpoint="index")
api.add_resource(Participant, "/api/participant", endpoint="participant")
api.add_resource(Pair, "/api/participant/add/", endpoint="participant_add")
api.add_resource(Pair, "/api/pair", endpoint="pair")
api.add_resource(Pair, "/api/pair/<string:giver>", endpoint="giver")


if __name__ == "__main__":
    app.run(debug=True)
