import json

from analyzer.PostAnalyzer import PostAnalyzer
from entity.CrawledData import CrawledData
from db.RepositoryInternal import RepositoryInternal


def refresh_ranking(event, context):
    array_json_sqs_response = event['Records']

    repository = RepositoryInternal()
    analyzer = PostAnalyzer()

    for item in array_json_sqs_response:
        item_body = json.loads(item['body'])

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


# ev = {"username": "diariodibrodo", "post_id": "92759706439750529492_2059697415", "date": "2022-01-26",
#       "img_url": [84, 85, 86, 87, 88, 89],
#       "caption_text": "Oh Crispa! Un pezzo di Cina a Torino #brodo #hot #xiaolongbao #bao #chinesefood #torino #sansalvario",
#       "location": {"location_name": "Oh Crispa", "lat": 45.058, "lng": 7.6798, "category": "Chinese Restaurant",
#                    "phone": "+393715854863", "website": "", "db_id": 73}}
# if __name__ == "__main__":
#     refresh_ranking(ev, None)
