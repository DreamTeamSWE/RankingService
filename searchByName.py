import json

from db.RepositoryExternal import RepositoryExternal


def search_by_name(event, context) -> json:

    body = event['body']
    body_json = json.loads(body)
    name = body_json['name']

    repo_ext = RepositoryExternal()
    list_restaurants = repo_ext.search_restaurants_by_name(name)

    response = {
        'statusCode': 200,
        'headers': {
            'Access-Control-Allow-Headers': 'Content-Type',
            'Access-Control-Allow-Credentials': 'true',
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'OPTIONS,POST,GET'
        },
        "body": json.dumps(list_restaurants)
    }

    return response
