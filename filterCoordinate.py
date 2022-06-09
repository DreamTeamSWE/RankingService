import json

from db.RepositoryExternal import RepositoryExternal


def filter_coordinate(event, context) -> json:
    if 'queryStringParameters' in event and event['queryStringParameters'] is not None \
            and 'comune' in event['queryStringParameters'] \
            and 'provincia' in event['queryStringParameters'] \
            and 'regione' in event['queryStringParameters']:
        query_string_parameters = event['queryStringParameters']

        city = query_string_parameters['comune']
        province = query_string_parameters['provincia']
        region = query_string_parameters['regione']

        if 'radius' in query_string_parameters:
            radius = query_string_parameters['radius']
            int_radius_km = int(radius)
            int_radius_miles = int_radius_km / 1.60934
        else:
            int_radius_miles = 10

        print("filter_coordinate: " + city + " " + region + " " + str(int_radius_miles))

        query_string_parameters = event['queryStringParameters']
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

        print("filter_coordinate: " + str(int_position) + " " + str(int_size))

        repo_ext = RepositoryExternal()
        city_coordinate = repo_ext.get_coordinate_by_city_name(city, province, region)

        lat = float(city_coordinate[0]['lat'])
        lng = float(city_coordinate[0]['lng'])

        print("get_ranking: " + str(lat) + " " + str(lng))

        list_restaurants = \
            repo_ext.filter_by_coordinate(lat,
                                          lng,
                                          int_radius_miles,
                                          int_position,
                                          int_size)

        response = {
            'statusCode': 200,
            'headers': {
                'Access-Control-Allow-Headers': 'Content-Type',
                'Access-Control-Allow-Credentials': 'true',
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Methods': 'OPTIONS,POST,GET'
            },
            "body": json.dumps(list_restaurants)
        }

    else:
        response = {
            'statusCode': 400,
            'headers': {
                'Access-Control-Allow-Headers': 'Content-Type',
                'Access-Control-Allow-Credentials': 'true',
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Methods': 'OPTIONS,POST,GET'
            },
            'body': json.dumps('location is missing')
        }

    return response
