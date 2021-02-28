FROM gcr.io/cs6510-spr2021/stimuli_ci_base

# Allow statements and log messages to immediately appear in the Cloud Run logs
ENV PYTHONUNBUFFERED True

WORKDIR /app

COPY src/ /app

EXPOSE 8080

# Run the web service on container startup. 
# Use gunicorn webserver with one worker process and 8 threads.
# For environments with multiple CPU cores, increase the number of workers
# to be equal to the cores available.
CMD ["gunicorn", "--bind",  ":8080", "--workers",  "1",  "--threads", "8", "--timeout", "0", "server.main:app"]

