from cmd import Cmd
from datetime import date
import shlex

from src.models.subject import Subject
from src.storage.file_storage import FileStorage, FileStorageError

class CLI(Cmd):
    prompt = 'study-planner> '
    intro = "Welcome to the Study Planner CLI! Type help or ? to list commands."
    
    def __init__(self, interactive=False):
        """Initialize the CLI with an empty subjects list."""
        super().__init__()
        self.subjects = []
        self.storage = FileStorage("data/subjects.json")
        self.interactive = interactive
    
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
        Or use: add_subject -i for interactive mode
        """
        if arg.strip() == "-i" or self.interactive:
            return self._add_subject_interactive()
        
        try:
            # Parse input handling quoted strings and whitespace
            args = shlex.split(arg)
            
            if len(args) != 3:
                print("Usage: add_subject <name> <exam_date> <difficulty>")
                print("Example: add_subject 'Computer Science' 2024-12-31 3")
                return

            name = args[0]
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

    def _add_subject_interactive(self):
        """Interactive mode for adding subjects"""
        try:
            # Get subject name
            name = input("Enter subject name: ").strip()
            if not name:
                print("Error: Subject name cannot be empty")
                return

            # Get exam date
            while True:
                date_str = input("Enter exam date (YYYY-MM-DD): ").strip()
                try:
                    exam_date = date(*map(int, date_str.split('-')))
                    if exam_date < date.today():
                        print("Error: Exam date cannot be in the past")
                        continue
                    break
                except ValueError:
                    print("Error: Invalid date format. Please use YYYY-MM-DD")

            # Get difficulty
            while True:
                try:
                    difficulty = int(input("Enter difficulty (1-5): ").strip())
                    if not (1 <= difficulty <= 5):
                        print("Error: Difficulty must be between 1 and 5")
                        continue
                    break
                except ValueError:
                    print("Error: Please enter a number between 1 and 5")

            # Create and add the new subject
            new_subject = Subject(name, exam_date, difficulty)
            self.subjects.append(new_subject)
            print(f"\nSubject '{name}' added successfully!")
            
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
            print(f"   Progress: {subject.progress:.2f}%")
            print("-" * 50)
    
    def do_remove_subject(self, arg):
        """Remove a subject."""
        self.do_list_subjects("")
        print("Enter the number of the subject to remove:")
        try:
            while True:
                choice = input("Choice: ").strip()
                if choice.isdigit() and 1 <= int(choice) <= len(self.subjects):
                    index = int(choice) - 1
                    removed_subject = self.subjects.pop(index)
                    print(f"Removed subject: {removed_subject.name}")
                    break
                else:
                    print("Invalid choice. Please enter a valid number.")
        except IndexError:
            print("Error: Subject not found. Please try again.")
        except Exception as e:
            print(f"Unexpected error: {e}")
    
    def do_add_topic(self, arg):
        """Add a new topic to a subject."""
        # Example implementation
        print(f"Adding topic: {arg}")
        # Here you would parse the arg and add the topic to the specified subject

        print(f"Topic '{arg}' added successfully.")
        # In a real implementation, you would also handle errors and validate input
        
    def do_list_topics(self, arg):
        """List all topics for a subject."""
        try:
            while True:
                self.do_list_subjects("")
                choice = input("Enter the subject number to list topics: ").strip()
                if choice.isdigit() and 1 <= int(choice) <= len(self.subjects):
                    index = int(choice) - 1
                    subject = self.subjects[index]
                    print(f"Topics in '{subject.name}':")
                    for i, topic in enumerate(subject.topics, 1):
                        print(f"{i}. {topic.name} [Priority: {topic.priority}, Hours: {topic.estimated_hours}, Completed: {'✓' if topic.completed else '✗'}]")
                    print("-" * 50)
                    break
                else:
                    print("Invalid choice. Please enter a valid number.")
        except IndexError:
            print("Error: Subject not found. Please try again.")
        except Exception as e:
            print(f"Unexpected error: {e}")
    
    def do_remove_topic(self, arg):
        """Remove a topic from a subject."""
        try:
            subject = None
            self.do_list_subjects("")
            while True:
                choice = input("Enter the subject number to remove a topic from: ").strip()
                if choice.isdigit() and 1 <= int(choice) <= len(self.subjects):
                    index_s = int(choice) - 1
                    subject = self.subjects[index_s]
                    break
                else:
                    print("Invalid choice. Please enter a valid number.")
            print(f"Topics in '{subject.name}':")
            for i, topic in enumerate(subject.topics, 1):
                print(f"{i}. {topic.name}")
            while True:
                choice = input("Enter the number of the topic to remove: ").strip()
                if choice.isdigit() and 1 <= int(choice) <= len(subject.topics):
                    index_t = int(choice) - 1
                    removed_topic = subject.topics.pop(index_t)
                    print(f"Removed topic: {removed_topic.name}")
                    subject.update_progress()
                    break
                else:
                    print("Invalid choice. Please enter a valid number.")
        except IndexError:
            print("Error: Topic not found. Please try again.")
        except Exception as e:
            print(f"Unexpected error: {e}")
    
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

    def do_EOF(self, arg):
        """Exit on EOF character (Ctrl+D on Mac/Linux, Ctrl+Z on Windows)."""
        print("\nGoodbye!")
        return True

    def default(self, line):
        print(f"Unknown command: {line}")
        print("Type 'help' for a list of commands.")