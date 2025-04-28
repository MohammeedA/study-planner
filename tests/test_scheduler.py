"""Tests for the scheduler module."""

import unittest
from datetime import date, timedelta
from src.models.subject import Subject
from src.models.topic import Topic
from src.controllers.scheduler import Scheduler

class TestScheduler(unittest.TestCase):
    def setUp(self):
        """Set up test subjects and topics."""
        # Create test date starting tomorrow to avoid validation errors
        self.start_date = date.today() + timedelta(days=1)
        
        # Create two test subjects
        self.math = Subject("Mathematics", 
                          exam_date=self.start_date + timedelta(days=10),
                          difficulty=4)
        self.math.add_topic(Topic("Calculus", priority=5, estimated_hours=10))
        self.math.add_topic(Topic("Algebra", priority=3, estimated_hours=8))
        
        self.physics = Subject("Physics",
                            exam_date=self.start_date + timedelta(days=5),
                            difficulty=3)
        self.physics.add_topic(Topic("Mechanics", priority=4, estimated_hours=6))
        self.physics.add_topic(Topic("Thermodynamics", priority=3, estimated_hours=4))
        
        self.subjects = [self.math, self.physics]
        self.scheduler = Scheduler(self.subjects)
        
    def test_create_schedule(self):
        """Test that create_schedule returns a valid schedule."""
        schedule = self.scheduler.create_schedule(start_date=self.start_date)
        
        self.assertTrue(isinstance(schedule, list))
        self.assertTrue(len(schedule) > 0)
        
        # Check first day's schedule
        first_day = schedule[0]
        self.assertEqual(first_day["date"], self.start_date)
        self.assertTrue(isinstance(first_day["topics"], list))
        
        # Verify schedule structure
        for day in schedule:
            self.assertIn("date", day)
            self.assertIn("topics", day)
            for topic in day["topics"]:
                self.assertIn("subject", topic)
                self.assertIn("topic", topic)
                self.assertIn("hours", topic)
                self.assertIn("priority", topic)
                
    def test_get_next_days_schedule(self):
        """Test getting schedule for next N days."""
        days = 3
        schedule = self.scheduler.get_next_days_schedule(days)
        
        # Should not return more days than requested
        self.assertLessEqual(len(schedule), days)
        
    def test_completed_topics_excluded(self):
        """Test that completed topics are not scheduled."""
        # Mark a topic as complete
        self.math.topics[0].mark_complete()
        
        schedule = self.scheduler.create_schedule(start_date=self.start_date)
        
        # Check that the completed topic is not in the schedule
        for day in schedule:
            for topic in day["topics"]:
                self.assertNotEqual(topic["topic"], "Calculus")
                
    def test_exam_date_ordering(self):
        """Test that subjects are scheduled according to exam dates."""
        schedule = self.scheduler.create_schedule(start_date=self.start_date)
        
        # Physics exam is sooner, should be prioritized in early days
        first_day = schedule[0]
        physics_topics_first_day = [
            t for t in first_day["topics"] 
            if t["subject"] == "Physics"
        ]
        self.assertTrue(len(physics_topics_first_day) > 0)
        
    def test_empty_subjects(self):
        """Test scheduling with no subjects."""
        scheduler = Scheduler([])
        schedule = scheduler.create_schedule(start_date=self.start_date)
        self.assertEqual(len(schedule), 0)
        
    def test_all_topics_completed(self):
        """Test scheduling when all topics are completed."""
        # Mark all topics as complete
        for subject in self.subjects:
            for topic in subject.topics:
                topic.mark_complete()
                
        schedule = self.scheduler.create_schedule(start_date=self.start_date)
        self.assertEqual(len(schedule), 0)