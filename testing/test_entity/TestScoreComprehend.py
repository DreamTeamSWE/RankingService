import unittest

from entity.ScoreComprehend import ScoreComprehend, Sentiment


class TestScoreComprehend(unittest.TestCase):
    def setUp(self):
        self.__pos = 80
        self.__neg = 10
        self.__mix = 5
        self.__neu = 5
        self.score_comprehend = ScoreComprehend(positive=self.__pos, negative=self.__neg,
                                                mixed=self.__mix, neutral=self.__neu)

    def test_set_sentiment(self):
        self.score_comprehend.set_sentiment("positive")
        self.assertEqual(Sentiment.POSITIVE, self.score_comprehend._ScoreComprehend__principal_sentiment)
        self.score_comprehend.set_sentiment("negative")
        self.assertEqual(Sentiment.NEGATIVE, self.score_comprehend._ScoreComprehend__principal_sentiment)
        self.score_comprehend.set_sentiment("mixed")
        self.assertEqual(Sentiment.MIXED, self.score_comprehend._ScoreComprehend__principal_sentiment)
        self.score_comprehend.set_sentiment("neutral")
        self.assertEqual(Sentiment.NEUTRAL, self.score_comprehend._ScoreComprehend__principal_sentiment)

    def test_calculate_score(self):
        self.assertEqual(82.0, self.score_comprehend.calculate_score())

    def test_set_param_for_query(self):
        id_post = 1
        expected = [
            {"name": "id_post", "value": {"stringValue": id_post}},
            {"name": "negative", "value": {"longValue": self.__neg}},
            {"name": "positive", "value": {"longValue": self.__pos}},
            {"name": "neutral", "value": {"longValue": self.__neu}},
            {"name": "mixed", "value": {"longValue": self.__mix}}
        ]

        self.assertEqual(expected, self.score_comprehend.set_param_for_query(id_post))


if __name__ == '__main__':
    unittest.main()
