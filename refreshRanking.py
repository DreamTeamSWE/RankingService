import json

from analyzer.PostAnalyzer import PostAnalyzer
from entity.CrawledData import CrawledData
from db.RepositoryInternal import RepositoryInternal


def refresh_ranking(event, context) -> json:
    array_json_sqs_response = event['Records']

    repository = RepositoryInternal()
    analyzer = PostAnalyzer()

    for item in array_json_sqs_response:
        item_body = json.loads(item['body'])
        # item_body = item['body']
        post = CrawledData.parse_post_from_sqs(item_body)

        print("check if post " + post.get_id_post() + " is already in db")

        if not repository.check_if_post_already_exist(id_post=post.get_id_post()):
            print("Post " + post.get_id_post() + " not present")
            print(post)
            analyzer.analyze(post)
        else:
            print("Post " + post.get_id_post() + " already exist")

    response = {
        "statusCode": 200,
        "body": "Done!"
    }

    return response
