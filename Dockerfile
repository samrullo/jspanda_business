FROM tiangolo/uwsgi-nginx-flask:python3.8-alpine
#FROM tiangolo/meinheld-gunicorn-flask
RUN apk --update add bash nano
RUN apk add build-base postgresql-dev
ENV STATIC_URL /static
ENV STATIC_PATH /app/application/static
COPY ./requirements.txt /var/www/flask_app/
RUN pip install -r /var/www/flask_app/requirements.txt
COPY ./python_bugs/flask_uploads.py /usr/local/lib/python3.8/site-packages/flask_uploads.py