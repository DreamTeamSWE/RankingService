from enum import Enum


class Sentiment(Enum):
    POSITIVE = 1
    NEGATIVE = 2
    NEUTRAL = 3


class ScoreComprehend:
    def __init__(self, negative: int, positive: int, neutral: int):
        self.negative = negative
        self.positive = positive
        self.neutral = neutral
        self.principal_sentiment = None

    def __str__(self):
        return "Principal Sentiment: " + str(self.principal_sentiment) + "\n" + \
               "Negative: " + str(self.negative) + "\n" + \
               "Positive: " + str(self.positive) + "\n" + \
               "Neutral: " + str(self.neutral) + "\n"

    # set principal sentiment
    def set_sentiment(self, sentiment: str):
        if sentiment == "positive":
            self.principal_sentiment = Sentiment.POSITIVE
        elif sentiment == "negative":
            self.principal_sentiment = Sentiment.NEGATIVE
        else:
            self.principal_sentiment = Sentiment.NEUTRAL

    def calculate_score(self) -> int:
        return self.negative + self.positive + self.neutral
