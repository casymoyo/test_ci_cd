FROM python:3.12
WORKDIR /usr/local/app

# Install the application dependencies
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Setup an app user so the container doesn't run as the root user
RUN useradd app
USER app

RUN chown -R appuser:appuser /app

# Download dependencies as a separate step to take advantage of Docker's caching.
# Leverage a cache mount to /root/.cache/pip to speed up subsequent builds.
# Leverage a bind mount to requirements.txt to avoid having to copy them into
# into this layer.
RUN --mount=type=cache,target=/root/.cache/pip \
    --mount=type=bind,source=requirements.txt,target=requirements.txt \
    python -m pip install -r requirements.txt

# Switch to the non-privileged user to run the application.
USER appuser

WORKDIR /app
# Copy the source code into the container.
COPY . .

# Expose the port that the application listens on.
EXPOSE 8300

# Run the application.
CMD gunicorn -b 0.0.0.0 -p 8300 test_ci_cd.wsgi:application
