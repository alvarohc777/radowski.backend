FROM python:3.12.1-alpine3.19
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
WORKDIR /code
COPY requirements.txt /code/
RUN pip install -r requirements.txt
COPY ./radowski/ /code/
RUN mkdir static
RUN python manage.py collectstatic --noinput

