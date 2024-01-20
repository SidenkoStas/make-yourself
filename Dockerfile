FROM python:3
ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

COPY . ./make-yourself
WORKDIR /make-yourself

RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

