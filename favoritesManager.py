import json
from db.RepositoryFavorites import RepositoryFavorites


def favorites_handler(event, context):
    username = event['queryStringParameters']['user']
    action = event['queryStringParameters']['action']
    result = ''

    fav = RepositoryFavorites()
    if action == 'get':
        result = fav.get_favorites(username)
    elif action == 'remove':
        id_rest = int(event['queryStringParameters']['restaurant'])
        result = fav.remove_favorite(username, id_rest)
    elif action == 'add':
        id_rest = int(event['queryStringParameters']['restaurant'])
        result = fav.add_favorite(username, id_rest)

    response = {
        "statusCode": 200,

        "headers": {
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Credentials": True
        },

        "body": json.dumps(result)

    }

    return response
