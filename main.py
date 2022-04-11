import collections
import functools
import logging
import operator


def merge_and_sum(a: dict, b: dict) -> dict:
    """
    Merge two dictionaries and sum their values.
    """
    return {k: a.get(k, 0) + b.get(k, 0) for k in set(a) | set(b)}


if __name__ == '__main__':
    logging.basicConfig(format='%(asctime)s - %(message)s', level=logging.INFO)

    labels = {"Ravioli": 1, "Pasta": 1}
    print("labels: ")
    print(labels)

    emotions = {'HAPPY': 2}
    print("\nemotions: ")
    print(emotions)

    labels_dict = {}
    emotions_dict = {}

    print("\nlabels_dict: ")
    print(labels_dict)
    print("\nemotions_dict: ")
    print(emotions_dict)

    print("\n-------------------\n")
    print("after merge and sum: ")

    # labels_dict = {k: labels.get(k, 0) + labels_dict.get(k, 0) for k in set(labels) | set(labels_dict)}
    # emotions_dict = {k: emotions.get(k, 0) + emotions_dict.get(k, 0) for k in set(emotions) | set(emotions_dict)}
    labels_dict = merge_and_sum(labels, labels_dict)
    emotions_dict = merge_and_sum(emotions, emotions_dict)

    print("\nlabels_dict: ")
    print(labels_dict)
    print("\nemotions_dict: ")
    print(emotions_dict)

    print("\n-------------------")
    print("-------------------\n")

    labels = {"Zucchero": 1, "Pasta": 1}
    print("labels: ")
    print(labels)

    emotions = {'SAD': 2, 'HAPPY': 2}
    print("\nemotions: ")
    print(emotions)

    print("\n-------------------\n")
    print("after merge and sum: ")

    labels_dict = merge_and_sum(labels, labels_dict)
    emotions_dict = merge_and_sum(emotions, emotions_dict)

    print("\nlabels_dict: ")
    print(labels_dict)
    print("\nemotions_dict: ")
    print(emotions_dict)

    print('Done')
