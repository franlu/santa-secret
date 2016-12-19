#!/usr/bin/env python
# -*- coding: utf-8 -*-
import random
import itertools

from flask import Flask, jsonify
from flask_pymongo import PyMongo
from flask_restful import Resource, Api, reqparse

app = Flask(__name__)
api = Api(app)
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

PAIR = []


def pairing(giver, receiver):
    for g, r in itertools.izip_longest(giver, receiver):
        if g == r:
            return False
    return True


class Participant(Resource):
    def get(self):
        return jsonify({"status": "ok", "data": PARTICIPANT})

    def post(self):
        try:
            parser = reqparse.RequestParser()
            parser.add_argument('name', type=str, help='Participant\'s Name')
            parser.add_argument('age', type=int, help='Participant\'s Age')

            args = parser.parse_args()
            _participantName = args['name']
            _participantAge = args['age']

            PARTICIPANT.append({
                "name": _participantName,
                "age": _participantAge
            })

            # do the pairing
            names = []
            for p in PARTICIPANT:
                names.append(p["name"])
            givers = list(names)
            receivers = list(names)
            while not pairing(givers, receivers):
                random.shuffle(givers)
                random.shuffle(receivers)

            for g, r in itertools.izip_longest(givers, receivers):
                PAIR.append({
                    "giver": g,
                    "receiver": r
                })

            return jsonify({"status": "ok", "message": "Participant added"})

        except Exception as e:
            return {'error': str(e)}


class Pair(Resource):
    def get(self):
        return jsonify({"status": "ok", "data": PAIR})

    def post(self):
        try:
            parser = reqparse.RequestParser()
            parser.add_argument('name', type=str, help='Giftee\'s Name')

            args = parser.parse_args()
            _gifteeName = args['name']

            giftee = ""
            for p in PAIR:
                if p["giver"] == _gifteeName:
                    giftee = p["receiver"]

            return jsonify({
                "status": "ok",
                "message": "Giftee\'s Name: %s" % giftee
            })

        except Exception as e:
            return {'error': str(e)}


api.add_resource(Participant, "/api/participant/", endpoint="participant")
api.add_resource(Pair, "/api/pair/", endpoint="pair")


if __name__ == "__main__":
    app.run(debug=True)
