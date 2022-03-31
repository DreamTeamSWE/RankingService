from enum import Enum


class Sentiment(Enum):
    POSITIVE = 1
    NEGATIVE = 2
    NEUTRAL = 3


class ScoreComprehend:
    def __init__(self, negative, positive, neutral):
        self.principal_sentiment = None
        self.negative = negative
        self.positive = positive
        self.neutral = neutral

    def __str__(self):
        return "Principal Sentiment: " + str(self.principal_sentiment) + "\n" + \
               "Negative: " + str(self.negative) + "\n" + \
               "Positive: " + str(self.positive) + "\n" + \
               "Neutral: " + str(self.neutral) + "\n"

    def set_sentiment(self, sentiment: str):
        if sentiment == "positive":
            self.principal_sentiment = Sentiment.POSITIVE
        elif sentiment == "negative":
            self.principal_sentiment = Sentiment.NEGATIVE
        else:
            self.principal_sentiment = Sentiment.NEUTRAL
