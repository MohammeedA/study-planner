from cmd import Cmd
from datetime import date

from src.models.subject import Subject
from src.storage.file_storage import FileStorage, FileStorageError

class CLI(Cmd):
    prompt = 'study-planner> '
    intro = "Welcome to the Study Planner CLI! Type help or ? to list commands."
    
    def __init__(self):
        """Initialize the CLI with an empty subjects list."""
        super().__init__()
        self.subjects = []
        self.storage = FileStorage("data/subjects.json")
    
    def preloop(self):
        """Override preloop to customize the startup message."""
        print("Starting the Study Scheduler...")
        try:
            self.subjects = self.storage.load_subjects()
            print(f"Loaded {len(self.subjects)} subjects.")
        except FileStorageError as e:
            print(f"Error loading subjects: {e}")
        except Exception as e:
            print(f"Unexpected error: {e}")
        print("You can now enter commands.")
        return super().preloop()
    
    def postloop(self):
        """Override postloop to customize the shutdown message."""
        try:
            # Assuming self.subjects contains the subjects data
            self.storage.save_subjects(self.subjects)
            print(f"Saved {len(self.subjects)} subjects.")
        except FileStorageError as e:
            print(f"Error saving subjects: {e}")
        except Exception as e:
            print(f"Unexpected error: {e}")
            
        print("Exiting the Study Scheduler...")
        return super().postloop()

    def do_greet(self, arg):
        """Greet the user."""
        print(f"Hello, {arg}!")
    
    def do_add_subject(self, arg):
        """Add a new subject.
        Usage: add_subject <name> <exam_date> <difficulty>
        Example: add_subject 'Computer Science' 2024-12-31 3
        """
        try:
            # Split the arguments
            args = arg.split(" ")
            if len(args) != 3:
                print("Usage: add_subject <name> <exam_date> <difficulty>")
                print(args)
                return
            name = args[0].strip("'\"")
            exam_date = date(*map(int, args[1].split('-')))
            difficulty = int(args[2])
            if not (1 <= difficulty <= 5):
                print("Difficulty must be between 1 and 5.")
                return
            if exam_date < date.today():
                print("Exam date cannot be in the past.")
                return
            # Create a new subject
            new_subject = Subject(name, exam_date, difficulty)
            self.subjects.append(new_subject)
            print(f"Subject '{name}' added successfully.")
        except ValueError as e:
            print(f"Error adding subject: {e}")
        except Exception as e:
            print(f"Unexpected error: {e}")
    
    def do_list_subjects(self, arg):
        """List all subjects."""
        if not self.subjects:
            print("No subjects found.")
            return
        
        print("\nCurrent Subjects:")
        print("-" * 50)
        for i, subject in enumerate(self.subjects, 1):
            print(f"{i}. {subject.name}")
            print(f"   Exam Date: {subject.exam_date}")
            print(f"   Difficulty: {subject.difficulty}/5")
            print(f"   Topics: {len(subject.topics)}")
            print("-" * 50)
    
    def do_remove_subject(self, arg):
        """Remove a subject."""
        # Example implementation
        print(f"Removing subject: {arg}")
        # Here you would parse the arg and remove the subject from storage

        print(f"Subject '{arg}' removed successfully.")
        # In a real implementation, you would also handle errors and validate input
    
    def do_add_topic(self, arg):
        """Add a new topic to a subject."""
        # Example implementation
        print(f"Adding topic: {arg}")
        # Here you would parse the arg and add the topic to the specified subject

        print(f"Topic '{arg}' added successfully.")
        # In a real implementation, you would also handle errors and validate input
        
    def do_list_topics(self, arg):
        """List all topics for a subject."""
        # Example implementation
        print(f"Listing topics for subject: {arg}")
        # Here you would retrieve the topics from the specified subject and print them
        # For demonstration, we'll just print a placeholder
        print("1. Data Structures\n2. Algorithms\n3. Operating Systems")
    
    def do_remove_topic(self, arg):
        """Remove a topic from a subject."""
        # Example implementation
        print(f"Removing topic: {arg}")
        # Here you would parse the arg and remove the topic from the specified subject

        print(f"Topic '{arg}' removed successfully.")
        # In a real implementation, you would also handle errors and validate input
    
    def do_mark_complete(self, arg):
        """Mark a topic as complete."""
        # Example implementation
        print(f"Marking topic as complete: {arg}")
        # Here you would parse the arg and mark the topic as complete in the specified subject

        print(f"Topic '{arg}' marked as complete.")
        # In a real implementation, you would also handle errors and validate input

    def do_exit(self, arg):
        """Exit the CLI."""
        print("Goodbye!")
        return True

    def default(self, line):
        print(f"Unknown command: {line}")
        print("Type 'help' for a list of commands.")