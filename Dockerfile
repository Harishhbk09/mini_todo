# A Dockerfile is a recipe for packaging your app + its runtime into an "image".
# The same image runs identically on your laptop and in the cloud.

# 1. Start from a small official Python base image
FROM python:3.12-slim

# 2. Work inside /app in the container
WORKDIR /app

# 3. Install dependencies first (Docker caches this layer if requirements don't change)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 4. Copy the app code
COPY app.py .

# 5. Don't run as root (security basic)
RUN useradd --create-home appuser
USER appuser

# 6. Default config; the cloud platform can override these
ENV APP_ENV=production PORT=8080
EXPOSE 8080

# 7. Run with gunicorn, a production web server (Flask's built-in server is for dev only)
CMD gunicorn --bind 0.0.0.0:$PORT --workers 1 app:app
