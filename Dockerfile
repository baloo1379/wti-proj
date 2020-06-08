FROM tiangolo/meinheld-gunicorn-flask:python3.8

COPY ./app /app/app
COPY ./requirements.txt /app/requirements.txt

RUN pip install -r requirements.txt