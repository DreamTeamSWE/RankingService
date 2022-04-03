import json
from entity.CrawledData import CrawledData
from entity.Restaurant import Restaurant


def refresh_ranking(event, context):
    array_json_sqs_response = event['Records']

    list_post = []

    for item in array_json_sqs_response:
        print(item['body'])
        item_body = item['body']
        restaurant = Restaurant(
            id_rist=item_body['db_id'],
            nome=item_body['location_name'],
            # indirizzo=item_body['address'],
            indirizzo="",
            telefono=item_body['phone'],
            sito=item_body['website'],
            lat=item_body['lat'],
            lng=item_body['lng'],
            categoria=item_body['category'])

        list_img = []
        for img in item_body['img_url']:
            list_img.append(img)

        post = CrawledData(
            id_post=item_body['post_id'],
            utente=item_body['username'],
            caption=item_body['caption_text'],
            list_image=list_img,
            restaurant=restaurant)

        print('--------------------\n')

        print(post)
        list_post.append(post)

        print('--------------------\n')

    body = {
        "message": "Go Serverless v1.0! Your function executed successfully!",
        "input": "Ciaone"
    }

    response = {
        "statusCode": 200,
        "body": json.dumps(body)
    }

    return response
