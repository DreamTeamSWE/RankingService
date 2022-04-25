from db.DatabaseHandler import DatabaseHandler


class RepositoryExternal:
    def __init__(self, db_name: str = 'ranking_test') -> None:
        self.database = DatabaseHandler(db_name)

    """
    - API che ritorna i tipi di cucina data una ricerca
    - API che ritorna le zone
    - API che ritorna dei locali alternativi, nel caso non ci fosse un risultato “perfetto”
    - API per la gestione dei preferiti, nel caso l’utente sia loggato
    """

    def get_ranking(self, position: int, size: int):
        """
        return restaurants ranking, ordered by sum of punteggio_emoji, punteggio_foto ,punteggio_testo

        :param position: position from where to start (possible numbers start from 0)
        :param size: numbers of restaurants to return
        :return: restaurants ranking
        """

        position_param = {"name": "position", "value": {"longValue": position}}
        size_param = {"name": "size", "value": {"longValue": size}}

        query = "SELECT * FROM ristorante ORDER BY (punteggio_emoji+punteggio_foto+punteggio_testo) DESC LIMIT " \
                ":position, :size"
        response = self.database.do_read_query(query, [position_param, size_param])

        return response

    def get_post_and_tag_by_restaurant(self, id_rist: int):
        """
        return post and tag of restaurant

        :param id_rist: id of restaurant
        :return: post and tag of restaurant
        """
        query = "select * from post p join immagine i on p.id_post = i.id_post join label_img l on l.id_immagine = " \
                "i.id_immagine where p.id_ristorante = :id_ristorante group by p.id_ristorante"

        param = [{"name": "id_ristorante", "value": {"longValue": id_rist}}]

        return self.database.do_read_query(query, param)

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
