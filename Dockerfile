FROM python:3.12.0

ENV HOME=/home/FastAPI \
    APP_HOME=/home/FastAPI/src \
    PYTHONPATH="$PYTHONPATH:/home/FastAPI" \
    PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1


RUN mkdir -p $APP_HOME && groupadd -r fastgroup && useradd -r -g fastgroup fast
WORKDIR $HOME

COPY poetry.lock pyproject.toml $HOME

RUN python -m pip install --upgrade pip
RUN pip install poetry
RUN poetry config virtualenvs.create false
RUN poetry install --no-interaction --no-root
RUN poetry self update

COPY config.yml $HOME
COPY alembic.ini $HOME
COPY alembic $HOME/alembic

COPY src $APP_HOME
#RUN alembic upgrade head

USER fast