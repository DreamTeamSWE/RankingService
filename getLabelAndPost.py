import json

from db.RepositoryExternal import RepositoryExternal


def get_label_and_post(event, context) -> json:
    repo_ext = RepositoryExternal()

    body = event['body']
    body_json = json.loads(body)
    id_rist = body_json['id_rist']

    print(type(id_rist))

    id_rist = int(id_rist)

    print("id_rist: " + str(id_rist))

    list_restaurant = repo_ext.get_post_and_tag_by_restaurant(id_rist)

    response = {
        'statusCode': 200,
        'headers': {
            'Access-Control-Allow-Headers': 'Content-Type',
            'Access-Control-Allow-Credentials': 'true',
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'OPTIONS,POST,GET'
        },
        "body": json.dumps(list_restaurant)
    }

    return response
