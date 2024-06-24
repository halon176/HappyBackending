FROM python:3.11-alpine AS compile-image

WORKDIR /app

COPY requirements.txt .

ENV PATH=/root/.local/bin:$PATH

RUN pip install --user -r requirements.txt

FROM python:3.11-alpine AS build-image

WORKDIR /app

COPY --from=compile-image /root/.local /root/.local

COPY ./src /app/src
COPY ./static /app/static

ENV PATH=/root/.local/bin:$PATH

CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]
