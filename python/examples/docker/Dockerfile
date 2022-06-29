# syntax=docker/dockerfile:1

FROM python:3.9-alpine

WORKDIR /app

# install python dependencies
COPY ./src/requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY . .

# CMD ["python3", "-m", "flask", "run", "--host=0.0.0.0"]
# CMD ["python3", "/app/src/app.py", "--host=0.0.0.0"]
ENTRYPOINT [ "./entrypoint.sh" ]
