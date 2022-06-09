import json

from db.RepositoryExternal import RepositoryExternal


def filter_handler(event, context) -> json:
    query_string_parameters = event['queryStringParameters']

    list_restaurants = None
    int_radius_miles = 10 / 1.60934
    int_position = 0
    int_size = 10

    repo_ext = RepositoryExternal()

    if 'from' in query_string_parameters:
        position = query_string_parameters['from']
        int_position = int(position)

    if 'size' in query_string_parameters:
        size = query_string_parameters['size']
        int_size = int(size)

    if 'location' in query_string_parameters and 'categoria' in query_string_parameters:
        # filter by location and category
        location = query_string_parameters['location']
        category = query_string_parameters['categoria']
        if 'radius' in query_string_parameters:
            radius = query_string_parameters['radius']
            int_radius_km = int(radius)
            int_radius_miles = int_radius_km / 1.60934

        city_coordinate = repo_ext.get_coordinate_by_city_name(location)

        lat = float(city_coordinate[0]['lat'])
        lng = float(city_coordinate[0]['lng'])

        list_restaurants = \
            repo_ext.multi_filter(lat, lng, int_radius_miles, category, int_position, int_size)

    elif 'location' in query_string_parameters:
        # filter by location only
        location = query_string_parameters['location']
        if 'radius' in query_string_parameters:
            radius = query_string_parameters['radius']
            int_radius_km = int(radius)
            int_radius_miles = int_radius_km / 1.60934

        city_coordinate = repo_ext.get_coordinate_by_city_name(location)

        lat = float(city_coordinate[0]['lat'])
        lng = float(city_coordinate[0]['lng'])

        list_restaurants = \
            repo_ext.filter_by_coordinate(lat, lng, int_radius_miles, int_position, int_size)

    elif 'categoria' in query_string_parameters:
        # filter by category only
        category = query_string_parameters['categoria']
        list_restaurants = \
            repo_ext.filter_by_category(category, int_position, int_size)

    if list_restaurants is not None:
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
            'body': json.dumps('Error, usage: ?location=city&categoria=category or ?location=city or '
                               '?categoria=category, radius=km (optional) only if location is present')
        }

    return response
