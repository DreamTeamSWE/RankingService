from enum import Enum


class Sentiment(Enum):
    POSITIVE = 1
    NEGATIVE = 0
    NEUTRAL = 0.3
    MIXED = 0.1


class ScoreComprehend:
    def __init__(self, negative: float, positive: float, neutral: float, mixed: float):
        self.__positive = positive
        self.__neutral = neutral
        self.__negative = negative
        self.__mixed = mixed
        self.__principal_sentiment = None

    # set principal sentiment

    def set_sentiment(self, sentiment: str):
        if sentiment == "positive":
            self.__principal_sentiment = Sentiment.POSITIVE
        elif sentiment == "negative":
            self.__principal_sentiment = Sentiment.NEGATIVE
        elif sentiment == "mixed":
            self.__principal_sentiment = Sentiment.MIXED
        else:
            self.__principal_sentiment = Sentiment.NEUTRAL

    def calculate_score(self) -> float:
        return Sentiment.POSITIVE.value * self.__positive + \
               Sentiment.NEUTRAL.value * self.__neutral + \
               Sentiment.NEGATIVE.value * self.__negative + \
               Sentiment.MIXED.value * self.__mixed

    def set_param_for_query(self, id_post: str) -> list:
        post_id = {"name": "id_post", "value": {"stringValue": id_post}}
        negative_param = {"name": "negative", "value": {"longValue": self.__negative}}
        positive_param = {"name": "positive", "value": {"longValue": self.__positive}}
        neutral_param = {"name": "neutral", "value": {"longValue": self.__neutral}}
        mixed_param = {"name": "mixed", "value": {"longValue": self.__mixed}}
        return [post_id, negative_param, positive_param, neutral_param, mixed_param]

    def __str__(self) -> str:
        return "Principal Sentiment: " + str(self.__principal_sentiment) + "\n" + \
               "Positive: " + str(self.__positive) + "\n" + \
               "Neutral: " + str(self.__neutral) + "\n" + \
               "Negative: " + str(self.__negative) + "\n" + \
               "Mixed: " + str(self.__mixed) + "\n"
