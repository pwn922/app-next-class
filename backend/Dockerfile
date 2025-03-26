FROM python:3.12-alpine AS deps

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir --prefix=/install -r requirements.txt

FROM python:3.12-alpine AS base

WORKDIR /app

COPY --from=deps /install /usr/local

COPY . .

FROM base AS prod

RUN pip install --no-cache-dir gunicorn

CMD ["gunicorn", "--bind", "0.0.0.0:5000", "app:app"]