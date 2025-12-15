FROM python:3.11.14-trixie

# disable auto check for pip updates
ENV PIP_DISABLE_PIP_VERSION_CHECK 1

# disable bytecode files (.pyc)
ENV PYTHONDONTWRITEBYTECODE=1

# send python output straight to the terminal with out buffering
#  (e.g. output django application logs in real time)
ENV PYTHONUNBUFFERED 1

# Set working directory
WORKDIR /app

RUN apt-get update \
    && apt-get -y install \
        bash \
        build-essential \
        libpq-dev \
        gcc \
        vim \
    && apt-get clean

SHELL ["/bin/bash", "-c"]

# Install dependencies
COPY ./requirements.txt /app/
RUN pip install --upgrade pip \
    && pip install -r requirements.txt

# Copy the env file and set environment variables
COPY container.env /.env

# Copy the entrypoint script, and make the script executable
COPY entrypoint.sh /
RUN chmod +x /entrypoint.sh

# Copy application code
COPY ./app/ /app/

# Expose the port your Django application will run on (e.g., Gunicorn)
EXPOSE 8000

# Set the entrypoint script
ENTRYPOINT ["/entrypoint.sh"]

# Define a default command (CMD becomes arguments to ENTRYPOINT)
CMD ["echo", "Container started successfully"]
