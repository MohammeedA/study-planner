from cmd import Cmd
from datetime import date
import shlex

from src.models.subject import Subject
from src.models.topic import Topic
from src.storage.file_storage import FileStorage, FileStorageError
from src.controllers.scheduler import Scheduler

class CLI(Cmd):
    prompt = 'study-planner> '
    intro = "Welcome to the Study Planner CLI! Type help or ? to list commands."
    
    def __init__(self, interactive=False):
        """Initialize the CLI with an empty subjects list."""
        super().__init__()
        self.subjects = []
        self.storage = FileStorage("data/subjects.json")
        self.interactive = interactive
        self.scheduler = None

    def preloop(self):
        """Override preloop to customize the startup message."""
        print("Starting the Study Scheduler...")
        try:
            self.subjects = self.storage.load_subjects()
            self.scheduler = Scheduler(self.subjects)
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
            if not self.subjects:
                print("No subjects to save.")
                self.storage.save_subjects([])
                print("Saved an empty list of subjects.")
                return
            # Assuming self.subjects contains the subjects data
            self.storage.save_subjects(self.subjects)
            print(f"Saved {len(self.subjects)} subjects.")
        except FileStorageError as e:
            print(f"Error saving subjects: {e}")
        except Exception as e:
            print(f"Unexpected error: {e}")
            
        print("Exiting the Study Scheduler...")
        return super().postloop()

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
        try:
            if arg.strip() == "-i" or self.interactive:
                return self._add_topic_interactive()
            # Parse input handling quoted strings and whitespace
            args = shlex.split(arg)
            if len(args) != 4:
                print("Usage: add_topic <subject_number> <name> <priority> <estimated_hours>")
                print("Example: add_topic 1 'Data Structures' 3 5.0")
                return
            subject_index = int(args[0]) - 1
            name = args[1]
            priority = int(args[2])
            estimated_hours = float(args[3])
            if not (1 <= priority <= 5):
                print("Priority must be between 1 and 5.")
                return
            if estimated_hours <= 0:
                print("Estimated hours must be greater than 0.")
                return
            if subject_index < 0 or subject_index >= len(self.subjects):
                print("Invalid subject number.")
                return
            subject = self.subjects[subject_index]
            new_topic = Topic(name, priority, estimated_hours)
            subject.topics.append(new_topic)
            print(f"Topic '{name}' added successfully to '{subject.name}'.")
            subject.update_progress()
        except IndexError:
            print("Error: Subject not found. Please try again.")
        except TypeError:
            print("Error: Invalid input type. Please check your inputs.")
        except ValueError as e:
            print(f"Error adding topic: {e}")
        except Exception as e:
            print(f"Unexpected error: {e}")
            
    def _add_topic_interactive(self):
        while True:
            self.do_list_subjects("")
            choice = input("Enter the subject number to add a topic to: ").strip()
            if choice.isdigit() and 1 <= int(choice) <= len(self.subjects):
                index = int(choice) - 1
                subject = self.subjects[index]
                print(f"Adding topic to '{subject.name}'...")
                print("-" * 50)
                print(f"Current Topics in '{subject.name}':")
                for i, topic in enumerate(subject.topics, 1):
                    print(f"{i}. {topic.name} [Priority: {topic.priority}, Hours: {topic.estimated_hours}, Completed: {'✓' if topic.completed else '✗'}]")
                print("-" * 50)
            else:
                print("Invalid choice. Please enter a valid number.")
            name = input("Enter topic name: ").strip()
            if not name:
                print("Error: Topic name cannot be empty")
                return
            priority = int(input("Enter topic priority (1-5): ").strip())
            if not (1 <= priority <= 5):
                print("Error: Priority must be between 1 and 5")
                return
            estimated_hours = float(input("Enter estimated hours: ").strip())
            if estimated_hours <= 0:
                print("Error: Estimated hours must be greater than 0")
                return
            
            new_topic = Topic(name, priority, estimated_hours)
            subject.topics.append(new_topic)
            print(f"Topic '{name}' added successfully to '{subject.name}'.")
            subject.update_progress()
            break
            
        
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
                        print(f"{i}. {topic.name} [Priority: {topic.priority}, Hours: {topic.hours_spent}/{topic.estimated_hours}, Progress: {topic.get_progress():.1f}%, Completed: {'✓' if topic.completed else '✗'}]")
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
                    break
                else:
                    print("Invalid choice. Please enter a valid number.")
            while True:
                choice = input("Enter the number of the topic to mark as complete: ").strip()
                if choice.isdigit() and 1 <= int(choice) <= len(subject.topics):
                    index_t = int(choice) - 1
                    topic = subject.topics[index_t]
                    topic.mark_complete()
                    print(f"Marked topic '{topic.name}' as complete.")
                    subject.update_progress()
                    break
                else:
                    print("Invalid choice. Please enter a valid number.")
        except IndexError:
            print("Error: Topic not found. Please try again.")
        except Exception as e:
            print(f"Unexpected error: {e}")

    def do_reset_topic(self, arg):
        """Reset progress for a specific topic."""
        try:
            while True:
                self.do_list_subjects("")
                choice = input("Enter the subject number to list topics: ").strip()
                if choice.isdigit() and 1 <= int(choice) <= len(self.subjects):
                    index = int(choice) - 1
                    subject = self.subjects[index]
                    print(f"Topics in '{subject.name}':")
                    for i, topic in enumerate(subject.topics, 1):
                        print(f"{i}. {topic}")
                    break
                else:
                    print("Invalid choice. Please enter a valid number.")
            while True:
                choice = input("Enter the number of the topic to reset: ").strip()
                if choice.isdigit() and 1 <= int(choice) <= len(subject.topics):
                    index_t = int(choice) - 1
                    topic = subject.topics[index_t]
                    topic.reset_progress()
                    print(f"Reset progress for topic '{topic.name}'.")
                    subject.update_progress()
                    break
                else:
                    print("Invalid choice. Please enter a valid number.")
        except IndexError:
            print("Error: Topic not found. Please try again.")
        except Exception as e:
            print(f"Unexpected error: {e}")

    def do_reset_subject(self, arg):
        """Reset progress for all topics in a subject."""
        try:
            while True:
                self.do_list_subjects("")
                choice = input("Enter the subject number to reset all topics: ").strip()
                if choice.isdigit() and 1 <= int(choice) <= len(self.subjects):
                    index = int(choice) - 1
                    subject = self.subjects[index]
                    confirm = input(f"Are you sure you want to reset all topics in '{subject.name}'? (y/n): ").lower()
                    if confirm == 'y':
                        subject.reset_progress()
                        print(f"Reset progress for all topics in '{subject.name}'.")
                    else:
                        print("Operation cancelled.")
                    break
                else:
                    print("Invalid choice. Please enter a valid number.")
        except IndexError:
            print("Error: Subject not found. Please try again.")
        except Exception as e:
            print(f"Unexpected error: {e}")

    def do_view_schedule(self, arg):
        """View study schedule for the next N days.
        Usage: view_schedule [days]
        Example: view_schedule 7
        Default is 7 days if no argument is provided.
        """
        try:
            days = 7  # default value
            if arg.strip():
                days = int(arg)
                if days <= 0:
                    print("Number of days must be positive.")
                    return

            if not self.subjects:
                print("No subjects found. Add some subjects first.")
                return

            schedule = self.scheduler.get_next_days_schedule(days)
            
            if not schedule:
                print("No study activities scheduled for this period.")
                return

            print(f"\nStudy Schedule for the Next {days} Days:")
            print("-" * 60)
            
            for day in schedule:
                date_str = day["date"].strftime("%A, %B %d, %Y")
                print(f"\n{date_str}")
                print("-" * 40)
                
                total_hours = sum(topic["hours"] for topic in day["topics"])
                
                for topic in day["topics"]:
                    print(f"• {topic['subject']} - {topic['topic']}")
                    print(f"  Hours: {topic['hours']:.1f}, Priority: {topic['priority']}, Remaining after today: {topic['remaining_hours']:.1f}")
                
                print(f"\nTotal study hours for {day['date']}: {total_hours:.1f}")
                print("-" * 40)

        except ValueError:
            print("Please enter a valid number of days.")
        except Exception as e:
            print(f"Error displaying schedule: {e}")

    def do_daily_schedule(self, arg):
        """View today's study schedule.
        Usage: daily_schedule
        """
        try:
            if not self.subjects:
                print("No subjects found. Add some subjects first.")
                return

            schedule = self.scheduler.create_schedule()
            
            if not schedule:
                print("No study activities scheduled for today.")
                return

            today = date.today()
            today_schedule = next((day for day in schedule if day["date"] == today), None)
            
            if not today_schedule:
                print("No study activities scheduled for today.")
                return

            print("\nToday's Study Schedule:")
            print("-" * 40)
            
            total_hours = sum(topic["hours"] for topic in today_schedule["topics"])
            
            for i, topic in enumerate(today_schedule["topics"], 1):
                print(f"\n{i}. {topic['subject']} - {topic['topic']}")
                print(f"  Suggested Hours: {topic['hours']:.1f}, Priority: {topic['priority']}")
                print(f"  Hours remaining after today: {topic['remaining_hours']:.1f}")
            
            print(f"\nTotal suggested study hours today: {total_hours:.1f}")
            print("-" * 40)

        except Exception as e:
            print(f"Error displaying today's schedule: {e}")

    def do_complete_day(self, arg):
        """Complete today's study activities by logging actual hours spent.
        Usage: complete_day
        """
        try:
            if not self.subjects:
                print("No subjects found. Add some subjects first.")
                return

            schedule = self.scheduler.create_schedule()
            if not schedule:
                print("No study activities scheduled.")
                return

            today = date.today()
            today_schedule = next((day for day in schedule if day["date"] == today), None)
            
            if not today_schedule:
                print("No study activities scheduled for today.")
                return

            print("\nToday's Study Activities:")
            print("-" * 40)
            
            for i, scheduled_topic in enumerate(today_schedule["topics"], 1):
                subject = next(s for s in self.subjects if s.name == scheduled_topic["subject"])
                topic = next(t for t in subject.topics if t.name == scheduled_topic["topic"])
                
                print(f"\n{i}. {scheduled_topic['subject']} - {scheduled_topic['topic']}")
                print(f"  Suggested Hours: {scheduled_topic['hours']:.1f}")
                
                while True:
                    try:
                        hours_input = input(f"  Enter actual hours spent (or press Enter to skip): ").strip()
                        if not hours_input:
                            print("  Skipped.")
                            break
                            
                        hours = float(hours_input)
                        if hours < 0:
                            print("  Hours cannot be negative.")
                            continue
                            
                        topic.add_hours(hours)
                        if topic.hours_spent >= topic.estimated_hours:
                            completed = input("  Topic hours completed. Mark as complete? (y/n): ").lower()
                            if completed == 'y':
                                topic.mark_complete()
                                print(f"  Marked {topic.name} as complete.")
                        
                        subject.update_progress()
                        break
                        
                    except ValueError:
                        print("  Please enter a valid number.")

            print("\nDay completed! Progress has been saved.")
            
        except Exception as e:
            print(f"Error completing day: {e}")

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