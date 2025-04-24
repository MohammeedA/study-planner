"""
Module for the Subject class which represents a study subject.
"""

from datetime import date
from .topic import Topic

class Subject:
    """
    Represents a study subject with properties for tracking progress and time management.
    
    Properties:
        name (str): The name of the subject
        difficulty (int): difficulty level from 1-5, where 5 is highest difficulty
        estimated_hours (float): Estimated hours needed to complete the subject
        completed (bool): Whether the subject has been completed
    """

    def __init__(
        self,
        name: str,
        exam_date: date,
        difficulty: int = 1
    ) -> None:
        """
        Initialize a new Subject instance.

        Args:
            name (str): The name of the subject
            exam_date (datetime.date): The date of the exam
            difficulty (int, optional): The difficulty level from 1 to 5. Defaults to 1.

        Raises:
            ValueError: If difficulty is not between 1 and 5
            ValueError: If exam_date is in the past
        """
        if not 1 <= difficulty <= 5:
            raise ValueError("Difficulty must be between 1 and 5")
        if exam_date < date.today():
            raise ValueError("Exam date cannot be in the past")
        self.name = name
        self.exam_date = exam_date
        self.difficulty = difficulty
        self.progress = 0.0
        self.topics = []  # List of topics associated with the subject
    
    def add_topic(self, topic) -> None:
        """
        Add a topic to the subject.

        Args:
            topic: The topic to be added
        
        Raises:
            ValueError: If the topic is not an instance of the Topic class
        """
        if not isinstance(topic, Topic):
            raise ValueError("The topic must be an instance of the Topic class")
        self.topics.append(topic)
    
    def remove_topic(self, topic) -> None:
        """
        Remove a topic from the subject.

        Args:
            topic: The topic to be removed
        
        Raises:
            ValueError: If the topic is not found in the subject
        """
        try:
            self.topics.remove(topic)
        except ValueError as exc:
            raise ValueError("The topic is not found in the subject") from exc
    
    def update_progress(self) -> None:
        """
        Update the progress of the subject based on the completion of its topics.
        """
        if not self.topics:
            self.progress = 0.0
            return
        
        completed_topics = sum(1 for topic in self.topics if topic.completed)
        self.progress = (completed_topics / len(self.topics)) * 100
    
    def __str__(self) -> str:
        """
        Return a string representation of the Subject.

        Returns:
            A formatted string showing the subject's properties
        """
        status = "✓" if self.progress == 100 else "✗"
        return f"Subject: {self.name} [Difficulty: {self.difficulty}, Progress: {self.progress:.2f}%, Status: {status}]"