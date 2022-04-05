from abc import ABC
import boto3
from analyzer.Analyzer import Analyzer
from entity import CrawledData
from entity.ScoreComprehend import ScoreComprehend

AWS_REGION = 'eu-central-1'


def detect_sentiment_text(post: CrawledData) -> ScoreComprehend:
    comprehend = boto3.client(service_name='comprehend',
                              region_name=AWS_REGION)
    # result of comprehend
    json_result = comprehend.detect_sentiment(Text=post.caption, LanguageCode='it')

    # get sentiment
    array = json_result["SentimentScore"]
    sentiment_score = json_result["Sentiment"]

    # get score
    negative = array["Negative"] * 100
    neutral = array["Neutral"] * 100
    positive = array["Positive"] * 100

    score = ScoreComprehend(negative, neutral, positive)
    score.set_sentiment(sentiment_score)

    return score


def detect_labels(photo, bucket):
    client = boto3.client('rekognition', region_name=AWS_REGION)

    response = client.detect_labels(Image={'S3Object': {'Bucket': bucket, 'Name': photo}},
                                    MaxLabels=10)

    print('Detected labels for ' + photo)
    print()

    labels = []
    theresPerson = False

    for label in response['Labels']:
        if label['Confidence'] > 90:
            labels.append(label)
            if label['Name'] == 'Person':
                theresPerson = True

    return labels, theresPerson

    #
    #
    #
    #
    #     print("Label: " + label['Name'])
    #     print("Confidence: " + str(label['Confidence']))
    #     print("Instances:")
    #     for instance in label['Instances']:
    #         print("  Bounding box")
    #         print("    Top: " + str(instance['BoundingBox']['Top']))
    #         print("    Left: " + str(instance['BoundingBox']['Left']))
    #         print("    Width: " + str(instance['BoundingBox']['Width']))
    #         print("    Height: " + str(instance['BoundingBox']['Height']))
    #         print("  Confidence: " + str(instance['Confidence']))
    #         print()
    #
    #     print("Parents:")
    #     for parent in label['Parents']:
    #         print("   " + parent['Name'])
    #     print("----------")
    #     print()
    # return len(response['Labels'])


class PostAnalyzer(Analyzer, ABC):
    def analyze(self, post: CrawledData):
        print("Hello from PostAnalyzer")

        score = detect_sentiment_text(post)

        print("\n" + str(score) + "\n-------------------\n")

        list_image = post.list_image

        if list_image is not None:
            for name_image in list_image:
                print("\n-------------------")
                name_image = str(name_image) + ".jpg"
                print(name_image)

                labels, theresPerson = detect_labels(name_image, 'dream-team-img-test')
                print(labels)
                if theresPerson:
                    print("There is a person")
                else:
                    print("There is no person")

                print("-------------------\n")

        else:
            print("\nNo image in post\n")
