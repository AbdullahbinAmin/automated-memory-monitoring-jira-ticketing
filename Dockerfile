FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY automated-memory-monitoring-jira-ticketing.py .

# Non-root user
RUN useradd -m -u 1000 appuser && chown -R appuser /app
USER appuser

ENTRYPOINT ["python", "automated-memory-monitoring-jira-ticketing.py"]
