# syntax=docker/dockerfile:1
FROM python:3.10-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /mais_todos

COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .

EXPOSE 8000
