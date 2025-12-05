# Dockerfile
FROM python:3.11-slim

WORKDIR /app
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

COPY requirements.txt .
RUN pip install -U pip && pip install -r requirements.txt

COPY . .

# Expose port (not required but good practice)
EXPOSE 8080

# For MCP stdio usage you might exec directly in Cloud Run or wrap with a small HTTP bridge.
# For now, we just keep an image that can run `python mcp_server.py`.
CMD ["python", "mcp_server.py"]
