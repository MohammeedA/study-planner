"""
Module for the Topic class which represents a study topic within a subject.
"""

class Topic:
    """
    Represents a study topic with properties for tracking progress and time management.
    
    Properties:
        name (str): The name of the topic
        priority (int): Priority level from 1-5, where 5 is highest priority
        estimated_hours (float): Estimated hours needed to complete the topic
        completed (bool): Whether the topic has been completed
        hours_spent (float): Actual hours spent studying this topic
    """
    
    def __init__(
        self,
        name: str,
        priority: int = 1,
        estimated_hours: float = 1.0,
        completed: bool = False
    ) -> None:
        """
        Initialize a new Topic instance.
        
        Args:
            name: The name of the topic
            priority: Priority level (1-5), defaults to 1
            estimated_hours: Estimated study hours needed, defaults to 1.0
            completed: Whether the topic is completed, defaults to False
            
        Raises:
            ValueError: If priority is not between 1 and 5
            ValueError: If estimated_hours is negative
        """
        if not 1 <= priority <= 5:
            raise ValueError("Priority must be between 1 and 5")
        if estimated_hours < 0:
            raise ValueError("Estimated hours cannot be negative")
          
        self.name = name
        self.priority = priority
        self.estimated_hours = estimated_hours
        self.completed = completed
        self.hours_spent = 0.0

    def add_hours(self, hours: float) -> None:
        """
        Add study hours to the topic.
        
        Args:
            hours: Number of hours to add
            
        Raises:
            ValueError: If hours is negative
        """
        if hours < 0:
            raise ValueError("Cannot add negative hours")
        self.hours_spent += hours
        if self.hours_spent >= self.estimated_hours:
            self.mark_complete()

    def mark_complete(self) -> None:
        """Mark the topic as completed."""
        self.completed = True
        # Ensure hours_spent matches estimated_hours when marked complete
        self.hours_spent = self.estimated_hours
  
    def get_progress(self) -> float:
        """
        Get the progress percentage for this topic.
        
        Returns:
            float: Progress percentage (0-100)
        """
        if self.completed:
            return 100.0
        return min(100.0, (self.hours_spent / self.estimated_hours) * 100)

    def reset_progress(self) -> None:
        """Reset the topic's progress by clearing completed status and hours spent."""
        self.completed = False
        self.hours_spent = 0.0

    def __str__(self) -> str:
        """
        Return a string representation of the Topic.
        
        Returns:
            A formatted string showing the topic's properties
        """
        status = "✓" if self.completed else "✗"
        progress = self.get_progress()
        return f"Topic: {self.name} [Priority: {self.priority}, Progress: {progress:.1f}%, Hours: {self.hours_spent}/{self.estimated_hours}, {status}]"