FROM python:3.12
WORKDIR /usr/local/app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
RUN useradd app
USER app

RUN chown -R appuser:appuser 
RUN --mount=type=cache,target=/root/.cache/pip \
    --mount=type=bind,source=requirements.txt,target=requirements.txt \
    python -m pip install -r requirements.txt

# Switch to the non-privileged user to run the application.
USER appuser

WORKDIR /app
COPY . .

# Expose the port that the application listens on.
EXPOSE 8300

# Run the application.
CMD gunicorn -b 0.0.0.0 -p 8300 test_ci_cd.wsgi:application
