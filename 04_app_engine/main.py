# [START gae_python37_app]
from flask import Flask, jsonify, request
from flask_cors import CORS, cross_origin
from google.cloud import datastore

app = Flask(__name__)
CORS(app)

client = datastore.Client()


@app.route('/api/heroes', methods=['GET'])
@cross_origin()
def get_heroes():
    query = client.query(kind='Hero')
    return jsonify(list(query.fetch())), 200


@app.route('/api/heroes', methods=['POST'])
@cross_origin()
def post_hero():
    hero = request.json
    key = client.key('Hero', hero['id'])
    hero_entity = datastore.Entity(key)
    hero_entity.update(hero)
    client.put(hero_entity)
    return jsonify(hero_entity), 200


@app.route('/api/heroes', methods=['PUT'])
@cross_origin()
def update_hero():
    hero = request.json
    key = client.key('Hero', hero['id'])
    hero_entity = datastore.Entity(key)
    hero_entity.update(hero)
    client.put(hero_entity)
    return jsonify(hero_entity), 200


@app.route('/api/heroes/<id>', methods=['DELETE'])
@cross_origin()
def delete_hero_by_id(id):
    key = client.key('Hero', id)
    client.delete(key)
    return '', 200


@app.route('/api/heroes/<id>', methods=['GET'])
@cross_origin()
def get_hero_by_id(id):
    key = client.key('Hero', id)
    hero = client.get(key)
    if hero:
        return jsonify(hero), 200
    else:
        return jsonify(), 404


@app.route('/api/search/<name>', methods=['GET'])
@cross_origin()
def search_heroes_by_name(name):
    query = client.query(kind='Hero')
    return jsonify(list(query.fetch())), 200


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080, debug=True)
# [END gae_python37_app]
