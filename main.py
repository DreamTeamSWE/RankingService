from enum import Enum


class Sentiment(Enum):
    POSITIVE = 1
    NEGATIVE = 0
    NEUTRAL = 0.3
    MIXED = 0.1


if __name__ == '__main__':
    print(Sentiment.MIXED.value)

    final_sentiment = 1 + Sentiment.NEUTRAL.value

    print(final_sentiment)
    pass
