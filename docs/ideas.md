# StudyBuddy - Study Scheduler Application

## Core Features

### 1. Subject Management

- Add/edit/delete subjects
- Set exam dates
- Assign difficulty levels (1-5)
- Track topics within subjects
- Set priority levels

### 2. Schedule Generation

- Create daily/weekly study plans
- Smart time allocation based on:
  - Days until exam
  - Subject difficulty
  - Topic priority
  - Available study hours
- Flexible scheduling options

### 3. Progress Tracking

- Mark topics as completed
- Track study hours
- Progress visualization
- Performance metrics
- Study streak tracking

### 4. User Interface

- Initial version: Command-line interface
- Future version: GUI using tkinter
- Potential web version using Flask

## Technical Requirements

### Libraries

- `datetime`: Date and time handling
- `sqlite3`: Local data storage
- `tkinter`: GUI (future)
- `matplotlib`: Progress visualization
- `pandas`: Data management

### Data Structure

```python
Subject:
  - name: str
  - exam_date: datetime
  - difficulty: int
  - topics: List[Topic]
  - progress: float

Topic:
  - name: str
  - priority: int
  - estimated_hours: float
  - completed: bool
```

## Development Phases

### Phase 1: Core Functionality

1. Basic subject management
2. Simple scheduling algorithm
3. Command-line interface
4. File-based storage

### Phase 2: Enhanced Features

1. Advanced scheduling algorithm
2. Progress tracking
3. Statistics and reporting
4. Database implementation

### Phase 3: User Interface

1. Basic GUI implementation
2. Visual progress tracking
3. Interactive calendar
4. Reminder system

## Future Enhancements

- Mobile app integration
- Cloud sync
- Study group features
- AI-powered scheduling
- Pomodoro timer integration
