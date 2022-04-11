from analyzer.PostAnalyzer import PostAnalyzer
from entity.CrawledData import CrawledData
from entity.Image import Image
from entity.Restaurant import Restaurant


def refresh_ranking(event, context):
    array_json_sqs_response = event['Records']

    for item in array_json_sqs_response:
        item_body = item['body']
        restaurant_body = item_body['location']

        restaurant = Restaurant(
            id_rist=restaurant_body['db_id'],
            nome=restaurant_body['location_name'],
            indirizzo="",  # indirizzo=item_body['address'],
            telefono=restaurant_body['phone'],
            sito=restaurant_body['website'],
            lat=restaurant_body['lat'],
            lng=restaurant_body['lng'],
            categoria=restaurant_body['category'])

        list_img = []
        for img in item_body['img_url']:
            list_img.append(Image(img))

        post = CrawledData(
            id_post=item_body['post_id'],
            utente=item_body['username'],
            caption=item_body['caption_text'],
            list_images=list_img,
            restaurant=restaurant)

        analyzer = PostAnalyzer()
        analyzer.analyze(post)

    response = {
        "statusCode": 200,
        "body": "Done!"
    }

    return response
