import json
import unittest

from entity.Restaurant import Restaurant


class TestRestaurant(unittest.TestCase):

    def setUp(self):
        self.restaurant = Restaurant(
            id_rist=1,
            nome="Ristorante",
            indirizzo="indirizzo",
            telefono="0002220000",
            sito="www.riso.it",
            lat=1.001,
            lng=2.002,
            categoria="italiano",
        )
        self.restaurant.set_emoji_score(1.0)
        self.restaurant.set_image_score(2.0)
        self.restaurant.set_text_score(3.0)

    def test_get_id(self):
        self.assertEqual(1, self.restaurant.get_id())

    def test_get_name(self):
        self.assertEqual("Ristorante", self.restaurant.get_name())

    def test_get_address(self):
        self.assertEqual("indirizzo", self.restaurant.get_address())

    def test_get_phone(self):
        self.assertEqual("0002220000", self.restaurant.get_phone())

    def test_get_website(self):
        self.assertEqual("www.riso.it", self.restaurant.get_website())

    def test_get_lat(self):
        self.assertEqual(1.001, self.restaurant.get_lat())

    def test_get_lng(self):
        self.assertEqual(2.002, self.restaurant.get_lng())

    def test_get_category(self):
        self.assertEqual("italiano", self.restaurant.get_category())

    def test_set_param_for_query(self):
        expected = [
            {"name": "id_ristorante", "value": {"longValue": 1}},
            {"name": "nome_ristorante", "value": {"stringValue": "Ristorante"}},
            {"name": "indirizzo", "value": {"stringValue": "indirizzo"}},
            {"name": "telefono", "value": {"stringValue": "0002220000"}},
            {"name": "sito_web", "value": {"stringValue": "www.riso.it"}},
            {"name": "latitudine", "value": {"doubleValue": 1.001}},
            {"name": "longitudine", "value": {"doubleValue": 2.002}},
            {"name": "categoria", "value": {"stringValue": "italiano"}},
            {"name": "punteggio_emoji", "value": {"doubleValue": 1.0}},
            {"name": "punteggio_foto", "value": {"doubleValue": 2.0}},
            {"name": "punteggio_testo", "value": {"doubleValue": 3.0}}
        ]

        self.assertEqual(expected,
                         self.restaurant.set_param_for_query())

    def test_parse_restaurant_from_sqs(self):
        sqs_message = json.loads(
            '{"username": "trekelvin", "post_id": "2804645955154227206_25025264", "date": "2022-03-29 ' \
            '13:17:53", "caption_text": "blablabla", "location": {"location_name": "180g Pizzeria Romana", ' \
            '"lat": 41.8912, "lng": 12.5528, "category": "Pizza place", "phone": "+393479998983", ' \
            '"website": "http://www.180gpizzeriaromana.com", "db_id": 204}, "s3_id": [7150]} '
        )

        expected = self.restaurant = Restaurant(
            id_rist=204,
            nome="180g Pizzeria Romana",
            indirizzo="",
            telefono="+393479998983",
            sito="http://www.180gpizzeriaromana.com",
            lat=41.8912,
            lng=12.5528,
            categoria="Pizza place"
        )

        self.assertEqual(expected.__dict__, Restaurant.parse_restaurant_from_sqs(sqs_message).__dict__)

    def test_get_emoji_score(self):
        self.assertEqual(1.0, self.restaurant.get_emoji_score())

    def test_get_image_score(self):
        self.assertEqual(2.0, self.restaurant.get_image_score())

    def test_get_text_score(self):
        self.assertEqual(3.0, self.restaurant.get_text_score())


if __name__ == '__main__':
    unittest.main()
