"""
Dapr service invocation middleware for the Todo Chatbot application.
This middleware enables service-to-service communication using Dapr's service invocation building block.
"""

import asyncio
import json
from typing import Callable, Any
from functools import wraps
from loguru import logger

from fastapi import Request, Response, HTTPException
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint


class DaprServiceInvocationMiddleware(BaseHTTPMiddleware):
    """
    Middleware for handling Dapr service invocations in the Todo Chatbot application.
    This ensures all communication between services uses Dapr APIs as required.
    """

    def __init__(self, app):
        super().__init__(app)
        self.dapr_client = None
        self._initialized = False

    async def initialize(self):
        """Initialize the Dapr client for service invocation."""
        if self._initialized:
            return

        try:
            # Import here to avoid dependency issues if Dapr is not available
            try:
                from dapr.aio.clients import DaprClient
                self.dapr_client = DaprClient()
                logger.info("Dapr client initialized for service invocation")
            except ImportError:
                logger.warning("Dapr client not available. Using mock mode.")
                self.dapr_client = MockDaprClient()

            self._initialized = True
        except Exception as e:
            logger.error(f"Failed to initialize Dapr client: {e}")
            raise

    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint) -> Response:
        """
        Process the incoming request through the middleware.

        Args:
            request: The incoming request
            call_next: The next middleware or endpoint in the chain

        Returns:
            Response: The processed response
        """
        if not self._initialized:
            await self.initialize()

        # Add Dapr-specific headers and context to the request
        request.state.dapr_context = {
            'trace_id': request.headers.get('dapr-trace-id'),
            'span_id': request.headers.get('dapr-span-id'),
            'correlation_id': request.headers.get('dapr-correlation-id', request.headers.get('x-correlation-id'))
        }

        # Process the request
        response = await call_next(request)

        # Add Dapr-specific headers to the response
        response.headers['dapr-trace-id'] = request.state.dapr_context.get('trace_id', '')
        response.headers['dapr-correlation-id'] = request.state.dapr_context.get('correlation_id', '')

        return response


def dapr_invoke(service_app_id: str, method: str, http_verb: str = "POST"):
    """
    Decorator to enable Dapr service invocation for specific endpoints.

    Args:
        service_app_id: The Dapr app ID of the target service
        method: The method to invoke on the target service
        http_verb: The HTTP verb to use for the invocation (default: POST)
    """
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        async def wrapper(*args, **kwargs):
            # Initialize Dapr client if not already done
            dapr_client = None
            try:
                from dapr.aio.clients import DaprClient
                dapr_client = DaprClient()
            except ImportError:
                logger.warning("Dapr client not available. Using mock mode.")
                dapr_client = MockDaprClient()

            try:
                # Get the request object if it's in the kwargs
                request = kwargs.get('request')

                # Prepare data for the invocation
                func_result = await func(*args, **kwargs)

                # If the function result is data to be sent to another service, invoke it
                if request and hasattr(request.state, 'dapr_context'):
                    correlation_id = request.state.dapr_context.get('correlation_id')

                    # Invoke the target service using Dapr
                    resp = await dapr_client.invoke_method(
                        app_id=service_app_id,
                        method=method,
                        data=json.dumps(func_result),
                        http_verb=http_verb,
                        metadata=(
                            ('correlation_id', correlation_id),
                        ) if correlation_id else ()
                    )

                    # Return the response from the target service
                    result = json.loads(resp.content_type)
                    return result

                return func_result
            except Exception as e:
                logger.error(f"Dapr service invocation failed: {e}")
                raise HTTPException(status_code=500, detail=f"Service invocation failed: {str(e)}")
            finally:
                if hasattr(dapr_client, 'close'):
                    await dapr_client.close()

        return wrapper
    return decorator


class DaprServiceInvoker:
    """
    Helper class for performing Dapr service invocations.
    """

    def __init__(self):
        self.dapr_client = None
        self._initialized = False

    async def initialize(self):
        """Initialize the Dapr client."""
        if self._initialized:
            return

        try:
            # Import here to avoid dependency issues if Dapr is not available
            try:
                from dapr.aio.clients import DaprClient
                self.dapr_client = DaprClient()
                logger.info("DaprServiceInvoker client initialized")
            except ImportError:
                logger.warning("Dapr client not available. Using mock mode.")
                self.dapr_client = MockDaprClient()

            self._initialized = True
        except Exception as e:
            logger.error(f"Failed to initialize DaprServiceInvoker: {e}")
            raise

    async def invoke_service(self, app_id: str, method: str, data: Any = None,
                           http_verb: str = "POST", timeout: int = 30) -> Any:
        """
        Invoke a method on another service via Dapr service invocation.

        Args:
            app_id: The Dapr app ID of the target service
            method: The method to invoke on the target service
            data: Data to send with the invocation
            http_verb: The HTTP verb to use for the invocation
            timeout: Timeout for the invocation in seconds

        Returns:
            Response from the target service
        """
        if not self._initialized:
            await self.initialize()

        try:
            # Convert data to bytes if it's not already
            if data is not None and not isinstance(data, bytes):
                data = json.dumps(data).encode('utf-8')

            # Perform the service invocation
            resp = await self.dapr_client.invoke_method(
                app_id=app_id,
                method=method,
                data=data,
                http_verb=http_verb
            )

            # Parse and return the response
            if resp.content_type.startswith('application/json'):
                return json.loads(resp.content_type.decode('utf-8'))
            else:
                return resp.content_type.decode('utf-8')

        except Exception as e:
            logger.error(f"Service invocation to {app_id}.{method} failed: {e}")
            raise

    async def close(self):
        """Close the Dapr client connection."""
        if self.dapr_client and hasattr(self.dapr_client, 'close'):
            await self.dapr_client.close()


# Global instance of the service invoker
_dapr_invoker = None


async def get_dapr_invoker() -> DaprServiceInvoker:
    """
    Get the singleton instance of the Dapr service invoker.

    Returns:
        DaprServiceInvoker: The singleton instance
    """
    global _dapr_invoker
    if _dapr_invoker is None:
        _dapr_invoker = DaprServiceInvoker()
        await _dapr_invoker.initialize()
    return _dapr_invoker


async def invoke_external_service(app_id: str, method: str, data: Any = None) -> Any:
    """
    Convenience function to invoke an external service using Dapr.

    Args:
        app_id: The Dapr app ID of the target service
        method: The method to invoke on the target service
        data: Data to send with the invocation

    Returns:
        Response from the target service
    """
    invoker = await get_dapr_invoker()
    return await invoker.invoke_service(app_id, method, data)


class MockDaprClient:
    """Mock Dapr client for testing and development when Dapr is not available."""

    async def invoke_method(self, app_id: str, method: str, data: Any = None,
                          http_verb: str = "POST", metadata: tuple = ()):
        """Mock invoke method."""
        import random

        # Simulate a response
        mock_response = {
            'status': 'success',
            'invoked_service': app_id,
            'method': method,
            'data_received': data.decode('utf-8') if isinstance(data, bytes) else data,
            'timestamp': asyncio.get_event_loop().time()
        }

        # Simulate occasional failures for testing
        if random.random() < 0.05:  # 5% failure rate
            raise Exception(f"Simulated invocation failure to {app_id}.{method}")

        print(f"[MOCK] Invoked {app_id}.{method} with data: {mock_response['data_received']}")
        return MockDaprResponse(json.dumps(mock_response))

    async def close(self):
        """Mock close method."""
        print("[MOCK] Dapr client closed")


class MockDaprResponse:
    """Mock response object for testing."""

    def __init__(self, content):
        self.content_type = content
        self.text = content