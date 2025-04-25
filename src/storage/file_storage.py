import json
from pathlib import Path
from typing import List
from src.models.subject import Subject
from src.models.topic import Topic

class FileStorage:
    """
    A class to handle file storage for subjects and topics.
    
    Attributes:
        file_path (Path): The path to the JSON file where data is stored.
    """

    def __init__(self, file_path: str) -> None:
        """
        Initialize the FileStorage with a given file path.
        
        Args:
            file_path (str): The path to the JSON file for storage.
        """
        self.file_path = Path(file_path)
        self.file_path.parent.mkdir(parents=True, exist_ok=True)  # Ensure directory exists
     
    def save_subjects(self, subjects: List[Subject]) -> None:
        """
        Save a list of subjects to the JSON file.
        
        Args:
            subjects (List[Subject]): The list of subjects to save.
        """
        if not subjects:
            raise ValueError("The list of subjects is empty.")
        try:
            # Validate all subjects before saving
            data = []
            for subject in subjects:
                if not isinstance(subject, Subject):
                    raise ValueError("All items must be instances of Subject.")
                data.append(self._serialize_subject(subject))
            # Write to file
            with self.file_path.open('w', encoding='utf-8') as file:
                json.dump(data, file, indent=2)
                
        except (IOError, TypeError) as e:
            raise FileStorageError(f"Error saving subjects to file: {e}") from e
        except Exception as e:
            raise FileStorageError(f"Error serializing subjects: {e}") from e
        
    def load_subjects(self) -> List[Subject]:
        """
        Load subjects from the JSON file.
        
        Returns:
            List[Subject]: A list of loaded subjects.
        """
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
                    subjects.append(subject)
                except (KeyError, TypeError) as e:
                    raise ValueError(f"Error deserializing subject: {e}") from e
        except (IOError, OSError) as e:
            raise FileStorageError(f"Failed to read file {self.file_path}: {e}") from e
        except json.JSONDecodeError as e:
            raise FileStorageError(f"Failed to decode JSON from file {self.file_path}: {e}") from e
        return subjects
        
    def _serialize_subject(self, subject: Subject) -> dict:
        """
        Serialize a Subject object to a dictionary.
        
        Args:
            subject (Subject): The subject to serialize.
            
        Returns:
            dict: The serialized subject.
        """
        return {
            "name": subject.name,
            "exam_date": subject.exam_date.isoformat(),
            "difficulty": subject.difficulty,
            "topics": [
                {
                    "name": topic.name,
                    "priority": topic.priority,
                    "estimated_hours": topic.estimated_hours,
                    "completed": topic.completed
                }
                for topic in subject.topics
            ]
        }
        
    def _deserialize_subject(self, data: dict) -> Subject:
        """
        Deserialize a dictionary into a Subject object.
        
        Args:
            data (dict): The dictionary to deserialize.
                
        Returns:
            Subject: The deserialized subject.
        """
        subject = Subject(
            name=data["name"],
            exam_date=data["exam_date"],
            difficulty=data["difficulty"]
        )
        for topic_data in data["topics"]:
            topic = Topic(
                name=topic_data["name"],
                priority=topic_data["priority"],
                estimated_hours=topic_data["estimated_hours"],
                completed=topic_data["completed"]
            )
            subject.add_topic(topic)
        subject.update_progress()  # Update progress after adding topics
        return subject
   
class FileStorageError(Exception):
    """Custom exception for file storage errors."""