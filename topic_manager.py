"""
Topic Management Module

Comprehensive topic management for batch uploads
- Track topics across batches
- Save/retrieve topic mappings
- Generate reports on topic-wise uploads
"""

from typing import Dict, List, Optional, Set
from datetime import datetime
from collections import defaultdict


class TopicManager:
    """
    Comprehensive topic manager for tracking and organizing topics
    across multiple uploads and batches
    """
    
    def __init__(self):
        self.topics: Dict[str, Dict] = {}  # {topic_name: {metadata}}
        self.batch_mappings: Dict[str, List[str]] = defaultdict(list)  # {batch_id: [topics]}
        self.topic_stats: Dict[str, Dict] = defaultdict(lambda: {"count": 0, "last_used": None})
    
    def add_topic(self, topic_name: str, batch_id: str = None) -> None:
        """
        Add or register a topic
        
        Args:
            topic_name: Name of the topic
            batch_id: Optional batch ID to associate
        """
        if topic_name not in self.topics:
            self.topics[topic_name] = {
                "created": datetime.now().isoformat(),
                "usage_count": 0
            }
        
        if batch_id:
            if topic_name not in self.batch_mappings[batch_id]:
                self.batch_mappings[batch_id].append(topic_name)
            self.topic_stats[topic_name]["count"] += 1
            self.topic_stats[topic_name]["last_used"] = datetime.now().isoformat()
    
    def get_topics(self) -> List[str]:
        """Get all registered topics"""
        return sorted(list(self.topics.keys()))
    
    def get_topics_for_batch(self, batch_id: str) -> List[str]:
        """Get all topics used in a specific batch"""
        return self.batch_mappings.get(batch_id, [])
    
    def get_topic_info(self, topic_name: str) -> Optional[Dict]:
        """Get detailed information about a topic"""
        if topic_name in self.topics:
            return {
                **self.topics[topic_name],
                **self.topic_stats.get(topic_name, {})
            }
        return None
    
    def topic_exists(self, topic_name: str) -> bool:
        """Check if topic exists"""
        return topic_name in self.topics
    
    def get_topic_count(self) -> int:
        """Get total number of unique topics"""
        return len(self.topics)
    
    def get_batch_topic_count(self, batch_id: str) -> int:
        """Get number of unique topics in a batch"""
        return len(self.batch_mappings.get(batch_id, []))
    
    def get_statistics(self) -> Dict:
        """Get overall topic statistics"""
        return {
            "total_topics": len(self.topics),
            "total_batches": len(self.batch_mappings),
            "most_used": self._get_most_used_topics(),
            "topic_usage": dict(self.topic_stats)
        }
    
    def _get_most_used_topics(self, limit: int = 5) -> List[str]:
        """Get most frequently used topics"""
        sorted_topics = sorted(
            self.topic_stats.items(),
            key=lambda x: x[1]["count"],
            reverse=True
        )
        return [topic for topic, _ in sorted_topics[:limit]]
    
    def clear_batch(self, batch_id: str) -> None:
        """Clear a batch from tracking"""
        if batch_id in self.batch_mappings:
            del self.batch_mappings[batch_id]
    
    def clear_all(self) -> None:
        """Clear all topics and mappings"""
        self.topics.clear()
        self.batch_mappings.clear()
        self.topic_stats.clear()


class TopicForumMapping:
    """
    Maps topics to forum thread information
    Maintains correspondence between topics and chat forum threads
    """
    
    def __init__(self):
        self.mappings: Dict[int, Dict[str, int]] = {}  # {chat_id: {topic: thread_id}}
        self.reverse_mappings: Dict[int, Dict[int, str]] = {}  # {chat_id: {thread_id: topic}}
    
    def add_mapping(self, chat_id: int, topic: str, thread_id: int) -> None:
        """Add topic->thread mapping for a chat"""
        if chat_id not in self.mappings:
            self.mappings[chat_id] = {}
            self.reverse_mappings[chat_id] = {}
        
        self.mappings[chat_id][topic] = thread_id
        self.reverse_mappings[chat_id][thread_id] = topic
    
    def get_thread_id(self, chat_id: int, topic: str) -> Optional[int]:
        """Get thread ID for a topic in chat"""
        return self.mappings.get(chat_id, {}).get(topic)
    
    def get_topic_for_thread(self, chat_id: int, thread_id: int) -> Optional[str]:
        """Get topic for a thread in chat"""
        return self.reverse_mappings.get(chat_id, {}).get(thread_id)
    
    def get_all_topics_in_chat(self, chat_id: int) -> List[str]:
        """Get all topics mapped in a chat"""
        return list(self.mappings.get(chat_id, {}).keys())
    
    def get_all_threads_in_chat(self, chat_id: int) -> Dict[str, int]:
        """Get all topic->thread mappings in a chat"""
        return self.mappings.get(chat_id, {})
    
    def topic_mapped(self, chat_id: int, topic: str) -> bool:
        """Check if topic is already mapped in chat"""
        return chat_id in self.mappings and topic in self.mappings[chat_id]
    
    def clear_chat(self, chat_id: int) -> None:
        """Clear all mappings for a chat"""
        if chat_id in self.mappings:
            del self.mappings[chat_id]
        if chat_id in self.reverse_mappings:
            del self.reverse_mappings[chat_id]


# Example usage for testing
if __name__ == "__main__":
    # Test TopicManager
    manager = TopicManager()
    manager.add_topic("Arithmetic", "batch1")
    manager.add_topic("Advance", "batch1")
    manager.add_topic("Arithmetic", "batch2")
    
    print("All topics:", manager.get_topics())
    print("Batch 1 topics:", manager.get_topics_for_batch("batch1"))
    print("Statistics:", manager.get_statistics())
    
    # Test TopicForumMapping
    mapping = TopicForumMapping()
    mapping.add_mapping(-100123456, "Arithmetic", 789)
    mapping.add_mapping(-100123456, "Advance", 790)
    
    print("Thread ID for Arithmetic:", mapping.get_thread_id(-100123456, "Arithmetic"))
    print("All topics in chat:", mapping.get_all_topics_in_chat(-100123456))