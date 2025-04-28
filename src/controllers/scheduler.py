"""
Module for scheduling study sessions based on subjects, topics, and time constraints.
"""

from datetime import date, datetime, timedelta
from typing import List, Dict, Any
from src.models.subject import Subject
from src.models.topic import Topic

class Scheduler:
    """
    A simple scheduler that creates study plans based on subjects and their topics.
    Takes into account:
    - Exam dates
    - Topic priorities
    - Estimated study hours
    - Subject difficulties
    """
    
    def __init__(self, subjects: List[Subject]):
        """
        Initialize the scheduler with a list of subjects.
        
        Args:
            subjects: List of Subject objects to schedule
        """
        self.subjects = subjects
        
    def create_schedule(self, start_date: date = None, hours_per_day: float = 4.0) -> List[Dict[str, Any]]:
        """
        Create a daily study schedule based on subjects and topics.
        
        Args:
            start_date: The date to start the schedule from (defaults to today)
            hours_per_day: Maximum study hours per day (default 4.0)
            
        Returns:
            A list of daily schedules with assigned topics
        """
        if start_date is None:
            start_date = date.today()
            
        # Sort subjects by exam date
        sorted_subjects = sorted(self.subjects, key=lambda x: x.exam_date)
        
        schedule = []
        current_date = start_date
        
        while sorted_subjects:
            # Remove subjects with passed exam dates
            sorted_subjects = [s for s in sorted_subjects if s.exam_date > current_date]
            if not sorted_subjects:
                break
                
            daily_hours = hours_per_day
            day_schedule = {
                "date": current_date,
                "topics": []
            }
            
            # Prioritize subjects closer to exam date
            for subject in sorted_subjects:
                if daily_hours <= 0:
                    break
                    
                # Get incomplete topics for this subject
                incomplete_topics = [
                    t for t in subject.topics 
                    if not t.completed
                ]
                
                if not incomplete_topics:
                    continue
                    
                # Sort topics by priority (highest first)
                sorted_topics = sorted(
                    incomplete_topics,
                    key=lambda t: t.priority,
                    reverse=True
                )
                
                # Calculate time allocation based on days until exam
                days_until_exam = (subject.exam_date - current_date).days
                if days_until_exam <= 0:
                    continue
                    
                # Allocate time based on subject difficulty and topic priority
                for topic in sorted_topics:
                    if daily_hours <= 0:
                        break
                        
                    # Calculate study time for this topic
                    suggested_hours = min(
                        daily_hours,
                        topic.estimated_hours / days_until_exam * subject.difficulty/3
                    )
                    
                    if suggested_hours > 0:
                        day_schedule["topics"].append({
                            "subject": subject.name,
                            "topic": topic.name,
                            "hours": round(suggested_hours, 1),
                            "priority": topic.priority
                        })
                        daily_hours -= suggested_hours
            
            if day_schedule["topics"]:
                schedule.append(day_schedule)
            current_date += timedelta(days=1)
            
        return schedule
    
    def get_next_days_schedule(self, days: int = 7) -> List[Dict[str, Any]]:
        """
        Get the schedule for the next specified number of days.
        
        Args:
            days: Number of days to schedule (default 7)
            
        Returns:
            A list of daily schedules for the specified period
        """
        schedule = self.create_schedule()
        return schedule[:days]