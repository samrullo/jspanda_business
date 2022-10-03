FROM ubuntu
RUN apt update
RUN apt install -y nginx
RUN apt install -y systemctl

# C header libraries to connect to postgresql database
RUN apt install -y libpq-dev


ENV STATIC_URL /static
ENV STATIC_PATH /app/application/static
COPY ./requirements.txt /var/www/flask_app/
RUN pip install -r /var/www/flask_app/requirements.txt
COPY ./python_bugs/flask_uploads.py /usr/local/lib/python3.8/site-packages/flask_uploads.py