import nltk
from sklearn.feature_extraction.text import TfidfVectorizer
from collections import defaultdict

nltk.download('punkt')

class TopicDetector:
    def __init__(self):
        self.vectorizer = TfidfVectorizer()
        self.topics = defaultdict(list)

    def detect_topics(self, text):
        # Sample method to detect topics from text
        tokens = nltk.word_tokenize(text)
        # Further processing would go here
        return tokens

    def extract_from_link(self, link):
        # Placeholder for link name extraction logic
        return self.detect_topics(link)

    def extract_from_caption(self, caption):
        # Placeholder for caption extraction logic
        return self.detect_topics(caption)

class ForumManager:
    def __init__(self):
        self.forums = {}

    def create_forum(self, title):
        # Logic to create a new forum
        self.forums[title] = []

    def post_topic(self, forum_title, topic):
        # Logic to post a topic in the specified forum
        if forum_title in self.forums:
            self.forums[forum_title].append(topic)

    def get_forum_topics(self, forum_title):
        # Retrieve all topics from a specific forum
        return self.forums.get(forum_title, [])

# Sample usage
if __name__ == "__main__":
    td = TopicDetector()
    fm = ForumManager()
    fm.create_forum("Tech Discussions")
    topic = td.detect_topics("Latest trends in AI")
    fm.post_topic("Tech Discussions", topic)