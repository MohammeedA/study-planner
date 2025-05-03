from datetime import date
import json
from pathlib import Path
from typing import List
from src.models.subject import Subject
from src.models.topic import Topic

class FileStorageError(Exception):
    """Custom exception for file storage errors."""

class FileStorage:
    def __init__(self, file_path: str) -> None:
        self.file_path = Path(file_path)
        self.file_path.parent.mkdir(parents=True, exist_ok=True)
     
    def save_subjects(self, subjects: List[Subject]) -> None:
        if not subjects:
            with self.file_path.open('w', encoding='utf-8') as file:
                json.dump([], file, indent=2)
            #raise ValueError("The list of subjects is empty.")
        try:
            data = []
            for subject in subjects:
                if not isinstance(subject, Subject):
                    raise ValueError("All items must be instances of Subject.")
                data.append(self._serialize_subject(subject))
                
            with self.file_path.open('w', encoding='utf-8') as file:
                json.dump(data, file, indent=2)
                
        except (IOError, TypeError) as e:
            raise FileStorageError(f"Error saving subjects to file: {e}") from e
        except Exception as e:
            raise FileStorageError(f"Error serializing subjects: {e}") from e
        
    def load_subjects(self) -> List[Subject]:
        if not self.file_path.exists():
            return []
            
        try:
            with self.file_path.open('r', encoding='utf-8') as file:
                data = json.load(file)
            
            if not isinstance(data, list):
                raise ValueError("Invalid JSON format: Expected a list.")
            
            subjects = []
            for item in data:
                try:
                    subject = self._deserialize_subject(item)
                    subject.update_progress()
                    subjects.append(subject)
                except (KeyError, TypeError) as e:
                    raise ValueError(f"Error deserializing subject: {e}") from e
                    
            return subjects
            
        except json.JSONDecodeError as e:
            if not self.file_path.stat().st_size:
                return []
            raise FileStorageError(f"Failed to decode JSON from file {self.file_path}: {e}") from e
        except (IOError, OSError) as e:
            raise FileStorageError(f"Failed to read file {self.file_path}: {e}") from e
        
    def _serialize_subject(self, subject: Subject) -> dict:
        if not isinstance(subject, Subject):
            raise ValueError("Input must be a Subject instance")
            
        return {
            "name": subject.name,
            "exam_date": subject.exam_date.isoformat(),
            "difficulty": subject.difficulty,
            "topics": [
                {
                    "name": topic.name,
                    "priority": topic.priority,
                    "estimated_hours": topic.estimated_hours,
                    "completed": topic.completed,
                    "hours_spent": topic.hours_spent
                }
                for topic in subject.topics
            ]
        }
        
    def _deserialize_subject(self, data: dict) -> Subject:
        required_fields = {"name", "exam_date", "difficulty", "topics"}
        if not all(field in data for field in required_fields):
            missing = required_fields - set(data.keys())
            raise ValueError(f"Missing required fields: {missing}")
            
        try:
            exam_date = date.fromisoformat(data["exam_date"])
            
            subject = Subject(
                name=data["name"],
                exam_date=exam_date,
                difficulty=data["difficulty"]
            )
            
            for topic_data in data["topics"]:
                if not isinstance(topic_data, dict):
                    raise ValueError(f"Invalid topic data format: {topic_data}")
                    
                required_topic_fields = {"name", "priority", "estimated_hours", "completed"}
                if not all(field in topic_data for field in required_topic_fields):
                    missing = required_topic_fields - set(topic_data.keys())
                    raise ValueError(f"Missing required topic fields: {missing}")
                    
                topic = Topic(
                    name=topic_data["name"],
                    priority=topic_data["priority"],
                    estimated_hours=topic_data["estimated_hours"]
                )
                # Restore hours spent from saved data
                if "hours_spent" in topic_data:
                    topic.hours_spent = topic_data["hours_spent"]
                if topic_data["completed"]:
                    topic.mark_complete()
                subject.add_topic(topic)
                
            return subject
            
        except (KeyError, TypeError, ValueError) as e:
            raise ValueError(f"Invalid subject data: {e}") from e