FROM python:3.8
ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONFAULTHANDLER 1

RUN mkdir /app

WORKDIR /app/
RUN apt-get update && apt-get install -y libpq-dev \
    && pip install pipenv

COPY Pipfile .
COPY Pipfile.lock .
RUN PIPENV_VENV_IN_PROJECT=1 pipenv install --system && pwd
ENV PATH="/app/.venv/bin:$PATH"

COPY solution/ /app/