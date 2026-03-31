"""
Topic Detection and Forum Management Module

This module handles:
- Detecting topics from various sources (file names, URLs, text patterns)
- Creating and managing forum topics in Telegram groups
- Organizing content by topic with proper thread management
"""

import re
from pathlib import PurePosixPath
from urllib.parse import unquote, urlparse
from collections import defaultdict
from typing import List, Dict, Tuple, Optional


class TopicDetector:
    """
    Detects topics from various sources:
    - File names with patterns like [Topic]
    - URL filenames
    - Text with explicit topic markers
    """
    
    TOPIC_PATTERN = re.compile(r"^\[(?P<topic>[^\[\]]+)\]", re.IGNORECASE)
    
    def __init__(self):
        self.topics_cache: Dict[str, List[str]] = defaultdict(list)
    
    def detect_from_text(self, text: str) -> str:
        """
        Detect topic from text with markers like [Arithmetic] or [Advance]
        Returns: Detected topic or 'General'
        """
        if not text:
            return "General"
        
        # Check for [Topic] pattern at start
        match = self.TOPIC_PATTERN.match(text)
        if match:
            topic = match.group("topic").strip()
            return topic if topic else "General"
        
        # Check for explicit topic markers
        topic_markers = [" - topic:", ": topic ", "topic: ", "topic ="]
        for marker in topic_markers:
            if marker in text.lower():
                idx = text.lower().find(marker)
                topic = text[idx + len(marker):].split()[0].strip("[]()").strip()
                if topic:
                    return topic
        
        return "General"
    
    def detect_from_url(self, url: str) -> str:
        """
        Extract topic from URL filename
        Example: /videos/[Arithmetic]_class1.mp4 -> [Arithmetic]
        """
        try:
            parsed = urlparse(url)
            filename = unquote(PurePosixPath(parsed.path).name)
            
            # Check if filename has [Topic] pattern
            topic = self.detect_from_text(filename)
            return topic
        except Exception:
            return "General"
    
    def detect_from_link_name(self, link: str) -> str:
        """
        Detect topic from link description/name (for txt file URLs)
        """
        return self.detect_from_url(link)
    
    def cache_topic(self, user_id: int, topic: str) -> None:
        """Cache detected topic for user"""
        if topic not in self.topics_cache[str(user_id)]:
            self.topics_cache[str(user_id)].append(topic)
    
    def get_cached_topics(self, user_id: int) -> List[str]:
        """Get all cached topics for user"""
        return self.topics_cache.get(str(user_id), [])
    
    def clear_cache(self, user_id: int) -> None:
        """Clear user's topic cache"""
        if str(user_id) in self.topics_cache:
            del self.topics_cache[str(user_id)]


class ForumManager:
    """
    Manages forum topics and thread organization
    Handles creating and organizing topics in Telegram forums
    """
    
    def __init__(self):
        self.forums: Dict[int, Dict[str, int]] = {}  # {chat_id: {topic_name: thread_id}}
        self.detector = TopicDetector()
    
    def create_forum_entry(self, chat_id: int, topic_name: str, thread_id: int) -> None:
        """Create entry for forum topic thread"""
        if chat_id not in self.forums:
            self.forums[chat_id] = {}
        self.forums[chat_id][topic_name] = thread_id
    
    def get_thread_id(self, chat_id: int, topic_name: str) -> Optional[int]:
        """Get thread ID for a topic in chat"""
        if chat_id in self.forums:
            return self.forums[chat_id].get(topic_name)
        return None
    
    def get_forum_topics(self, chat_id: int) -> Dict[str, int]:
        """Get all topics and thread IDs for a chat"""
        return self.forums.get(chat_id, {})
    
    def topic_exists(self, chat_id: int, topic_name: str) -> bool:
        """Check if topic thread exists for chat"""
        return chat_id in self.forums and topic_name in self.forums[chat_id]


# Global instances for easy access
topic_detector = TopicDetector()
forum_manager = ForumManager()


if __name__ == "__main__":
    # Test topic detection
    detector = TopicDetector()
    
    # Test text detection
    print(detector.detect_from_text("[Arithmetic] Class 1"))  # → Arithmetic
    print(detector.detect_from_text("[Advance] Mathematics"))  # → Advance
    print(detector.detect_from_text("No topic here"))  # → General
    
    # Test forum manager
    fm = ForumManager()
    fm.create_forum_entry(12345, "Arithmetic", 789)
    print(fm.get_thread_id(12345, "Arithmetic"))  # → 789