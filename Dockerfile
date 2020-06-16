FROM python:3.8-slim
RUN apt-get update && apt-get install -qq -y build-essential libpq-dev curl --no-install-recommends
COPY pyproject.toml .
COPY poetry.lock .
RUN curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python
RUN PATH="$HOME/.poetry/bin:$PATH" poetry install
WORKDIR /code
COPY . /code/

ENTRYPOINT ["poetry", "run", "test_saver"]
