import json

from db.RepositoryExternal import RepositoryExternal


def get_ranking(event, context):
    query_string_parameters = event['queryStringParameters']

    # check if key are presents
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

    repo_ext = RepositoryExternal()
    list_restaurant = repo_ext.get_ranking(int_position, int_size)

    response = {
        "statusCode": 200,
        "body": json.dumps(list_restaurant)
    }

    return response
