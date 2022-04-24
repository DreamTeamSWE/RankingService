from enum import Enum


class Sentiment(Enum):
    POSITIVE = 1
    NEGATIVE = 0
    NEUTRAL = 0.3
    MIXED = 0.1


class ScoreComprehend:
    def __init__(self, negative: float, positive: float, neutral: float, mixed: float):
        self.positive = positive
        self.neutral = neutral
        self.negative = negative
        self.mixed = mixed
        self.principal_sentiment = None

    def __str__(self):
        return "Principal Sentiment: " + str(self.principal_sentiment) + "\n" + \
               "Positive: " + str(self.positive) + "\n" + \
               "Neutral: " + str(self.neutral) + "\n" + \
               "Negative: " + str(self.negative) + "\n" + \
               "Mixed: " + str(self.mixed) + "\n"

    # set principal sentiment
    def set_sentiment(self, sentiment: str):
        if sentiment == "positive":
            self.principal_sentiment = Sentiment.POSITIVE
        elif sentiment == "negative":
            self.principal_sentiment = Sentiment.NEGATIVE
        elif sentiment == "mixed":
            self.principal_sentiment = Sentiment.MIXED
        else:
            self.principal_sentiment = Sentiment.NEUTRAL

    def calculate_score(self) -> float:
        return Sentiment.POSITIVE.value * self.positive + \
               Sentiment.NEUTRAL.value * self.neutral + \
               Sentiment.NEGATIVE.value * self.negative + \
               Sentiment.MIXED.value * self.mixed
