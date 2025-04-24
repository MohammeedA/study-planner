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

    def mark_complete(self) -> None:
        """Mark the topic as completed."""
        self.completed = True
  
    def __str__(self) -> str:
        """
        Return a string representation of the Topic.
        
        Returns:
            A formatted string showing the topic's properties
        """
        status = "✓" if self.completed else "✗"
        return f"Topic: {self.name} [Priority: {self.priority}, Hours: {self.estimated_hours}, {status}]"