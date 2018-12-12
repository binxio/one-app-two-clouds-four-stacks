# [START gae_python37_app]
from flask import Flask, jsonify, request
from flask_cors import CORS, cross_origin

app = Flask(__name__)
CORS(app)

heroes = [
    {
        'id': "1",
        'name': 'superman'
    },
    {
        'id': "2",
        'name': 'batman'
    },
    {
        'id': "3",
        'name': 'spiderman'
    },
    {
        'id': "4",
        'name': 'ironman'
    }
]


@app.route('/api/heroes', methods=['GET'])
@cross_origin()
def get_heroes():
    global heroes
    return jsonify(heroes), 200


@app.route('/api/heroes', methods=['POST'])
@cross_origin()
def post_hero():
    global heroes
    hero = request.json
    heroes.append(hero)
    return jsonify(hero), 200


@app.route('/api/heroes', methods=['PUT'])
@cross_origin()
def update_hero():
    global heroes
    hero = request.json
    heroes.append(hero)
    return jsonify(hero), 200


@app.route('/api/heroes/<id>', methods=['DELETE'])
@cross_origin()
def delete_hero_by_id(id):
    xs = []
    global heroes
    for hero in heroes:
        if hero['id'] != id:
            xs.append(hero)
    heroes = xs
    return jsonify(heroes), 200


@app.route('/api/heroes/<id>', methods=['GET'])
@cross_origin()
def get_hero_by_id(id):
    global heroes
    for hero in heroes:
        if hero['id'] == id:
            return jsonify(hero), 200
    return jsonify({}), 404


@app.route('/api/search/<name>', methods=['GET'])
@cross_origin()
def search_heroes_by_name(name):
    global heroes
    xs = []
    for hero in heroes:
        if hero['name'].contains(name):
            xs.append(hero)
    return jsonify(xs), 200


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080, debug=True)
# [END gae_python37_app]
