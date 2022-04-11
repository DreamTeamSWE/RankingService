import boto3
from abc import ABC
from analyzer.Analyzer import Analyzer
from entity import CrawledData
from entity import Image
from entity.ScoreComprehend import ScoreComprehend
from db.RepositoryInternal import RepositoryInternal

AWS_REGION = 'eu-central-1'


def merge_and_sum(a: dict, b: dict) -> dict:
    """
    Merge two dictionaries and sum their values.

    :param a: first dictionary
    :param b: second dictionary

    :rtype: dict
    :return: merged dictionary
    """
    return {k: a.get(k, 0) + b.get(k, 0) for k in set(a) | set(b)}


def detect_sentiment_text(post: CrawledData) -> ScoreComprehend:
    """
    Detect sentiment of a post with Comprehend.

    :param post: post to analyze with Comprehend

    :rtype: ScoreComprehend
    :return: Comprehend confidence score
    """
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


def detect_labels(photo: Image, bucket: str):
    """
    Detect object of an image with Rekognition.

    :param bucket: name of S3 bucket
    :param photo: image to analyze with Rekognition

    :rtype: dict, bool
    :return: Dictionary of labels and boolean if there is a person
    """
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


def detect_sentiment_person(name_image: str, bucket: str):
    """
    Detect sentiment of a person with Comprehend.

    :param name_image: name of the image to analyze with Rekognition
    :param bucket: name of S3 bucket

    :rtype: dict, bool
    :return: Dictionary of emotions and boolean if emotions were found
    """
    print("\n-------------------")
    print('detect_sentiment_person')

    reko = boto3.client('rekognition', region_name=AWS_REGION)
    print(name_image)
    response = reko.detect_faces(Image={'S3Object': {'Bucket': bucket, 'Name': name_image}},
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
    """
    Analyze an image with Rekognition.

    :param name_image: name of the image to analyze

    :rtype: dict, dict
    :return: Dictionary of labels and dictionary of emotions
    """
    print("\n-------------------")
    print('image_analyzer')

    bucket = 'dream-team-img-test'
    emotions = {}

    print("\n-------------------")
    if not name_image.__contains__('.jpg'):
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
        """
        Analyze a post with Rekognition and Comprehend.
        After analyze, rds db is updated with the new data.

        :param post: Post to analyze
        """
        print("\nHello from PostAnalyzer\n")

        # calcolo punteggio caption con comprehend
        # score = detect_sentiment_text(post)
        # post.set_score(score)
        #
        # print("\ncomprehend score: " + str(score) + "\n-------------------\n")
        #
        # labels_dict = {}
        # emotions_dict = {}
        #
        # # calcolo punteggio per ogni immagine e salvo
        # if post.list_images is not None:
        #     for image_in_list in post.list_images:
        #         labels, emotions = image_analyzer(image_in_list.image_name)
        #
        #         if len(labels) > 0:
        #             labels_dict = merge_and_sum(labels_dict, labels)
        #         if len(emotions) > 0:
        #             emotions_dict = merge_and_sum(emotions_dict, emotions)
        #
        #         # post.set_labels(labels)
        #         # post.set_emotions(emotions)
        #
        #         image_in_list.set_labels(labels)
        #         image_in_list.set_emotions(emotions)
        # else:
        #     print("\nNo image in post\n")

        repository = RepositoryInternal()
        repository.save_post(post)
