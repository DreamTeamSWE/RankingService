class Image:
    def __init__(self, image_name: str):
        self.image_name = image_name
        self.labels = {}
        self.emotions = {}

    def set_labels(self, labels: dict):
        self.labels = labels

    def set_emotions(self, emotions: dict):
        self.emotions = emotions
