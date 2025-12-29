# SDD: Implements Task ID: T013
"""Entry point for the todo CLI application.

This module provides the main() function that serves as the CLI entry point.
"""

from src.cli.commands import create_parser
from src.core.todo_manager import TodoManager


def main() -> None:
    """Main entry point for the todo CLI application.

    Initializes the TodoManager, parses command-line arguments,
    and dispatches to the appropriate command handler.
    """
    manager = TodoManager()
    parser = create_parser()
    args = parser.parse_args()

    if args.command is None:
        parser.print_help()
        return

    args.func(args, manager)


if __name__ == "__main__":
    main()
