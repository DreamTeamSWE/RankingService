import json

from db.RepositoryExternal import RepositoryExternal


def get_label_categoria(event, context) -> json:
    repo_ext = RepositoryExternal()
    list_label_categoria = repo_ext.get_label_categoria()

    response = {
        'statusCode': 200,
        'headers': {
            'Access-Control-Allow-Headers': 'Content-Type',
            'Access-Control-Allow-Credentials': 'true',
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'OPTIONS,POST,GET'
        },
        "body": json.dumps(list_label_categoria)
    }

    return response
