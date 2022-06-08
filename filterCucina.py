import json

from db.RepositoryExternal import RepositoryExternal


def filter_cucina(event, context) -> json:
    if 'queryStringParameters' in event and event['queryStringParameters'] is not None \
            and 'cucina' in event['queryStringParameters']:
        query_string_parameters = event['queryStringParameters']

        cucina = query_string_parameters['cucina']

        print("filter_cucina: " + cucina)

        if 'from' in query_string_parameters:
            position = query_string_parameters['from']
            int_position = int(position)
        else:
            int_position = 0

        if 'size' in query_string_parameters:
            size = query_string_parameters['size']
            int_size = int(size)
        else:
            int_size = 10

        print("filter_cucina: " + str(int_position) + " " + str(int_size))

        repo_ext = RepositoryExternal()

        list_restaurants = \
            repo_ext.filter_by_cucina(cucina,
                                      int_position,
                                      int_size)

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
    else:
        response = {
            'statusCode': 400,
            'headers': {
                'Access-Control-Allow-Headers': 'Content-Type',
                'Access-Control-Allow-Credentials': 'true',
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Methods': 'OPTIONS,POST,GET'
            },
            'body': json.dumps('cucina is missing')
        }

    return response
