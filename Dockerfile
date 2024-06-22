# Use the official slim Python image as the base image
FROM python:3.12.4-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set the working directory to /app
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . .

# Install any necessary dependencies specified in requirements.txt
# Use --no-cache-dir to avoid caching the pip packages
RUN --mount=type=cache,target=/root/.cache/pip pip install --no-cache-dir -r requirements.txt

# Ensure the application listens on port 8000
EXPOSE 8000

# Add a user and group with a specific UID and GID
ARG UID=10001
RUN adduser --disabled-password --gecos "" --home "/" --shell "/sbin/nologin" --no-create-home --uid "${UID}" appuser

# Change to the non-root user
USER appuser

# Command to run the application
CMD ["python3", "main.py"]
