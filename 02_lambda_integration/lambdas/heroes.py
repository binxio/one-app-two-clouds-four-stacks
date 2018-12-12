import boto3
import json
import re
import sys
import os

client = boto3.client('dynamodb')


def response(body: any) -> dict:
    return {
        'statusCode': 200,
        'headers': {
            'Access-Control-Allow-Headers': 'Content-Type,X-Amz-Date,Authorization,X-Api-Key',
            'Access-Control-Allow-Methods': '*',
            'Access-Control-Allow-Origin': '*',
        },
        'body': json.dumps(body)
    }


def get_heroes():
    """Get a hero"""
    xs = []
    items = client.scan(TableName="heroes")['Items']
    for item in items:
        id = item['id']['S']
        name = item['name']['S']
        xs.append({'id': str(id), 'name': str(name)})
    return xs


def post_hero(body: dict) -> dict:
    """Add a hero"""
    item = {
        'id': {
            'S': body['id']
        },
        'name': {
            'S': body['name']
        }
    }
    client.put_item(TableName="heroes", Item=item)
    return {}


def update_hero(body: dict) -> dict:
    """Update a hero"""
    client.update_item(
        TableName="heroes",
        Key={
            "id": {
                "S": body['id']
            },
        },
        UpdateExpression="SET #n = :p",
        ExpressionAttributeValues={
            ":p": {"S": body['name']}
        },
        ExpressionAttributeNames={"#n": "name"}
    )
    return {}


def get_hero_by_id(id) -> dict:
    """Get hero by id"""
    res = client.get_item(
        TableName="heroes",
        Key={
            'id': {
                'S': str(id)
            }

        }).get('Item')

    if res:
        return {
            'id': res['id']['S'],
            'name': res['name']['S']
        }
    else:
        return {}


def delete_hero_by_id(id: str) -> dict:
    """Delete hero by id"""
    client.delete_item(
        TableName="heroes",
        Key={
            'id': {
                'S': id
            }

        })
    return {}


def heroes_by_name(name: str):
    """Get heroes by name"""
    xs = []
    items = client.scan(
        TableName="heroes",
        ScanFilter={
            'name': {
                'AttributeValueList': [{'S': name}],
                'ComparisonOperator': 'CONTAINS'
            }
        })['Items']

    for item in items:
        id = item['id']['S']
        name = item['name']['S']
        xs.append({'id': str(id), 'name': str(name)})
    return xs


def handler(event, ctx):
    try:
        print(json.dumps(event))

        # handle path params
        hero_by_id_regex = re.compile('/api/heroes/([\d]+)')
        heroes_by_name_regex = re.compile('/api/search/([a-zA-Z0-9]+)')
        path = event['path']
        http_method = event['httpMethod']
        hero_by_id_match = hero_by_id_regex.match(path)
        heroes_by_name_match = heroes_by_name_regex.match(path)

        # handlers
        if path == '/api/heroes' and http_method == "GET":
            return response(get_heroes())
        if path == '/api/heroes' and http_method == "POST":
            return response(post_hero(json.loads(event['body'])))
        if path == '/api/heroes' and http_method == "PUT":
            return response(update_hero(json.loads(event['body'])))
        if hero_by_id_match and http_method == "GET":
            id = hero_by_id_match.group(1)
            return response(get_hero_by_id(id))
        if hero_by_id_match and http_method == "DELETE":
            id = hero_by_id_match.group(1)
            return response(delete_hero_by_id(id))
        if heroes_by_name_match and http_method == "GET":
            name = heroes_by_name_match.group(1)
            return response(heroes_by_name(name))

        else:
            return response({'error': f'could not find handler for {http_method} -> {path}'})
    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        return response({
            'error': str(e),
            'type': str(exc_type),
            'file_name': str(fname),
            'line_number': str(exc_tb.tb_lineno)
        })
