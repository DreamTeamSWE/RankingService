import json

from db.RepositoryExternal import RepositoryExternal


def filter_coordinate(event, context) -> json:
    location = ''
    int_radius_miles = 10

    int_position = 0
    int_size = 10

    if 'queryStringParameters' in event and event['queryStringParameters'] is not None:
        query_string_parameters = event['queryStringParameters']

        # check if key are presents
        if 'location' in query_string_parameters:
            location = query_string_parameters['location']

        if 'radius' in query_string_parameters:
            radius = query_string_parameters['radius']
            int_radius_km = int(radius)
            int_radius_miles = int_radius_km / 1.60934

    print("filter_coordinate: " + location + " " + str(int_radius_miles))

    if location == '':
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
    else:
        query_string_parameters = event['queryStringParameters']
        if 'from' in query_string_parameters:
            position = query_string_parameters['from']
            int_position = int(position)

        if 'size' in query_string_parameters:
            size = query_string_parameters['size']
            int_size = int(size)

        print("get_ranking: " + str(int_position) + " " + str(int_size))

        repo_ext = RepositoryExternal()
        city_coordinate = repo_ext.get_coordinate_by_city_name(location)

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

    return response
