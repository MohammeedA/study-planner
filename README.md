# StudyPlanner 📚

A comprehensive study planning tool to help you organize your subjects, track topics, and manage your study schedule effectively.

## Features

- Manage multiple subjects with their exam dates and difficulty levels
- Break down subjects into specific topics
- Prioritize topics (1-5 scale)
- Track estimated study hours for each topic
- Mark topics as complete
- Track overall subject progress
- JSON-based storage for persistence

## Requirements

- Python 3.11 or higher
- Dependencies listed in requirements.txt

## Installation

1. Clone the repository:

    ```bash
    git clone https://github.com/MohammeedA/study-planner.git
    cd study-planner
    ```

2. Create a virtual environment:

    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows: .\venv\Scripts\activate
    ```

3. Install dependencies:

    ```bash
    pip install -r requirements.txt
    ```

## Usage

Run the application:

```bash
python main.py
```

### Basic Commands

- Add a new subject with exam date
- Add topics to subjects
- Set topic priorities and estimated study hours
- Mark topics as complete
- View your study schedule
- Track progress for each subject

## Development

### Running Tests

```bash
python -m pytest
```

## Project Structure

```plaintext
study-planner/
├── src/
│   ├── models/        # Core data models
│   ├── controllers/   # Business logic
│   ├── storage/       # Data persistence
│   └── cli/          # Command-line interface
├── tests/            # Test suite
└── docs/            # Documentation
```

## License

This project is licensed under the terms included in the LICENSE file.
