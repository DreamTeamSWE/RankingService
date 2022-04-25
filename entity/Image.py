from typing import List

from enum import Enum


class Emotions(float, Enum):
    HAPPY = 1
    CALM = 0.4
    SAD = 0.2
    ANGRY = 0.1
    SURPRISED = 0.6
    CONFUSED = 0.15
    DISGUSTED = 0
    FEAR = 0


class Image:
    def __init__(self, image_name: str):
        self.image_name = image_name
        self.labels = {}
        self.emotions = {}
        self.emotions_confidence = {}

    def set_labels(self, labels: dict):
        self.labels = labels

    def set_emotions(self, emotions: dict):
        self.emotions = emotions

    def set_emotions_confidence(self, emotions_confid: List[dict]):
        self.emotions_confidence = emotions_confid

    def calculate_score(self):
        if self.emotions:
            partial_sum = 0.0
            for emotion, num in self.emotions.items():
                partial_sum += Emotions[emotion].value * num
            return partial_sum
        return None

    # to string
    def __str__(self) -> str:
        return "__str__ image name: " + self.image_name
