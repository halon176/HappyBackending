FROM python:3.11

COPY . .

RUN pip install -r requirements.txt

RUN alembic upgrade head

CMD uvicorn src.main:app --host 0.0.0.0 --port 80 && celery -A src.tasks.tasks:celery worker --loglevel=INFO --pool=solo && celery -A src.tasks.tasks:celery flower