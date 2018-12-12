from flask import request, jsonify, Request
from google.cloud import datastore
import re
import sys
import os

client = datastore.Client()


def get_heroes():
    query = client.query(kind='Hero')
    return list(query.fetch()), 200


def post_hero(hero: dict):
    key = client.key('Hero', hero['id'])
    hero_entity = datastore.Entity(key)
    hero_entity.update(hero)
    client.put(hero_entity)
    return hero_entity, 200


def update_hero(hero: dict):
    key = client.key('Hero', hero['id'])
    hero_entity = datastore.Entity(key)
    hero_entity.update(hero)
    client.put(hero_entity)
    return hero_entity, 200


def delete_hero_by_id(id):
    key = client.key('Hero', id)
    client.delete(key)
    return '', 200


def get_hero_by_id(id):
    key = client.key('Hero', id)
    hero = client.get(key)
    if hero:
        return hero, 200
    else:
        return '', 404


def heroes_by_name(name):
    query = client.query(kind='Hero')
    return list(query.fetch()), 200


def hero_service(request: Request):
    try:
        global heroes

        if request.method == 'OPTIONS':
            headers = {
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Methods': '*',
                'Access-Control-Allow-Headers': 'Content-Type',
                'Access-Control-Max-Age': '3600'
            }
            return ('', 204, headers)

        # Set CORS headers for the main request
        headers = {
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': '*'
        }

        # handle path params
        hero_by_id_regex = re.compile('/api/heroes/([\d]+)')
        heroes_by_name_regex = re.compile('/api/search/([a-zA-Z0-9]+)')
        path = request.path
        http_method = request.method
        hero_by_id_match = hero_by_id_regex.match(path)
        heroes_by_name_match = heroes_by_name_regex.match(path)

        # handlers
        if path == '/api/heroes' and http_method == "GET":
            data, status_code = get_heroes()
            return jsonify(data), status_code, headers
        if path == '/api/heroes' and http_method == "POST":
            data, status_code = post_hero(request.json)
            return jsonify(data), status_code, headers
        if path == '/api/heroes' and http_method == "PUT":
            data, status_code = update_hero(request.json)
            return jsonify(data), status_code, headers
        if hero_by_id_match and http_method == "GET":
            id = hero_by_id_match.group(1)
            data, status_code = get_hero_by_id(id)
            return jsonify(data), status_code, headers
        if hero_by_id_match and http_method == "DELETE":
            id = hero_by_id_match.group(1)
            data, status_code = delete_hero_by_id(id)
            return jsonify(data), status_code, headers
        if heroes_by_name_match and http_method == "GET":
            name = heroes_by_name_match.group(1)
            data, status_code = heroes_by_name(name)
            return jsonify(data), status_code, headers

        else:
            return jsonify({'error': f'could not find handler for {http_method} -> {path}'}), 400, headers

    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        headers = {
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': '*'
        }
        payload = jsonify({
            'error': str(e),
            'type': str(exc_type),
            'file_name': str(fname),
            'line_number': str(exc_tb.tb_lineno)
        })
        return payload, 500, headers
