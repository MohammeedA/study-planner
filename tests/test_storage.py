from datetime import date
import os
import tempfile
import pytest

from src.models.subject import Subject
from src.models.topic import Topic
from src.storage.file_storage import FileStorage, FileStorageError

# pylint: disable=protected-access

@pytest.fixture(name="temp_file")
def fixture_temp_json_file():
    """Create a temporary JSON file for testing."""
    with tempfile.NamedTemporaryFile(suffix='.json', delete=False) as f:
        yield f.name
    os.unlink(f.name)

@pytest.fixture(name="test_subject")
def fixture_sample_subject():
    """Create a sample subject with topics for testing."""
    subject = Subject(
        name="Mathematics",
        exam_date=date(2025, 12, 31),  # Using end of year to avoid date conflicts
        difficulty=4
    )
    topic1 = Topic(name="Calculus", priority=5, estimated_hours=10)
    topic2 = Topic(name="Algebra", priority=3, estimated_hours=8)
    topic2.mark_complete()
    subject.add_topic(topic1)
    subject.add_topic(topic2)
    return subject

class TestFileStorage:
    def test_init_creates_directory(self, temp_file):
        """Test that initialization creates the parent directory."""
        storage = FileStorage(temp_file)
        assert storage.file_path.parent.exists()

    def test_save_and_load_subjects(self, temp_file, test_subject):
        """Test saving and loading subjects works correctly."""
        storage = FileStorage(temp_file)
        storage.save_subjects([test_subject])
        
        loaded_subjects = storage.load_subjects()
        assert len(loaded_subjects) == 1
        loaded_subject = loaded_subjects[0]
        
        assert loaded_subject.name == test_subject.name
        assert loaded_subject.difficulty == test_subject.difficulty
        assert len(loaded_subject.topics) == len(test_subject.topics)

    def test_save_empty_subjects_list(self, temp_file):
        """Test that saving an empty subjects list works."""
        storage = FileStorage(temp_file)
        storage.save_subjects([])  # Should save an empty list without error
        loaded = storage.load_subjects()
        assert loaded == []  # Should load back as empty list

    def test_load_nonexistent_file(self, temp_file):
        """Test loading from a non-existent file returns empty list."""
        storage = FileStorage(temp_file)
        assert storage.load_subjects() == []

    def test_save_invalid_subject(self, temp_file):
        """Test saving invalid subject data raises FileStorageError."""
        storage = FileStorage(temp_file)
        with pytest.raises(FileStorageError, match="Error serializing subjects"):
            storage.save_subjects([{"invalid": "data"}])

    def test_load_corrupted_json(self, temp_file):
        """Test loading corrupted JSON raises FileStorageError."""
        with open(temp_file, 'w', encoding='utf-8') as f:
            f.write("invalid json content")
            
        storage = FileStorage(temp_file)
        with pytest.raises(FileStorageError):
            storage.load_subjects()

    def test_hours_spent_persistence(self, temp_file, test_subject):
        """Test that hours_spent is saved and loaded correctly."""
        storage = FileStorage(temp_file)
        
        # Add some hours to a topic
        test_subject.topics[0].add_hours(2.5)
        storage.save_subjects([test_subject])
        
        # Load and verify hours are preserved
        loaded_subjects = storage.load_subjects()
        loaded_topic = loaded_subjects[0].topics[0]
        assert loaded_topic.hours_spent == 2.5

    def test_serialize_subject(self, test_subject):
        """Test subject serialization."""
        storage = FileStorage("test.json")
        serialized = storage._serialize_subject(test_subject)
        
        assert isinstance(serialized, dict)
        assert all(key in serialized for key in ["name", "exam_date", "difficulty", "topics"])
        assert len(serialized["topics"]) == len(test_subject.topics)

    def test_deserialize_subject(self, test_subject):
        """Test subject deserialization."""
        storage = FileStorage("test.json")
        serialized = storage._serialize_subject(test_subject)
        deserialized = storage._deserialize_subject(serialized)
        
        assert isinstance(deserialized, Subject)
        assert deserialized.name == test_subject.name
        assert deserialized.difficulty == test_subject.difficulty
        assert len(deserialized.topics) == len(test_subject.topics)

    def test_deserialize_invalid_data(self):
        """Test deserializing invalid data raises ValueError."""
        storage = FileStorage("test.json")
        invalid_data = {"name": "Test"}  # Missing required fields
        
        with pytest.raises(ValueError):
            storage._deserialize_subject(invalid_data)

    def test_file_permission_error(self, temp_file, test_subject):
        """Test handling of file permission errors."""
        storage = FileStorage(temp_file)
        os.chmod(temp_file, 0o444)  # Make file read-only
        
        with pytest.raises(FileStorageError):
            storage.save_subjects([test_subject])