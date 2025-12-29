# Quickstart: In-Memory Todo CLI

**Feature**: 001-todo-cli | **Last Updated**: 2025-12-29

## Prerequisites

- Python 3.13 or higher
- `uv` package manager

## Installation

### 1. Initialize Project with uv

```bash
# Create project structure
mkdir -p todo-cli && cd todo-cli

# Initialize uv project
uv init --name todo-cli --python 3.13

# Create directory structure
mkdir -p src/cli src/core tests
touch src/cli/__init__.py src/core/__init__.py

# Add dependencies (none required - using stdlib only)
uv add pytest --dev  # For testing
```

### 2. Configure pyproject.toml

```toml
[project]
name = "todo-cli"
version = "0.1.0"
description = "A simple CLI todo application"
requires-python = ">=3.13"
dependencies = []

[project.scripts]
todo = "main:main"

[tool.uv]
package = false

[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"
```

## Development Setup

### 1. Clone and Setup

```bash
git clone <repo-url>
cd todo-cli
uv sync
```

### 2. Verify Installation

```bash
python --version  # Should be 3.13+
uv run python -c "from core.todo_manager import TodoManager; print('Setup successful!')"
```

## Usage

### Basic Commands

```bash
# Add a task
uv run python main.py add "Buy groceries" "Milk, eggs, bread"

# List all tasks
uv run python main.py list

# Update a task
uv run python main.py update 1 --title "Buy groceries" --description "Milk, eggs, bread, butter"

# Complete a task
uv run python main.py complete 1

# Delete a task
uv run python main.py delete 1
```

### Help

```bash
uv run python main.py --help
uv run python main.py add --help
```

## Project Structure

```
todo-cli/
├── src/
│   ├── cli/
│   │   ├── __init__.py
│   │   └── commands.py    # CLI layer - argument parsing
│   ├── core/
│   │   ├── __init__.py
│   │   ├── models.py      # Task dataclass, TaskStatus enum
│   │   └── todo_manager.py # Business logic (TodoManager)
│   └── main.py            # Application entry point
├── tests/
│   └── test_todo_manager.py
├── pyproject.toml
└── README.md
```

## Running Tests

```bash
# Run all tests
uv run pytest

# Run with verbose output
uv run pytest -v

# Run specific test file
uv run pytest tests/test_todo_manager.py
```

## Code Quality

### Linting

```bash
# Check code style (if ruff is installed)
uv add ruff --dev
uv run ruff check src/
```

### Type Checking

```bash
# Check types (if mypy is installed)
uv add mypy --dev
uv run mypy src/
```

## Common Issues

### Python Version Too Low

```bash
Error: requires-python constraint not met
Solution: Install Python 3.13+
```

### Module Not Found

```bash
Error: ModuleNotFoundError: No module named 'core'
Solution: Run from project root: uv run python main.py
```

## Next Steps

1. Run `/sp.tasks` to generate implementation tasks
2. Implement code following the plan in `plan.md`
3. Add unit tests for TodoManager methods
4. Verify all acceptance scenarios pass