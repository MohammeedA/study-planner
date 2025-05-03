"""
Module for scheduling study sessions based on subjects, topics, and time constraints.
"""

from datetime import date, timedelta
from typing import List, Dict, Any
from src.models.subject import Subject

class Scheduler:
    """
    A scheduler that creates study plans based on subjects and their topics.
    Topics are scheduled sequentially - a topic must be completed before moving to the next.
    """
    
    def __init__(self, subjects: List[Subject]):
        """Initialize the scheduler with a list of subjects."""
        self.subjects = subjects
        
    def create_schedule(self, start_date: date = None, hours_per_day: float = 4.0) -> List[Dict[str, Any]]:
        if start_date is None:
            start_date = date.today()
            
        topic_scheduled_hours = {}  # (subject_name, topic_name) -> hours_scheduled
        schedule = []
        current_date = start_date
        active_subjects = sorted(self.subjects, key=lambda x: x.exam_date)
        
        max_days = 365  # Maximum number of days to prevent infinite loop
        days_processed = 0
        
        while active_subjects and days_processed < max_days:
            # Remove subjects with passed exam dates
            active_subjects = [s for s in active_subjects if s.exam_date > current_date]
            if not active_subjects:
                break
                
            daily_hours_remaining = hours_per_day
            day_schedule = {
                "date": current_date,
                "topics": []
            }
            
            # First pass: Get list of subjects with their first incomplete topic
            subjects_with_topics = []
            for subject in active_subjects:
                days_until_exam = (subject.exam_date - current_date).days
                if days_until_exam <= 0:
                    continue
                
                # Find first incomplete topic for this subject
                for topic in subject.topics:
                    topic_key = (subject.name, topic.name)
                    hours_already_scheduled = topic_scheduled_hours.get(topic_key, 0)
                    remaining_hours = topic.estimated_hours
                    if hasattr(topic, 'hours_spent'):
                        remaining_hours -= topic.hours_spent
                    remaining_hours -= hours_already_scheduled
                    
                    if not topic.completed and remaining_hours > 0:
                        urgency = (1.0 / max(1, days_until_exam)) * (1 + topic.priority / 5)
                        priority_score = urgency * (topic.priority / 3.0) * (subject.difficulty / 3.0)
                        
                        subjects_with_topics.append({
                            'subject': subject,
                            'topic': topic,
                            'score': priority_score,
                            'remaining_hours': remaining_hours,
                            'topic_key': topic_key,
                            'hours_scheduled': hours_already_scheduled,
                            'days_until_exam': days_until_exam
                        })
                        break  # Only take first incomplete topic
            
            if not subjects_with_topics:
                break
                
            # Sort by priority score
            subjects_with_topics.sort(key=lambda x: x['score'], reverse=True)
            
            # Schedule topics while we have hours remaining
            while daily_hours_remaining > 0 and subjects_with_topics:
                # Take the highest priority topic
                topic_data = subjects_with_topics[0]
                subject = topic_data['subject']
                topic = topic_data['topic']
                remaining_topic_hours = topic_data['remaining_hours']
                
                # Calculate minimum hours needed to maintain progress
                min_daily_hours = remaining_topic_hours / max(topic_data['days_until_exam'], 1)
                
                # Calculate suggested hours - try to allocate larger chunks
                suggested_hours = min(
                    daily_hours_remaining,  # Don't exceed remaining daily hours
                    max(
                        min_daily_hours,  # At least the minimum required
                        min(
                            remaining_topic_hours,  # Don't exceed topic's remaining hours
                            max(2.0, daily_hours_remaining / (len(subjects_with_topics) or 1))  # Try for at least 2-hour blocks
                        )
                    )
                )
                
                if suggested_hours > 0:
                    day_schedule["topics"].append({
                        "subject": subject.name,
                        "topic": topic.name,
                        "hours": round(suggested_hours, 1),
                        "priority": topic.priority,
                        "is_current": True,
                        "remaining_hours": round(remaining_topic_hours - suggested_hours, 1)
                    })
                    
                    daily_hours_remaining -= suggested_hours
                    topic_key = topic_data['topic_key']
                    topic_scheduled_hours[topic_key] = topic_data['hours_scheduled'] + suggested_hours
                    
                    # If topic is complete, remove it from the list
                    if topic_scheduled_hours[topic_key] >= topic.estimated_hours:
                        subjects_with_topics.pop(0)
                    # Otherwise update remaining hours
                    else:
                        subjects_with_topics[0]['remaining_hours'] -= suggested_hours
                        subjects_with_topics[0]['hours_scheduled'] += suggested_hours
                else:
                    break
            
            if day_schedule["topics"]:
                schedule.append(day_schedule)
            
            current_date += timedelta(days=1)
            days_processed += 1
            
            # Update active subjects
            active_subjects = [
                s for s in active_subjects
                if any(
                    not t.completed and 
                    (t.estimated_hours - topic_scheduled_hours.get((s.name, t.name), 0) - 
                     (t.hours_spent if hasattr(t, 'hours_spent') else 0)) > 0
                    for t in s.topics
                )
            ]
        
        return schedule
    
    def get_next_days_schedule(self, days: int = 7) -> List[Dict[str, Any]]:
        """Get the schedule for the next specified number of days."""
        schedule = self.create_schedule()
        return schedule[:days]