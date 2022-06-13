import json
import unittest

from entity.Image import Image


class TestImage(unittest.TestCase):
    def setUp(self):
        self.image = Image("1.jpg")
        self.labels = {
            "Meat": 1,
            "Person": 1,
            "Wine": 1
        }
        self.emotions = {
            "HAPPY": 1
        }
        self.emotion_confid = {
                    "HAPPY": 91.06643676757812,
                    "SURPRISED": 1.04343,
                    "CALM": 0.3212432,
                    "ANGRY": 0.3212432,
                    "FEAR": 0.3212432,
                    "CONFUSED": 0.3212432,
                    "DISGUSTED": 0.321243,
                    "SAD": 0.3212432
        }
        self.image.set_emotions(self.emotions)

    def test_set_and_get_labels(self):
        self.image.set_labels(self.labels)
        self.assertEqual(self.labels, self.image.get_labels())

    def test_get_emotions(self):
        self.assertEqual(self.emotions, self.image.get_emotions())

    def test_set_and_get_emotions_confidence(self):
        self.image.set_emotions_confidence(self.emotion_confid)
        self.assertEqual(self.emotion_confid, self.image.get_emotions_confidence())

    def test_calculate_score(self):
        self.assertEqual(100.00, self.image.calculate_score())

        self.image.set_emotions(None)
        self.assertEqual(None, self.image.calculate_score())

    def test_get_image_name(self):
        self.assertEqual("1.jpg", self.image.get_image_name())

if __name__ == '__main__':
    unittest.main()
