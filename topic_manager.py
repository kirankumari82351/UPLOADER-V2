# topic_manager.py

class TopicManager:
    def __init__(self):
        self.topics = {}

    def add_topic(self, topic_name):
        if topic_name not in self.topics:
            self.topics[topic_name] = []

    def add_forum_post(self, topic_name, post_content):
        if topic_name in self.topics:
            self.topics[topic_name].append(post_content)
        else:
            raise ValueError(f"Topic '{topic_name}' does not exist")

    def get_topics(self):
        return list(self.topics.keys())

    def get_posts_for_topic(self, topic_name):
        if topic_name in self.topics:
            return self.topics[topic_name]
        else:
            raise ValueError(f"Topic '{topic_name}' does not exist")

# Example usage:
# manager = TopicManager()
# manager.add_topic('Sports')
# manager.add_forum_post('Sports', 'Post about football')
# print(manager.get_posts_for_topic('Sports'))