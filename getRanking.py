import json

from db.RepositoryExternal import RepositoryExternal


def get_ranking(event, context):

    int_position = 0
    int_size = 10
    if 'queryStringParameters' in event and event['queryStringParameters'] is not None:
        query_string_parameters = event['queryStringParameters']

        # check if key are presents
        if 'from' in query_string_parameters:
            position = query_string_parameters['from']
            int_position = int(position)

        if 'size' in query_string_parameters:
            size = query_string_parameters['size']
            int_size = int(size)

    repo_ext = RepositoryExternal()
    list_restaurants = repo_ext.get_ranking(int_position, int_size)



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
