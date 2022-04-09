from abc import ABC
import boto3
from analyzer.Analyzer import Analyzer
from entity import CrawledData
from entity.ScoreComprehend import ScoreComprehend
from db.RepositoryInternal import RepositoryInternal

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
            if label['Name'] == 'Person':
                theresPerson = True
            elif label['Parents'] == 'Food':
                labels.append(label['Name'])

    return labels, theresPerson
    # print("Label: " + label['Name'])
    # print("Confidence: " + str(label['Confidence']))
    # print("Instances:")
    # for instance in label['Instances']:
    #     print("  Confidence: " + str(instance['Confidence']))
    #     print()
    #
    # print("Parents:")
    # for parent in label['Parents']:
    #     print("   " + parent['Name'])
    # print("----------")
    # print()


def detect_sentiment_person(img_url: str, bucket: str):
    reko = boto3.client('rekognition', region_name=AWS_REGION)
    print(img_url)
    response = reko.detect_faces(Image={'S3Object': {'Bucket': bucket, 'Name': img_url}},
                                 Attributes=['ALL'])
    count = 1
    emozioniEmpty = True
    emotion = ''
    for y in response["FaceDetails"]:
        emotion += f'persona {count}:\n'
        for x in y["Emotions"]:
            type_sent = x["Type"]
            confidence = x["Confidence"]
            if confidence > 75:
                emozioniEmpty = False
                emotion += f'emozione: {type_sent}, confidence: {confidence}\n'
        count += 1

    return emotion, emozioniEmpty


def image_analyzer(list_image: list):
    bucket = 'dream-team-img-test'
    labels = []
    emotions = []
    for name_image in list_image:
        print("\n-------------------")
        name_image = str(name_image) + ".jpg"
        print(name_image)

        label_returned, theresPerson = detect_labels(name_image, bucket)
        print(label_returned)
        labels.append(label_returned)
        if theresPerson:
            print("There is a person")

            emotion_returned, emozioniEmpty = detect_sentiment_person(name_image, bucket)
            if emozioniEmpty:
                print("No emotion detected")

            else:
                print(emotion_returned)
                emotions.append(emotion_returned)
                # setattr(post, "emotion_rekognition", emotion)
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

        if post.list_image is not None:
            labels, emotions = image_analyzer(post.list_image)
            post.set_labels(labels)
            post.set_emotions(emotions)
        else:
            print("\nNo image in post\n")

        repository = RepositoryInternal()
        repository.save_post(post)
