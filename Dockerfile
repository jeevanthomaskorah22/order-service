FROM python:3.9-slim

# Install PostgreSQL client to enable pg_isready
RUN apt-get update && \
    apt-get install -y postgresql-client curl && \
    apt-get clean

# Set working directory
WORKDIR /app

# Copy app code
COPY . .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy and set permissions for wait script
COPY wait-for-postgres.sh /wait-for-postgres.sh
RUN chmod +x /wait-for-postgres.sh

# Set Python path
ENV PYTHONPATH=/app

# Entry script waits for DB before starting app
ENTRYPOINT ["/wait-for-postgres.sh"]

# Start FastAPI app
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8002"]
