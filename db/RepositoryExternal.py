import boto3

from db.DatabaseHandler import DatabaseHandler


class RepositoryExternal:
    def __init__(self, db_name: str = 'ranking_test') -> None:
        self.database = DatabaseHandler(db_name)

    def __create_presigned_url(self, object_name: str, bucket_name: str = 'dream-team-img-test',
                               expiration=3600) -> str:
        """Generate a presigned URL to share an S3 object

        :param bucket_name: string
        :param object_name: string
        :param expiration: Time in seconds for the presigned URL to remain valid
        :return: Presigned URL as string. If error, returns None.
        """

        # Generate a presigned URL for the S3 object
        s3_client = boto3.client('s3', region_name='eu-central-1')
        response = \
            s3_client.generate_presigned_url('get_object',
                                             Params={'Bucket': bucket_name,
                                                     'Key': object_name},
                                             ExpiresIn=expiration)

        # The response contains the presigned URL
        return response

    def __get_count_query(self, response_count: dict, response: dict) -> dict:
        """
        return count of rows in query
        :param response_count: response of query, need to have count in select like "select count(*) as count"
        :param response: dictionary where append count
        :return: count of rows
        """

        count = response_count[0]["count"]

        # add count to response

        response.append({"count": count})

        return response

    def __iterate_over_response_ranking_restaurants(self, response: dict) -> dict:
        # iterate over response
        for r in response:
            image_name = str(r["url_image"]) + ".jpg"
            print("image_name: ", image_name)
            url_image = self.__create_presigned_url(image_name)
            print("url_image: ", url_image)
            r["url_image"] = url_image

        return response

    def get_ranking(self, position: int, size: int) -> dict:
        """
        return restaurants ranking, ordered by sum of punteggio_emoji, punteggio_foto ,punteggio_testo

        :param position: position from where to start (possible numbers start from 0)
        :param size: numbers of restaurants to return
        :return: restaurants ranking
        """

        position_param = {"name": "position", "value": {"longValue": position}}
        size_param = {"name": "size", "value": {"longValue": size}}

        print("position_param: ", position_param)
        print("size_param: ", size_param)

        query = "select " \
                "r.*, " \
                "i.id_immagine as url_image " \
                "from ristorante as r " \
                "join post p on r.id_ristorante=p.id_ristorante " \
                "join immagine i on p.id_post=i.id_post " \
                "where i.id_immagine not in (select e.id_immagine from emozione_img e) " \
                "and (r.punteggio_emoji is not null " \
                "or r.punteggio_foto is not null " \
                "or r.punteggio_testo is not null) " \
                "group by r.id_ristorante " \
                "order by (IFNULL(r.punteggio_emoji,0) + IFNULL(r.punteggio_foto,0) + IFNULL(r.punteggio_testo,0))/" \
                "(case when r.punteggio_emoji is not null then 1 else 0 end + " \
                "case when r.punteggio_foto is not null then 1 else 0 end + " \
                "case when r.punteggio_testo is not null then 1 else 0 end) desc " \
                "limit :position, :size"

        response = self.database.do_read_query(query, [position_param, size_param])
        print("query: ", query)

        query_count = "select " \
                      "count(*) as count " \
                      "from ristorante as r "

        response_count = self.database.do_read_query(query_count, [])

        response = self.__iterate_over_response_ranking_restaurants(response)

        return self.__get_count_query(response_count, response)

    def get_post_and_tag_by_restaurant(self, id_rist: int) -> dict:
        """
        return post and tag of restaurant

        :param id_rist: id of restaurant
        :return: post and tag of restaurant
        """
        # query = "select * from post p join immagine i on p.id_post = i.id_post join label_img l on " \
        #         "l.id_immagine = i.id_immagine where p.id_ristorante = :id_ristorante group by p.id_ristorante"

        query = "select * from post p where p.id_ristorante = :id_ristorante"

        print("query: ", query)

        param = [{"name": "id_ristorante", "value": {"longValue": id_rist}}]

        print("param: ", param)

        response = self.database.do_read_query(query, param)

        for r in response:
            id_post = r["id_post"]
            param = [{"name": "id_post", "value": {"stringValue": id_post}}]
            query = "select i.id_immagine from immagine i where i.id_post = :id_post"

            list_img = self.database.do_read_query(query, param)
            print("list_img: ", list_img)
            list_url_img = []
            for img in list_img:
                list_url_img.append(self.__create_presigned_url(str(img['id_immagine']) + ".jpg"))
            r["url_immagine"] = list_url_img
            r["nome_label"] = []

            for img_name in list_img:
                param = [{"name": "id_immagine", "value": {"longValue": img_name["id_immagine"]}}]
                query = "select l.nome_label from label_img l where l.id_immagine = :id_immagine"
                list_label = self.database.do_read_query(query, param)
                print("list_label: ", list_label)
                r["nome_label"].append(list_label)

        return response

    def __get_image_url_by_id_rist(self, id_rist: int) -> str:
        param = [{"name": "id_rist", "value": {"longValue": id_rist}}]
        print(param)

        query = "select immagine.id_immagine from post join ristorante on post.id_ristorante = " \
                "ristorante.id_ristorante join immagine on immagine.id_post = post.id_post where " \
                "ristorante.id_ristorante = :id_rist LIMIT 1;"

        list_img = self.database.do_read_query(query, param)
        print("list_img: ", list_img)

        image_name = str(list_img[0]["id_immagine"]) + ".jpg"
        print("image_name: ", image_name)

        return self.__create_presigned_url(image_name)

    def search_restaurants_by_name(self, name: str) -> dict:
        """
        get all restaurant which name LIKE :param name

        :param name: name to search
        :return: list of restaurants
        """
        query = "select * from ristorante where nome_ristorante like :nome_ristorante LIMIT 10;"
        param = [{"name": "nome_ristorante", "value": {"stringValue": "%" + name + "%"}}]
        response = self.database.do_read_query(query, param)
        print(response)

        if len(response) == 0:
            name_parts = name.split(" ")
            if name_parts.__sizeof__() > 0:
                query = "select * from ristorante where "
                i = 0
                param = []
                for part in name_parts:
                    query += "nome_ristorante like :nome_ristorante" + str(i) + " or "
                    param.append({"name": "nome_ristorante" + str(i), "value": {"stringValue": "%" + part + "%"}})
                    i += 1

                query = query[:-4]
                query += " limit 10;"
                print(query)
                response = self.database.do_read_query(query, param)

        for rist in response:
            rist["url_immagine"] = self.__get_image_url_by_id_rist(rist["id_ristorante"])
        # else:
        #     response[0]["url_immagine"] = self.__get_image_url_by_id_rist(response[0]["id_ristorante"])

        return response

    def get_cities(self) -> dict:
        """
        get city list
        :return: list of cities
        """
        query = "select * from citta;"
        response = self.database.do_read_query(query, [])
        return response

    def get_coordinate_by_city_name(self, city_name: str) -> dict:
        """
        return coordinate of city

        :param city_name: name of city
        :return: coordinate of city
        """
        query = "select latitudine as lat, longitudine as lng from citta where nome = :city_name"

        param = [{"name": "city_name", "value": {"stringValue": city_name}}]

        response = self.database.do_read_query(query, param)

        return response

    def filter_by_coordinate(self, lat: float, lng: float, radius: float, position: int, size: int) -> dict:
        """
        return restaurants ranking filter per coordinates and radius, ordered by sum of punteggio_emoji, punteggio_foto ,punteggio_testo

        :param lat: latitude of city
        :param lng: longitude of city
        :param radius: radius of search
        :param position: position from where to start (possible numbers start from 0)
        :param size: numbers of restaurants to return
        :return: filtered restaurants
        """

        lat_param = {"name": "lat_param", "value": {"doubleValue": lat}}
        lng_param = {"name": "lng_param", "value": {"doubleValue": lng}}
        radius_param = {"name": "radius_param", "value": {"doubleValue": radius}}

        print("lat_param: ", lat_param)
        print("lng_param: ", lng_param)
        print("radius_param: ", radius_param)

        position_param = {"name": "position", "value": {"longValue": position}}
        size_param = {"name": "size", "value": {"longValue": size}}

        print("position_param: ", position_param)
        print("size_param: ", size_param)

        query = "select " \
                "r.*, " \
                "i.id_immagine as url_image " \
                "from ristorante as r " \
                "join post p on r.id_ristorante=p.id_ristorante " \
                "join immagine i on p.id_post=i.id_post " \
                "where i.id_immagine not in (select e.id_immagine from emozione_img e) " \
                "and (r.punteggio_emoji is not null " \
                "or r.punteggio_foto is not null " \
                "or r.punteggio_testo is not null) " \
                "and ( " \
                " acos(sin(r.latitudine * 0.0175) * sin(:lat_param * 0.0175)  " \
                "      + cos(r.latitudine * 0.0175) * cos(:lat_param * 0.0175) * " \
                "        cos((:lng_param * 0.0175) - (r.longitudine * 0.0175)) " \
                "     ) * 3959 <= :radius_param " \
                ") " \
                "group by r.id_ristorante " \
                "order by (IFNULL(r.punteggio_emoji,0) + " \
                "IFNULL(r.punteggio_foto,0) + " \
                "IFNULL(r.punteggio_testo,0))/" \
                "(case when r.punteggio_emoji is not null then 1 else 0 end + " \
                "case when r.punteggio_foto is not null then 1 else 0 end + " \
                "case when r.punteggio_testo is not null then 1 else 0 end) desc " \
                "limit :position, :size"

        response = self.database.do_read_query(query,
                                               [lat_param,
                                                lng_param,
                                                radius_param,
                                                position_param,
                                                size_param])
        print("query: ", query)

        query_count = "select count(*) as count " \
                      "from ristorante as r " \
                      "join post p on r.id_ristorante=p.id_ristorante " \
                      "join immagine i on p.id_post=i.id_post " \
                      "where i.id_immagine not in (select e.id_immagine from emozione_img e) " \
                      "and (r.punteggio_emoji is not null " \
                      "or r.punteggio_foto is not null " \
                      "or r.punteggio_testo is not null) " \
                      "and ( " \
                      " acos(sin(r.latitudine * 0.0175) * sin(:lat_param * 0.0175)  " \
                      "      + cos(r.latitudine * 0.0175) * cos(:lat_param * 0.0175) * " \
                      "        cos((:lng_param * 0.0175) - (r.longitudine * 0.0175)) " \
                      "     ) * 3959 <= :radius_param " \
                      ") "

        response_count = self.database.do_read_query(query_count,
                                                     [lat_param,
                                                      lng_param,
                                                      radius_param])

        response = self.__iterate_over_response_ranking_restaurants(response)

        return self.__get_count_query(response_count, response)

    def get_label_categoria(self) -> dict:
        """
        get label cucina
        :return: list of label cucina
        """
        query = "select distinct categoria as categorie from ristorante;"
        response = self.database.do_read_query(query, [])
        return response

    def filter_categoria(self, cucina: str, position: int, size: int) -> dict:
        """
        return restaurants ranking filter per cooking type, ordered by sum of punteggio_emoji, punteggio_foto ,
        punteggio_testo

        :param cucina: type of restaurant
        :param position: position from where to start (possible numbers start from 0)
        :param size: numbers of restaurants to return
        :return: restaurant list
        """
        cucina_param = {"name": "cucina", "value": {"stringValue": cucina}}
        position_param = {"name": "position", "value": {"longValue": position}}
        size_param = {"name": "size", "value": {"longValue": size}}

        query = "select " \
                "r.*, " \
                "i.id_immagine as url_image " \
                "from ristorante as r " \
                "join post p on r.id_ristorante=p.id_ristorante " \
                "join immagine i on p.id_post=i.id_post " \
                "where i.id_immagine not in (select e.id_immagine from emozione_img e) " \
                "and (r.punteggio_emoji is not null " \
                "or r.punteggio_foto is not null " \
                "or r.punteggio_testo is not null) " \
                "and r.categoria = :cucina " \
                "group by r.id_ristorante " \
                "order by (IFNULL(r.punteggio_emoji,0) + " \
                "IFNULL(r.punteggio_foto,0) + " \
                "IFNULL(r.punteggio_testo,0))/" \
                "(case when r.punteggio_emoji is not null then 1 else 0 end + " \
                "case when r.punteggio_foto is not null then 1 else 0 end + " \
                "case when r.punteggio_testo is not null then 1 else 0 end) desc " \
                "limit :position, :size"

        response = self.database.do_read_query(query,
                                               [cucina_param,
                                                position_param,
                                                size_param])

        query_count = "select count(*) as count " \
                      "from ristorante as r " \
                      "join post p on r.id_ristorante=p.id_ristorante " \
                      "join immagine i on p.id_post=i.id_post " \
                      "where i.id_immagine not in (select e.id_immagine from emozione_img e) " \
                      "and (r.punteggio_emoji is not null " \
                      "or r.punteggio_foto is not null " \
                      "or r.punteggio_testo is not null) " \
                      "and r.categoria = :cucina "

        response_count = self.database.do_read_query(query_count, [cucina_param])

        response = self.__iterate_over_response_ranking_restaurants(response)

        return self.__get_count_query(response_count, response)
