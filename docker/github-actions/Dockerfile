FROM python:3.11-alpine

LABEL org.opencontainers.image.source="https://github.com/halon176/creazione_automatica_container"

COPY . .

RUN pip install -r requirements.txt

CMD python main.py