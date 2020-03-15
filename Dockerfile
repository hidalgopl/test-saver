FROM python:3.7-slim
COPY requirements/requirements.txt .
RUN pip install -r requirements.txt && rm -rf /root/.cache
WORKDIR /code
COPY . /code/

ENTRYPOINT ["python", "-m", "test_saver"]
