FROM python:3.10.5

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /StripeApi/stripes

COPY Pipfile Pipfile.lock /StripeApi/
RUN pip install pipenv && pipenv install --system
RUN pip install stripe
RUN pip install django-debug-toolbar
RUN pip install django-rest-framework
RUN pip install django-crispy-forms
RUN pip install pillow
RUN pip install Django
RUN pip install gunicorn

COPY . /StripeApi/