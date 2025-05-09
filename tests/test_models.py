from datetime import date
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
        expected_str = "Topic: English [Priority: 4, Progress: 0.0%, Hours: 0.0/3.0, ✗]"
        self.assertEqual(str(topic), expected_str)
        
        topic.mark_complete()
        expected_str_completed = "Topic: English [Priority: 4, Progress: 100.0%, Hours: 3.0/3.0, ✓]"
        self.assertEqual(str(topic), expected_str_completed)

    def test_reset_progress(self):
        """Test resetting topic progress"""
        topic = Topic("Computer Science", priority=4, estimated_hours=5.0)
        topic.add_hours(3.0)
        topic.reset_progress()
        self.assertEqual(topic.hours_spent, 0.0)
        self.assertFalse(topic.completed)

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

    def test_reset_subject_progress(self):
        """Test resetting all topics' progress in a subject"""
        subject = Subject("Computer Science", exam_date=date(2025, 12, 1))
        topic1 = Topic("Data Structures", priority=5, estimated_hours=10)
        topic2 = Topic("Algorithms", priority=4, estimated_hours=8)
        
        # Add some progress
        topic1.add_hours(5)
        topic2.mark_complete()
        
        subject.add_topic(topic1)
        subject.add_topic(topic2)
        
        # Reset progress
        subject.reset_progress()
        
        # Verify all topics are reset
        self.assertEqual(subject.topics[0].hours_spent, 0.0)
        self.assertFalse(subject.topics[0].completed)
        self.assertEqual(subject.topics[1].hours_spent, 0.0)
        self.assertFalse(subject.topics[1].completed)
        self.assertEqual(subject.progress, 0.0)

    def test_string_representation(self):
        """Test the string representation of a Subject"""
        subject = Subject("Physics", exam_date=date(2025, 5, 15), difficulty=4)
        expected_str = "Subject: Physics [Exam date: 2025-05-15, Difficulty: 4, Progress: 0.00%, Status: ✗]"
        self.assertEqual(str(subject), expected_str)
        
        # Test with some progress
        topic = Topic("Mechanics")
        topic.mark_complete()
        subject.add_topic(topic)
        subject.update_progress()
        expected_str_with_progress = "Subject: Physics [Exam date: 2025-05-15, Difficulty: 4, Progress: 100.00%, Status: ✓]"
        self.assertEqual(str(subject), expected_str_with_progress)

if __name__ == '__main__':
    unittest.main()