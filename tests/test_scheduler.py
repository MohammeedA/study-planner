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
        
    def test_sequential_topic_scheduling(self):
        """Test that topics are scheduled in sequential order."""
        schedule = self.scheduler.create_schedule(start_date=self.start_date)
        
        # Track which topics have been scheduled for each subject
        math_topics_seen = set()
        physics_topics_seen = set()
        
        for day in schedule:
            for topic in day["topics"]:
                if topic["subject"] == "Mathematics":
                    math_topics_seen.add(topic["topic"])
                    # Should not see Algebra until Calculus is complete
                    if "Algebra" in math_topics_seen:
                        self.assertIn("Calculus", math_topics_seen)
                elif topic["subject"] == "Physics":
                    physics_topics_seen.add(topic["topic"])
                    # Should not see Thermodynamics until Mechanics is complete
                    if "Thermodynamics" in physics_topics_seen:
                        self.assertIn("Mechanics", physics_topics_seen)
                        
    def test_hours_tracking(self):
        """Test that hours are tracked and topics are completed appropriately."""
        schedule = self.scheduler.create_schedule(start_date=self.start_date)
        
        # Calculate total scheduled hours for first topic of each subject
        math_hours = sum(
            t["hours"] for day in schedule 
            for t in day["topics"] 
            if t["subject"] == "Mathematics" and t["topic"] == "Calculus"
        )
        physics_hours = sum(
            t["hours"] for day in schedule 
            for t in day["topics"] 
            if t["subject"] == "Physics" and t["topic"] == "Mechanics"
        )
        
        # Check that scheduled hours match or exceed estimated hours
        self.assertGreaterEqual(math_hours, 10)  # Calculus estimated hours
        self.assertGreaterEqual(physics_hours, 6)  # Mechanics estimated hours
        
    def test_topic_completion(self):
        """Test that topics are marked complete when all hours are scheduled."""
        schedule = self.scheduler.create_schedule(start_date=self.start_date)
        
        # Simulate studying according to schedule
        for day in schedule:
            for topic_schedule in day["topics"]:
                subject = next(s for s in self.subjects if s.name == topic_schedule["subject"])
                topic = next(t for t in subject.topics if t.name == topic_schedule["topic"])
                if not topic.completed:
                    topic.add_hours(topic_schedule["hours"])
                    
        # Check that first topics are completed before second topics appear
        math_first_topic = self.math.topics[0]
        physics_first_topic = self.physics.topics[0]
        
        self.assertTrue(
            math_first_topic.completed or 
            math_first_topic.hours_spent == math_first_topic.estimated_hours
        )
        self.assertTrue(
            physics_first_topic.completed or 
            physics_first_topic.hours_spent == physics_first_topic.estimated_hours
        )
                
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
                self.assertIn("is_current", topic)
                
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