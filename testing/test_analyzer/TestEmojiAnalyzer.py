import unittest
from unittest.mock import patch

from analyzer.EmojiAnalyzer import EmojiAnalyzer
from entity.CrawledData import CrawledData


class TestEmojiAnalyzer(unittest.TestCase):
    def setUp(self):
        with patch('analyzer.EmojiAnalyzer.EmojiAnalyzer._EmojiAnalyzer__generate_emoji_scores') as mock_file:
            mock_file.return_value = {'😂': 0.7105, '❤': 0.973, '😅': 0.689}
            self.emoji_analyzer = EmojiAnalyzer()

    def test_analyze_single_emoji(self):
        post = CrawledData(caption='😂testo')
        self.assertAlmostEqual(71.05, self.emoji_analyzer.analyze(post), delta=0.01)

    def test_analyze_single_emoji_ending(self):
        post = CrawledData(caption='testo😅')
        self.assertAlmostEqual(82.679, self.emoji_analyzer.analyze(post), delta=0.01)

    def test_analyze_double_emoji(self):
        post = CrawledData(caption='❤❤testo')
        self.assertAlmostEqual(97.3, self.emoji_analyzer.analyze(post), delta=0.01)

    def test_analyze_triple_emoji(self):
        post = CrawledData(caption='❤❤❤testo')
        result = self.emoji_analyzer.analyze(post)
        self.assertAlmostEqual(97.3, result, delta=0.01)

    def test_analyze_multiple_emoji(self):
        post = CrawledData(caption='❤❤❤❤testo')
        self.assertAlmostEqual(97.3, self.emoji_analyzer.analyze(post), delta=0.01)

    def test_analyze_multiple_different_emoji(self):
        post = CrawledData(caption='😅❤😅❤testo')
        self.assertAlmostEqual(83.1, self.emoji_analyzer.analyze(post), delta=0.01)

    def test_analyze_multiple_emoji_ending(self):
        post = CrawledData(caption='testo😂😂😂😂')
        self.assertAlmostEqual(92.365, self.emoji_analyzer.analyze(post), delta=0.01)

    def test_analyze_unsupported_emoji(self):
        post = CrawledData(caption='😍')
        self.assertEqual(None, self.emoji_analyzer.analyze(post))

    def test_analyze_no_emoji(self):
        post = CrawledData(caption='testo')
        self.assertEqual(None, self.emoji_analyzer.analyze(post))


if __name__ == '__main__':
    unittest.main()
