import json

from analyzer.PostAnalyzer import PostAnalyzer
from entity.CrawledData import CrawledData
from db.RepositoryInternal import RepositoryInternal


def refresh_ranking(event, context):
    array_json_sqs_response = event['Records']

    repository = RepositoryInternal()
    analyzer = PostAnalyzer()

    for item in array_json_sqs_response:
        item_body = item['body']
        post = CrawledData.parse_post_from_sqs(item_body)

        print("check if post " + post.id_post + " is already in db")

        if not repository.check_if_post_already_exist(id_post=post.id_post):
            print("Post " + post.id_post + " not present")
            print(post)
            analyzer.analyze(post)
        else:
            print("Post " + post.id_post + " already exist")

    response = {
        "statusCode": 200,
        "body": "Done!"
    }

    return response


def favorites_handler(event, context):
    response = {
        "statusCode": 200,
        "body": json.dumps("test")
    }

    return response
