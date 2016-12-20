#!/usr/bin/env python
# -*- coding: utf-8 -*-
import itertools
import random

from bson.json_util import dumps
from common.util import pairing
from flask import Flask, g, jsonify
from flask_pymongo import PyMongo
from flask_restful import Resource, Api, reqparse


app = Flask(__name__)
api = Api(app)
app.config["MONGO_DBNAME"] = "santa_secret_db"
mongo = PyMongo(app, config_prefix='MONGO')


class Participant(Resource):
    def get(self):
        participants = mongo.db.participant.find()
        data = []
        for p in participants:
            data.append({"name": p["name"], "age": p["age"]})
        return jsonify({"status": "ok", "data": data})

    def post(self):
        try:
            parser = reqparse.RequestParser()
            parser.add_argument('name', type=str, help='Participant\'s Name')
            parser.add_argument('age', type=int, help='Participant\'s Age')

            args = parser.parse_args()
            _participantName = args['name']
            _participantAge = args['age']
            p = mongo.db.participant.find({
                "name": _participantName,
                "age": _participantAge
            })
            if p.count() > 0:
                return jsonify({
                    "status": "ok",
                    "message": "The participant already exists."})
            mongo.db.participant.insert({
                "name": _participantName,
                "age": _participantAge
            })

            return jsonify({"status": "ok", "message": "Participant added"})

        except Exception as e:
            return {'error': str(e)}


class Pair(Resource):
    def get(self):
        pairs = mongo.db.pair.find()
        data = []
        for p in pairs:
            data.append({"giver": p["giver"], "receiver": p["receiver"]})
        return jsonify({"status": "ok", "data": data})

    def post(self):
        try:
            parser = reqparse.RequestParser()
            parser.add_argument('name', type=str, help='Giftee\'s Name')
            args = parser.parse_args()
            _gifteeName = args['name']
            participant = mongo.db.participantfind_one({"giver": _gifteeName})

            return jsonify({
                "status": "ok",
                "message": "Giftee\'s Name: %s" % participant["receiver"]
            })

        except Exception as e:
            return {'error': str(e)}


class Pairing(Resource):
    def get(self):
        try:
            names = []
            participants = mongo.db.participant.find()
            if participants.count() <= 2:
                return jsonify({
                    "status": "ok",
                    "message": "Before pairing add at least 3 participants"
                })
            for p in participants:
                names.append(p["name"])

            givers = list(names)
            receivers = list(names)
            while not pairing(givers, receivers):
                random.shuffle(givers)
                random.shuffle(receivers)

            mongo.db.pair.remove()
            for g, r in itertools.izip_longest(givers, receivers):
                mongo.db.pair.insert({
                    "giver": g,
                    "receiver": r
                })

        except Exception as e:
            return {'error': str(e)}

        return jsonify({"status": "ok", "message": "Pairing done!"})


api.add_resource(Participant, "/api/participant/", endpoint="participant")
api.add_resource(Pair, "/api/pair/", endpoint="pair")
api.add_resource(Pairing, "/api/pairing/", endpoint="pairing")


if __name__ == "__main__":
    app.run(debug=True)
