import io
import json
import unittest
from unittest.mock import patch

from botocore import stub
from botocore.response import StreamingBody

from analyzer.PostAnalyzer import PostAnalyzer

import botocore.session
from botocore.stub import Stubber

from entity.CrawledData import CrawledData
from entity.ScoreComprehend import ScoreComprehend


class TestPostAnalyzer(unittest.TestCase):
    def setUp(self):
        # self.reko = botocore.session.get_session().create_client('rekognition')
        # self.comp = botocore.session.get_session().create_client('comprehend')
        # self.s3 = botocore.session.get_session().create_client('s3')
        # with Stubber(self.reko) as rekogntion_stubber, \
        #         Stubber(self.comp) as comprehend_stubber, \
        #         Stubber(self.s3) as s3_stubber:
        #
        #     expected_message = "😂, , 0x1f602, 14622, 0.805, 0.247, 0.285, 0.468, 0.221,, FACE WITH TEARS OF JOY, " \
        #                        "Emoticons ❤, , 0x2764, 8050, 0.747, 0.044, 0.166, 0.790, 0.746,, HEAVY BLACK HEART, " \
        #                        "Dingbats ♥, , 0x2665, 7144, 0.754, 0.035, 0.272, 0.693, 0.657,, BLACK HEART SUIT, " \
        #                        "Miscellaneous Symbols "
        #
        #     encoded_message = expected_message.encode()
        #
        #     raw_stream = StreamingBody(
        #         io.BytesIO(encoded_message),
        #         len(expected_message)
        #     )
        #
        #     response = {
        #         'Body': raw_stream
        #     }
        #
        #     s3_stubber.add_response("get_object", response, {})

        with patch('analyzer.EmojiAnalyzer.EmojiAnalyzer._EmojiAnalyzer__generate_emoji_scores') as mock_file:
            mock_file.return_value = {'😂': 0.221, '❤': 0.746, '😅': 0.178}
            self.post_analyzer = PostAnalyzer()
            self.reko = self.post_analyzer._PostAnalyzer__rekognition
            self.comp = self.post_analyzer._PostAnalyzer__comprehend

    def test_calculate_text_score(self):
        with Stubber(self.comp) as comprehend_stubber:
            detect_language_response = {
                'Languages': [
                    {
                        'LanguageCode': 'it',
                    }
                ]
            }

            comprehend_stubber.add_response("detect_dominant_language", detect_language_response, {'Text': stub.ANY})

            detect_sentiment_response = {
                'Sentiment': 'POSITIVE',
                'SentimentScore': {
                    'Positive': 0.91,
                    'Negative': 0.02,
                    'Neutral': 0.02,
                    'Mixed': 0.05
                }
            }

            comprehend_stubber.add_response("detect_sentiment", detect_sentiment_response, {'Text': stub.ANY,
                                                                                            'LanguageCode': stub.ANY})
            expected = ScoreComprehend(2, 91, 2, 5)
            expected.set_sentiment("positive")
            post = CrawledData(caption="testoprova")

            self.assertEqual(expected.__dict__,
                             self.post_analyzer.calculate_text_score(post).__dict__)

            self.assertEqual(expected.__dict__, post.get_comprehend_score().__dict__)

            self.assertAlmostEqual(92.1, post._CrawledData__text_score, delta=0.01)

    def test_calculate_emoji_score(self):
        post = CrawledData(caption="testoprova❤❤")
        self.post_analyzer.calculate_emoji_score(post)
        self.assertAlmostEqual(74.60, post._CrawledData__emoji_score, delta=0.01)



if __name__ == '__main__':
    unittest.main()
