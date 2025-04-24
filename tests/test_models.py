from datetime import datetime, date
import unittest
from src.models.subject import Subject
from src.models.topic import Topic

class TestTopic(unittest.TestCase):
    def test_valid_topic_creation(self):
        """Test creating a topic with valid parameters"""
        topic = Topic("Mathematics", priority=3, estimated_hours=2.5)
        self.assertEqual(topic.name, "Mathematics")
        self.assertEqual(topic.priority, 3)
        self.assertEqual(topic.estimated_hours, 2.5)
        self.assertFalse(topic.completed)

    def test_default_values(self):
        """Test topic creation with default values"""
        topic = Topic("Physics")
        self.assertEqual(topic.priority, 1)
        self.assertEqual(topic.estimated_hours, 1.0)
        self.assertFalse(topic.completed)

    def test_invalid_priority(self):
        """Test that invalid priority values raise ValueError"""
        with self.assertRaises(ValueError):
            Topic("Chemistry", priority=0)
        with self.assertRaises(ValueError):
            Topic("Biology", priority=6)

    def test_invalid_estimated_hours(self):
        """Test that negative estimated hours raise ValueError"""
        with self.assertRaises(ValueError):
            Topic("Physics", estimated_hours=-1)

    def test_mark_complete(self):
        """Test marking a topic as complete"""
        topic = Topic("Computer Science")
        self.assertFalse(topic.completed)
        topic.mark_complete()
        self.assertTrue(topic.completed)

    def test_string_representation(self):
        """Test the string representation of a Topic"""
        topic = Topic("English", priority=4, estimated_hours=3.0)
        expected_str = "Topic: English [Priority: 4, Hours: 3.0, ✗]"
        self.assertEqual(str(topic), expected_str)
        
        topic.mark_complete()
        expected_str_completed = "Topic: English [Priority: 4, Hours: 3.0, ✓]"
        self.assertEqual(str(topic), expected_str_completed)

class TestSubject(unittest.TestCase):
    def test_valid_subject_creation(self):
        """Test creating a subject with valid parameters"""
        subject = Subject("Mathematics", exam_date=date(2025, 12, 1), difficulty=3)
        self.assertEqual(subject.name, "Mathematics")
        self.assertEqual(subject.difficulty, 3)
        self.assertEqual(subject.exam_date, date(2025, 12, 1))
        self.assertEqual(subject.progress, 0.0)
        self.assertEqual(subject.topics, [])

    def test_invalid_difficulty(self):
        """Test that invalid difficulty values raise ValueError"""
        with self.assertRaises(ValueError):
            Subject("Chemistry", exam_date=date(2025, 12, 1), difficulty=0)
        with self.assertRaises(ValueError):
            Subject("Biology", exam_date=date(2025, 12, 1), difficulty=6)

    def test_exam_date_in_past(self):
        """Test that exam date in the past raises ValueError"""
        with self.assertRaises(ValueError):
            Subject("Physics", exam_date=date(2020, 1, 1))

    def test_add_topic(self):
        """Test adding a topic to a subject"""
        subject = Subject("Computer Science", exam_date=date(2025, 12, 1))
        topic = Topic("Data Structures")
        subject.add_topic(topic)
        self.assertIn(topic, subject.topics)

    def test_remove_topic(self):
        """Test removing a topic from a subject"""
        subject = Subject("Computer Science", exam_date=date(2025, 12, 1))
        topic = Topic("Data Structures")
        subject.add_topic(topic)
        subject.remove_topic(topic)
        self.assertNotIn(topic, subject.topics)

if __name__ == '__main__':
    unittest.main()