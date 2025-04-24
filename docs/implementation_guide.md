# StudyBuddy Implementation Guide

## Project Structure

```
study-planner/
├── src/
│   ├── models/
│   │   ├── __init__.py
│   │   ├── subject.py
│   │   └── topic.py
│   ├── controllers/
│   │   ├── __init__.py
│   │   └── scheduler.py
│   ├── storage/
│   │   ├── __init__.py
│   │   └── file_storage.py
│   ├── cli/
│   │   ├── __init__.py
│   │   └── interface.py
│   └── __init__.py
├── tests/
│   ├── __init__.py
│   ├── test_models.py
│   └── test_scheduler.py
├── requirements.txt
└── main.py
```

## Phase 1 Implementation Steps

### 1. Core Models (src/models/)

#### Topic Class (topic.py)

- Properties:
  - name (str)
  - priority (int, 1-5)
  - estimated_hours (float)
  - completed (bool)
- Methods:
  - __init__
  - mark_complete()
  - __str__

#### Subject Class (subject.py)

- Properties:
  - name (str)
  - exam_date (datetime)
  - difficulty (int, 1-5)
  - topics (List[Topic])
  - progress (float)
- Methods:
  - __init__
  - add_topic()
  - remove_topic()
  - update_progress()
  - __str__

### 2. Storage System (src/storage/)

#### FileStorage Class (file_storage.py)

- JSON-based persistence
- Methods:
  - save_subjects()
  - load_subjects()
  - _serialize_subject()
  - _deserialize_subject()

### 3. CLI Interface (src/cli/)

#### CommandLineInterface Class (interface.py)

- Commands:
  - add_subject
  - remove_subject
  - add_topic
  - mark_topic_complete
  - list_subjects
  - view_schedule
- Input validation
- User feedback

### 4. Testing (tests/)

#### Model Tests (test_models.py)

- Test Topic class
- Test Subject class
- Test progress calculations

#### Scheduler Tests (test_scheduler.py)

- Test schedule generation
- Test time allocation
- Test priority handling

## Setup Instructions

1. Create virtual environment:

```bash
python -m venv venv
source venv/bin/activate  # On Windows: .\venv\Scripts\activate
```

2. Install dependencies:

```bash
pip install -r requirements.txt
```

## Dependencies (requirements.txt)

```
python-dateutil>=2.8.2
pytest>=7.0.0
```

## Development Guidelines

1. Follow PEP 8 style guide
2. Write docstrings for all classes and methods
3. Add type hints
4. Write tests for new features
5. Use meaningful variable names
6. Keep functions small and focused

## Testing

Run tests with:

```bash
pytest tests/
```

## Next Steps After Phase 1

1. Implement advanced scheduling algorithm
2. Add progress tracking features
3. Implement database storage
4. Begin GUI development

## Implementation Order

### Step 1: Project Setup (Day 1)
1. Create project directory structure
2. Set up virtual environment
3. Create initial empty files
4. Set up git repository
5. Create requirements.txt with initial dependencies

### Step 2: Core Models (Days 1-2)
1. Implement Topic class
   - Basic attributes and methods
   - Input validation
   - String representation
2. Implement Subject class
   - Core attributes and methods
   - Topic management
   - Progress tracking
3. Write unit tests for both classes
4. Test and debug

### Step 3: Storage System (Days 2-3)
1. Implement FileStorage class
   - JSON serialization/deserialization
   - File handling
   - Error handling
2. Write storage unit tests
3. Test with sample data
4. Add data validation

### Step 4: CLI Interface (Days 3-4)
1. Create basic command loop
2. Implement core commands:
   - Add/remove subjects
   - Add/remove topics
   - Mark topics as complete
   - List subjects and topics
3. Add input validation
4. Implement help system
5. Test user interaction flow

### Step 5: Basic Scheduler (Days 4-5)
1. Implement simple scheduling algorithm
2. Add time allocation logic
3. Create schedule display format
4. Test scheduling functionality

### Step 6: Integration and Testing (Day 5)
1. Connect all components
2. Write integration tests
3. Add error handling
4. Test full workflow
5. Document usage

### Step 7: Refinement (Days 5-7)
1. Code cleanup
2. Performance optimization
3. Add logging
4. Improve error messages
5. Final testing
6. Update documentation

## Time Allocation
- Project Setup: 0.5 day
- Core Models: 1.5 days
- Storage System: 1 day
- CLI Interface: 1.5 days
- Basic Scheduler: 1 day
- Integration: 0.5 day
- Refinement: 1 day

Total: 7 days for Phase 1
