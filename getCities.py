import json

from db.RepositoryExternal import RepositoryExternal


def get_cities(event, context) -> json:
    repo_ext = RepositoryExternal()
    list_cities = repo_ext.get_cities()

    response = {
        'statusCode': 200,
        'headers': {
            'Access-Control-Allow-Headers': 'Content-Type',
            'Access-Control-Allow-Credentials': 'true',
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'OPTIONS,POST,GET'
        },
        "body": json.dumps(list_cities)
    }

    return response
