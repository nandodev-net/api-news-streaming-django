from python:3.10.2

# set work directory
WORKDIR /usr/src/app

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1


# install psycopg2 dependencies
# RUN apk update \
#     && apk add postgresql-dev gcc python3-dev musl-dev

# install dependencies
RUN pip install --upgrade pip
COPY ./requirements.txt .
RUN pip install -r requirements.txt

# Set up entry point
COPY ./entrypoint.sh .
RUN sed -i 's/\r$//g' /usr/src/app/entrypoint.sh
RUN chmod +x /usr/src/app/entrypoint.sh

RUN apt-get update
RUN apt-get install -y netcat

# copy project
COPY . .

RUN poetry config virtualenvs.create false --local

# Install dependencies with poetry
RUN poetry install 

ENTRYPOINT ["/usr/src/app/entrypoint.sh"]
