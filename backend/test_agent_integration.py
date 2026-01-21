"""
Test script for OpenAI Agent MCP integration.

This script tests the integration between the OpenAI Agents SDK and the MCP server
following the patterns demonstrated in the sample code.
"""

import asyncio
import os
from src.app.agent.integration import OpenAIAgentMCPIntegration, process_user_query


async def test_basic_integration():
    """Test basic integration functionality."""
    print("Testing basic OpenAI Agent MCP integration...")

    # Get API key from environment or use a placeholder for testing
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        print("Warning: OPENAI_API_KEY not found in environment. Using dummy key for testing.")
        api_key = "dummy-key-for-testing"

    try:
        # Initialize the integration
        integration = OpenAIAgentMCPIntegration(api_key=api_key)

        # Test health check
        health_result = await integration.health_check()
        print(f"Health check result: {health_result}")

        # Test basic query processing
        result = await integration.process_with_agent(
            user_id="test-user-123",
            query="What can you help me with regarding my tasks?"
        )

        print(f"Query result: {result}")
        return True

    except Exception as e:
        print(f"Error during basic integration test: {e}")
        return False


async def test_task_operations():
    """Test various task operations through the agent."""
    print("\nTesting task operations through agent...")

    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        print("Warning: OPENAI_API_KEY not found in environment. Using dummy key for testing.")
        api_key = "dummy-key-for-testing"

    try:
        integration = OpenAIAgentMCPIntegration(api_key=api_key)

        # Test creating a task
        create_result = await integration.process_with_agent(
            user_id="test-user-123",
            query="Please create a task titled 'Test Task' with description 'This is a test task' and high priority."
        )
        print(f"Create task result: {create_result}")

        # Test listing tasks
        list_result = await integration.process_with_agent(
            user_id="test-user-123",
            query="What tasks do I have?"
        )
        print(f"List tasks result: {list_result}")

        return True

    except Exception as e:
        print(f"Error during task operations test: {e}")
        return False


async def test_convenience_function():
    """Test the convenience function."""
    print("\nTesting convenience function...")

    api_key = os.getenv("OPENAI_API_KEY") or "dummy-key-for-testing"

    try:
        result = await process_user_query(
            user_id="test-user-123",
            query="Hello, can you help me manage my tasks?",
            api_key=api_key
        )

        print(f"Convenience function result: {result}")
        return True

    except Exception as e:
        print(f"Error during convenience function test: {e}")
        return False


async def main():
    """Run all tests."""
    print("Starting OpenAI Agent MCP Integration Tests...\n")

    tests = [
        ("Basic Integration", test_basic_integration),
        ("Task Operations", test_task_operations),
        ("Convenience Function", test_convenience_function),
    ]

    results = []
    for test_name, test_func in tests:
        print(f"Running {test_name} test...")
        try:
            result = await test_func()
            results.append((test_name, result))
            print(f"{test_name} test: {'PASSED' if result else 'FAILED'}\n")
        except Exception as e:
            print(f"{test_name} test: ERROR - {e}\n")
            results.append((test_name, False))

    # Summary
    print("Test Summary:")
    passed = sum(1 for _, result in results if result)
    total = len(results)
    print(f"Passed: {passed}/{total}")

    for test_name, result in results:
        status = "PASS" if result else "FAIL"
        print(f"  {test_name}: {status}")


if __name__ == "__main__":
    asyncio.run(main())