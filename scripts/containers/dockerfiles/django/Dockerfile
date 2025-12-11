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
         build-essential \
         libpq-dev \
         gcc \
         vim \
    && apt-get clean

# Install dependencies
COPY ./requirements.txt /app
RUN pip install --upgrade pip \
    && pip install -r requirements.txt


# Copy application code
COPY ./app/ /app/

# Expose the port your Django application will run on (e.g., Gunicorn)
EXPOSE 8000

CMD ["gunicorn", "--bind", "0.0.0.0:8000", "app.wsgi:application", "--reload"]