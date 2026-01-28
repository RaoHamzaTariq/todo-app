FROM python:3.13-slim

WORKDIR /app

# Copy requirements first to leverage Docker layer caching
COPY backend/requirements.txt .

# Install system dependencies and Python packages
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    && pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt \
    && pip install --no-cache-dir mcp \
    && apt-get purge -y gcc \
    && apt-get autoremove -y \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Copy application code
COPY backend/src/app/mcp/ /app/

# Expose the port the MCP server will run on
EXPOSE 8080

# Run the MCP server
CMD ["python", "server.py"]