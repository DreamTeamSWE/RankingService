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

        query = "select r.*,i.id_immagine as url_image from ristorante as r " \
                "join post p on r.id_ristorante=p.id_ristorante " \
                "join immagine i on p.id_post=i.id_post " \
                "where i.id_immagine not in (select e.id_immagine from emozione_img e) " \
                "group by r.id_ristorante " \
                "order by (r.punteggio_emoji+r.punteggio_foto+r.punteggio_testo) desc " \
                "limit :position, :size"

        response = self.database.do_read_query(query, [position_param, size_param])
        print("query: ", query)

        # iterate over response
        for r in response:
            image_name = str(r["url_image"]) + ".jpg"
            print("image_name: ", image_name)
            url_image = self.__create_presigned_url(image_name)
            print("url_image: ", url_image)
            r["url_image"] = url_image

        return response

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

    def search_restaurants_by_name(self, name: str) -> dict:
        """
        get all restaurant which name LIKE :param name

        :param name: name to search
        :return: list of restaurants
        """
        query = "SELECT * FROM ristorante WHERE nome_ristorante LIKE :nome_ristorante"
        param = [{"name": "nome_ristorante", "value": {"stringValue": "%" + name + "%"}}]
        response = self.database.do_read_query(query, param)
        print(response)

        if len(response) == 0:
            name_parts = name.split(" ")
            if name_parts.__sizeof__() > 0:
                query = "SELECT * FROM ristorante WHERE "
                i = 0
                param = []
                for part in name_parts:
                    query += "nome_ristorante LIKE :nome_ristorante" + str(i) + " OR "
                    param.append({"name": "nome_ristorante" + str(i), "value": {"stringValue": "%" + part + "%"}})
                    i += 1

                query = query[:-4]
                print(query)
                response = self.database.do_read_query(query, param)

        return response
