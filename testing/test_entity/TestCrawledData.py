import json
import unittest
from unittest.mock import patch

from entity.CrawledData import CrawledData
from entity.Image import Image
from entity.Restaurant import Restaurant


class TestCrawledData(unittest.TestCase):
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

        self.crawled_data = CrawledData(
            id_post="123",
            author="author",
            date_post="2019-01-01",
            caption="caption",
            restaurant=self.restaurant,
            list_images=[Image("1")]
        )

    def test_get_id_post(self):
        self.assertEqual("123", self.crawled_data.get_id_post())

    def test_get_author(self):
        self.assertEqual("author", self.crawled_data.get_author())

    def test_get_date_post(self):
        self.assertEqual("2019-01-01", self.crawled_data.get_date_post())

    def test_get_caption(self):
        self.assertEqual("caption", self.crawled_data.get_caption())

    def test_get_list_images(self):
        result = self.crawled_data.get_list_images()
        result = [image.get_image_name() for image in result]
        self.assertEqual([Image("1").get_image_name()], result)

    def test_set_param_for_query(self):
        expected = [
            {"name": "id_post", "value": {"stringValue": "123"}},
            {"name": "post_utente", "value": {"stringValue": "author"}},
            {"name": "data_post", "value": {"stringValue": "2019-01-01"}, "typeHint": "DATE"},
            {"name": "id_ristorante", "value": {"longValue": 1}},
            {"name": "testo", "value": {"stringValue": "caption"}},
            {"name": "punteggio_emoji", "value": {"doubleValue": None}},
            {"name": "punteggio_testo", "value": {"doubleValue": None}},
            {"name": "punteggio_foto", "value": {"doubleValue": None}},
        ]
        self.assertEqual(expected, self.crawled_data.set_param_for_query())

    def test_parse_post_from_sqs(self):
        with patch("entity.Restaurant.Restaurant.parse_restaurant_from_sqs") as mock_rest:
            mock_rest.return_value = None
            sqs_message = json.loads(
                '{"username": "trekelvin", "post_id": "2804645955154227206_25025264", "date": "2022-03-29 ' \
                '13:17:53", "caption_text": "blablabla", "location": null, "s3_id": []} '
            )

            expected = CrawledData(
                id_post="2804645955154227206_25025264",
                author="trekelvin",
                date_post="2022-03-29",
                caption="blablabla",
                restaurant=None,
                list_images=[]
            )

            self.assertEqual(expected.__dict__, self.crawled_data.parse_post_from_sqs(sqs_message).__dict__)

    def test_calculate_and_set_image_score(self):
        with patch("entity.Image.Image.calculate_score") as mock_image_score:
            mock_image_score.return_value = 0.5
            self.crawled_data.calculate_and_set_image_score()
            self.assertEqual(0.5, self.crawled_data._CrawledData__image_score)

if __name__ == '__main__':
    unittest.main()
