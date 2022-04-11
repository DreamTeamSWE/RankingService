import boto3
import operator
import functools
import collections
from abc import ABC
from entity import CrawledData
from analyzer.Analyzer import Analyzer
from entity.ScoreComprehend import ScoreComprehend
from db.RepositoryInternal import RepositoryInternal

AWS_REGION = 'eu-central-1'


def merge_and_sum(a: dict, b: dict) -> dict:
    """
    Merge two dictionaries and sum their values.
    """
    return {k: a.get(k, 0) + b.get(k, 0) for k in set(a) | set(b)}


def detect_sentiment_text(post: CrawledData) -> ScoreComprehend:
    print("\n-------------------")
    print('detect_sentiment_text')

    comprehend = boto3.client(service_name='comprehend',
                              region_name=AWS_REGION)
    # result of comprehend
    json_result = comprehend.detect_sentiment(Text=post.caption, LanguageCode='it')

    # get sentiment
    array = json_result["SentimentScore"]
    sentiment_score = json_result["Sentiment"]

    # get score
    negative = int(array["Negative"] * 100)
    neutral = int(array["Neutral"] * 100)
    positive = int(array["Positive"] * 100)

    score = ScoreComprehend(negative, neutral, positive)
    score.set_sentiment(sentiment_score)

    return score


def detect_labels(photo, bucket):
    print("\n-------------------")
    print('detect_labels')

    client = boto3.client('rekognition', region_name=AWS_REGION)

    response = client.detect_labels(Image={'S3Object': {'Bucket': bucket, 'Name': photo}},
                                    MaxLabels=10)

    print('Detecting labels for ' + photo)

    labels_dict = {}
    theresPerson = False

    for label in response['Labels']:
        if label['Confidence'] >= 90:
            if label['Name'] == 'Person':
                theresPerson = True
            else:
                for parent in label['Parents']:
                    if parent['Name'] == 'Food':
                        if label['Name'] in labels_dict:
                            labels_dict[label['Name']] += 1
                        else:
                            labels_dict[label['Name']] = 1

    return labels_dict, theresPerson


def detect_sentiment_person(img_url: str, bucket: str):
    print("\n-------------------")
    print('detect_sentiment_person')

    reko = boto3.client('rekognition', region_name=AWS_REGION)
    print(img_url)
    response = reko.detect_faces(Image={'S3Object': {'Bucket': bucket, 'Name': img_url}},
                                 Attributes=['ALL'])
    emozioniEmpty = True
    emotions_dict = {}

    for faceDetail in response['FaceDetails']:
        emotions = faceDetail['Emotions']
        for emotion in emotions:
            if emotion['Confidence'] >= 90:
                if emotion['Type'] in emotions_dict:
                    emotions_dict[emotion['Type']] += 1
                else:
                    emotions_dict[emotion['Type']] = 1
                emozioniEmpty = False

    return emotions_dict, emozioniEmpty


def image_analyzer(name_image: str):
    print("\n-------------------")
    print('image_analyzer')

    bucket = 'dream-team-img-test'
    emotions = {}

    print("\n-------------------")
    name_image = str(name_image) + ".jpg"
    print(name_image)

    labels, theresPerson = detect_labels(name_image, bucket)
    if theresPerson:
        print("There is a person")

        emotions, emozioniEmpty = detect_sentiment_person(name_image, bucket)
        if not emozioniEmpty:
            print("Emotion detected")
        else:
            print("No emotion detected")
    else:
        print("There is no person")

    print("-------------------\n")
    return labels, emotions


class PostAnalyzer(Analyzer, ABC):
    def analyze(self, post: CrawledData):
        print("Hello from PostAnalyzer")

        score = detect_sentiment_text(post)
        post.set_score(score)

        print("\n" + str(score) + "\n-------------------\n")

        labels_dict = {}
        emotions_dict = {}

        if post.list_image is not None:
            for name_image in post.list_image:
                labels, emotions = image_analyzer(name_image)

                if len(labels) > 0:
                    labels_dict = merge_and_sum(labels_dict, labels)
                if len(emotions) > 0:
                    emotions_dict = merge_and_sum(emotions_dict, emotions)

                post.set_labels(labels)
                post.set_emotions(emotions)
        else:
            print("\nNo image in post\n")

        repository = RepositoryInternal()
        repository.save_post(post)
