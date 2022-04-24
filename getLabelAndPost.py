import json

from db.RepositoryExternal import RepositoryExternal


def get_label_and_post(event, context):
    repo_ext = RepositoryExternal()

    body = event['body']
    body_json = json.loads(body)
    id_rist = int(body_json['id_rist'])

    list_restaurant = repo_ext.get_post_and_tag_by_restaurant(id_rist)

    response = {
        "statusCode": 200,
        "body": json.dumps(list_restaurant)
    }

    return response
