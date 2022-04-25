import json

from db.RepositoryExternal import RepositoryExternal


def search_by_name(event, context):
    name = event['queryStringParameters']['name']

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
