from enum import Enum
from typing import List


class Emotions(float, Enum):
    HAPPY = 1
    SURPRISED = 0.6
    CALM = 0.4
    SAD = 0.2
    CONFUSED = 0.15
    ANGRY = 0.1
    DISGUSTED = 0
    FEAR = 0


class Image:
    def __init__(self, image_name: str):
        self.__image_name = image_name
        self.__labels = {}
        self.__emotions = {}
        self.__emotions_confidence = [{}]

    def set_labels(self, labels: dict):
        self.__labels = labels

    def set_emotions(self, emotions: dict):
        self.__emotions = emotions

    def set_emotions_confidence(self, emotions_confid: List[dict]):
        self.__emotions_confidence = emotions_confid

    def get_image_name(self) -> str:
        return self.__image_name

    def get_labels(self) -> dict:
        return self.__labels

    def get_emotions(self) -> dict:
        return self.__emotions

    def get_emotions_confidence(self) -> List[dict]:
        return self.__emotions_confidence

    def calculate_score(self):
        if self.__emotions:
            partial_sum = 0.0
            for emotion, num in self.__emotions.items():
                partial_sum += Emotions[emotion].value * num
            return partial_sum
        return None

    # to string
    def __str__(self) -> str:
        return "image name: " + self.__image_name
