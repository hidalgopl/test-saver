FROM python:3.7 as python-base
COPY requirements/requirements.txt .
RUN pip install -r requirements.txt

FROM python:3.7-alpine
COPY --from=python-base /root/.cache /root/.cache
COPY --from=python-base requirements.txt .
RUN pip install -r requirements.txt && rm -rf /root/.cache

CMD ["python", "-m", "test_saver"]
