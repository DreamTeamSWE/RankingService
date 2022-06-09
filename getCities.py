import json

from db.RepositoryExternal import RepositoryExternal


def get_cities(event, context) -> json:
    repo_ext = RepositoryExternal()
    query_params = event['queryStringParameters']
    result = []
    if 'regione' in query_params and 'provincia' not in query_params:
        result = repo_ext.get_provinces_by_region(query_params['regione'])
    elif 'regione' in query_params and 'provincia' in query_params:
        result = repo_ext.get_cities(query_params['provincia'], query_params['regione'])

    response = {
        'statusCode': 200,
        'headers': {
            'Access-Control-Allow-Headers': 'Content-Type',
            'Access-Control-Allow-Credentials': 'true',
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'OPTIONS,POST,GET'
        },
        "body": json.dumps(result)
    }

    return response
