"""
Topic Handler - Manages topic operations and grouping

This module handles:
- Grouping topics together
- Managing topic-wise content organization
- Coordinating between topic detection and forum management
"""

from typing import Dict, List, Set, Optional
from collections import defaultdict
from topic_detection import TopicDetector, ForumManager
from topic_utils import sanitize_topic_name, forum_topic_short_name


class TopicGrouper:
    """Groups related topics together for better organization"""
    
    def __init__(self):
        self.groups: Dict[str, Set[str]] = defaultdict(set)
    
    def group_topics(self, topics: List[str]) -> Dict[str, List[str]]:
        """
        Group similar topics together
        Returns: {main_topic: [similar_topics]}
        """
        grouped = defaultdict(list)
        for topic in topics:
            sanitized = sanitize_topic_name(topic)
            short_name = forum_topic_short_name(sanitized)
            if sanitized not in grouped[short_name]:
                grouped[short_name].append(sanitized)
        return dict(grouped)
    
    def normalize_topic(self, topic: str) -> str:
        """Normalize a topic name"""
        return forum_topic_short_name(sanitize_topic_name(topic))


class BatchTopicManager:
    """
    Manages topics for a batch/upload session
    Tracks which topics were used in which batch
    """
    
    def __init__(self):
        self.batch_topics: Dict[str, Set[str]] = defaultdict(set)
        self.detector = TopicDetector()
    
    def add_topic_to_batch(self, batch_id: str, topic: str) -> None:
        """Add topic to batch record"""
        normalized = forum_topic_short_name(sanitize_topic_name(topic))
        self.batch_topics[batch_id].add(normalized)
    
    def get_batch_topics(self, batch_id: str) -> List[str]:
        """Get all unique topics used in batch"""
        return sorted(list(self.batch_topics.get(batch_id, set())))
    
    def get_topic_count_in_batch(self, batch_id: str) -> int:
        """Get number of unique topics in batch"""
        return len(self.batch_topics.get(batch_id, set()))


class ContentOrganizer:
    """
    Organizes content by topics
    Handles mapping content items to topics
    """
    
    def __init__(self):
        self.topic_content: Dict[str, List[Dict]] = defaultdict(list)
    
    def organize_entry(self, topic: str, entry: Dict) -> None:
        """
        Add entry to topic
        entry format: {url, title, topic, ...}
        """
        normalized_topic = forum_topic_short_name(sanitize_topic_name(topic))
        self.topic_content[normalized_topic].append(entry)
    
    def get_content_by_topic(self, topic: str) -> List[Dict]:
        """Get all content items for a topic"""
        normalized = forum_topic_short_name(sanitize_topic_name(topic))
        return self.topic_content.get(normalized, [])
    
    def get_all_topics(self) -> List[str]:
        """Get list of all topics with content"""
        return sorted(list(self.topic_content.keys()))
    
    def get_topic_statistics(self) -> Dict[str, int]:
        """Get count of items per topic"""
        return {
            topic: len(items)
            for topic, items in self.topic_content.items()
        }
    
    def clear(self) -> None:
        """Clear all organized content"""
        self.topic_content.clear()


# Example usage for testing
if __name__ == '__main__':
    # Test topic grouping
    grouper = TopicGrouper()
    topics = ["Arithmetic", "Arithmetic/Basic", "Advance", "Advance/Calculus"]
    grouped = grouper.group_topics(topics)
    print("Grouped topics:", grouped)
    
    # Test batch manager
    batch_mgr = BatchTopicManager()
    batch_mgr.add_topic_to_batch("batch1", "[Arithmetic]")
    batch_mgr.add_topic_to_batch("batch1", "[Advance]")
    print("Batch 1 topics:", batch_mgr.get_batch_topics("batch1"))
    
    # Test content organizer
    organizer = ContentOrganizer()
    organizer.organize_entry("Arithmetic", {"url": "http://example.com", "title": "Class 1"})
    print("Topics with content:", organizer.get_all_topics())  
