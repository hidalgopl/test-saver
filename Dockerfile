FROM python:3.7-slim
RUN apt-get update && apt-get install -qq -y build-essential libpq-dev --no-install-recommends
COPY requirements/requirements.txt .
RUN pip install -r requirements.txt && rm -rf /root/.cache
WORKDIR /code
COPY . /code/

ENTRYPOINT ["python", "-m", "test_saver"]
