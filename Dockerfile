FROM samrullo/ubuntu_2204_nginx_pyenv_python-3.9.14

ENV STATIC_URL /static
ENV STATIC_PATH /app/application/static
SHELL ["/bin/bash", "-c"]
RUN source /root/.bashrc

COPY data/etc/systemd/system/jspanda.service /etc/systemd/system/
COPY data/nginx/etc/nginx/sites-available/jspanda.conf /etc/nginx/sites-available/
RUN ln -s /etc/nginx/sites-available/jspanda.conf /etc/nginx/sites-enabled/

RUN mkdir /var/www/flask_app/
COPY ./requirements.txt /var/www/flask_app/
RUN /root/.pyenv/shims/pip install -r /var/www/flask_app/requirements.txt
RUN /root/.pyenv/shims/pip install uwsgi
COPY ./python_bugs/flask_uploads.py /root/.pyenv/versions/3.9.14/lib/python3.9/site-packages/flask_uploads.py