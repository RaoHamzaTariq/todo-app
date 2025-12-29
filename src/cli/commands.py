# SDD: Implements Task ID: T011, T012
"""CLI commands for the todo application.

This module handles user interaction, argument parsing, and output formatting.
"""

import argparse
import sys

from src.core.models import Task
from src.core.todo_manager import TodoManager


def add_command(args: argparse.Namespace, manager: TodoManager) -> None:
    """Handle 'add' subcommand.

    Args:
        args: Parsed arguments containing title and optional description
        manager: TodoManager instance for task operations
    """
    # SDD: Implements Task ID: T011
    try:
        task = manager.add_task(args.title, args.description)
        print(f"Added task {task.id}: {task.title}")
    except ValueError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


def list_command(args: argparse.Namespace, manager: TodoManager) -> None:
    """Handle 'list' subcommand.

    Args:
        args: Parsed arguments (no additional args needed)
        manager: TodoManager instance for task operations
    """
    # SDD: Implements Task ID: T015
    tasks = manager.list_tasks()
    if not tasks:
        print("No tasks found. Add a task with: todo add \"Title\" \"Description\"")
        return

    print("Tasks:")
    for task in tasks:
        status = "Completed" if task.status.value == "Completed" else "Pending"
        print(f"{task.id}. [{status}] {task.title}")


def update_command(args: argparse.Namespace, manager: TodoManager) -> None:
    """Handle 'update' subcommand.

    Args:
        args: Parsed arguments containing task_id, title, and description
        manager: TodoManager instance for task operations
    """
    # SDD: Implements Task ID: T018
    try:
        task = manager.update_task(
            task_id=args.task_id,
            title=args.title,
            description=args.description,
        )
        if task:
            print(f"Updated task {task.id}: {task.title}")
        else:
            print(f"Error: Task {args.task_id} not found", file=sys.stderr)
            sys.exit(1)
    except ValueError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


def complete_command(args: argparse.Namespace, manager: TodoManager) -> None:
    """Handle 'complete' subcommand.

    Args:
        args: Parsed arguments containing task_id
        manager: TodoManager instance for task operations
    """
    # SDD: Implements Task ID: T020
    task = manager.toggle_complete(args.task_id)
    if task:
        print(f"Completed task {task.id}: {task.title}")
    else:
        print(f"Error: Task {args.task_id} not found", file=sys.stderr)
        sys.exit(1)


def delete_command(args: argparse.Namespace, manager: TodoManager) -> None:
    """Handle 'delete' subcommand.

    Args:
        args: Parsed arguments containing task_id
        manager: TodoManager instance for task operations
    """
    # SDD: Implements Task ID: T022
    if manager.delete_task(args.task_id):
        print(f"Deleted task {args.task_id}")
    else:
        print(f"Error: Task {args.task_id} not found", file=sys.stderr)
        sys.exit(1)


def create_parser() -> argparse.ArgumentParser:
    """Create the argument parser for the todo CLI.

    Returns:
        Configured ArgumentParser with subcommands for all operations
    """
    # SDD: Implements Task ID: T012
    parser = argparse.ArgumentParser(
        prog="todo",
        description="A simple CLI todo application with in-memory storage",
    )
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # add command
    add_parser = subparsers.add_parser("add", help="Add a new task")
    add_parser.add_argument("title", help="Task title (required)")
    add_parser.add_argument(
        "description", nargs="?", default="", help="Optional task description"
    )
    add_parser.set_defaults(func=add_command)

    # list command
    list_parser = subparsers.add_parser("list", help="List all tasks")
    list_parser.set_defaults(func=list_command)

    # update command
    update_parser = subparsers.add_parser(
        "update", help="Update an existing task"
    )
    update_parser.add_argument("task_id", type=int, help="Task ID to update")
    update_parser.add_argument("--title", help="New task title")
    update_parser.add_argument("--description", help="New task description")
    update_parser.set_defaults(func=update_command)

    # complete command
    complete_parser = subparsers.add_parser(
        "complete", help="Mark a task as completed"
    )
    complete_parser.add_argument("task_id", type=int, help="Task ID to complete")
    complete_parser.set_defaults(func=complete_command)

    # delete command
    delete_parser = subparsers.add_parser("delete", help="Delete a task")
    delete_parser.add_argument("task_id", type=int, help="Task ID to delete")
    delete_parser.set_defaults(func=delete_command)

    return parser
