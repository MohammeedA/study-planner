from datetime import date, timedelta
from pathlib import Path
from src.models.subject import Subject
from src.models.topic import Topic
from src.storage.file_storage import FileStorage
from src.cli.interface import CLI

def generate_test_data():
    # Create subjects with realistic exam dates
    subjects = []
    
    # Computer Science subject
    cs = Subject("Computer Science", date.today() + timedelta(days=60), difficulty=4)
    cs.add_topic(Topic("Data Structures", priority=5, estimated_hours=10))
    cs.topics[0].mark_complete()  # Marking the first topic as complete
    cs.add_topic(Topic("Algorithms", priority=5, estimated_hours=12))
    cs.add_topic(Topic("Operating Systems", priority=3, estimated_hours=8))
    cs.add_topic(Topic("Computer Networks", priority=4, estimated_hours=6))
    subjects.append(cs)
    
    # Mathematics subject
    math = Subject("Mathematics", date.today() + timedelta(days=45), difficulty=5)
    math.add_topic(Topic("Calculus", priority=5, estimated_hours=15))
    math.add_topic(Topic("Linear Algebra", priority=4, estimated_hours=10))
    math.add_topic(Topic("Probability", priority=3, estimated_hours=8))
    subjects.append(math)
    
    # Physics subject
    physics = Subject("Physics", date.today() + timedelta(days=30), difficulty=4)
    physics.add_topic(Topic("Mechanics", priority=5, estimated_hours=10))
    physics.add_topic(Topic("Thermodynamics", priority=4, estimated_hours=8))
    physics.topics[1].mark_complete()  # Marking the second topic as complete
    physics.add_topic(Topic("Electromagnetism", priority=4, estimated_hours=12))
    subjects.append(physics)
    
    # Create storage directory
    storage_dir = Path("data")
    storage_dir.mkdir(exist_ok=True)
    
    # Save the test data
    storage = FileStorage(storage_dir / "subjects.json")
    storage.save_subjects(subjects)
    print(f"Generated test data for {len(subjects)} subjects with {sum(len(s.topics) for s in subjects)} topics")
    return storage

def main():
    # Uncomment the line below to generate test data
    # generate_test_data()
    
    # Initialize storage
    storage_instance = FileStorage(Path("data/subjects.json"))
    
    # Load and verify the data
    loaded_subjects = storage_instance.load_subjects()
    print("\nLoaded Subjects:")
    for subject in loaded_subjects:
        print(f"\n{subject}")
        for topic in subject.topics:
            print(f"  - {topic}")

    cli = CLI()
    cli.subjects = loaded_subjects
    cli.cmdloop()

if __name__ == "__main__":
    main()