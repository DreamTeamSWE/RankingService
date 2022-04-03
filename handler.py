import json
from entity.CrawledData import CrawledData
from entity.Restaurant import Restaurant
from analyzer.PostAnalyzer import PostAnalyzer


def refresh_ranking(event, context):
    array_json_sqs_response = event['Records']

    for item in array_json_sqs_response:
        # print(item['body'])
        item_body = item['body']

        restaurant_body = item_body['location']
        restaurant = Restaurant(
            id_rist=restaurant_body['db_id'],
            nome=restaurant_body['location_name'],
            # indirizzo=item_body['address'],
            indirizzo="",
            telefono=restaurant_body['phone'],
            sito=restaurant_body['website'],
            lat=restaurant_body['lat'],
            lng=restaurant_body['lng'],
            categoria=restaurant_body['category'])

        list_img = []
        for img in item_body['img_url']:
            list_img.append(img)

        post = CrawledData(
            id_post=item_body['post_id'],
            utente=item_body['username'],
            caption=item_body['caption_text'],
            list_image=list_img,
            restaurant=restaurant)

        # print('--------------------\n')

        # print(post)

        # print('--------------------\n')

        analyzer = PostAnalyzer()
        analyzer.analyze(post)

    body = {
        "message": "Go Serverless v1.0! Your function executed successfully!",
        "input": "Ciaone"
    }

    response = {
        "statusCode": 200,
        "body": json.dumps(body)
    }

    return response
