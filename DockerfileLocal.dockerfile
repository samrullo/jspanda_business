FROM samrullo/ubuntu_2204_pyenv_311

RUN mkdir /var/www/jspanda_business
WORKDIR /var/www/jspanda_business

COPY ./data/etc/systemd/system/jspanda.service /etc/systemd/system/

COPY ./requirements.txt .
RUN /root/.pyenv/shims/pip install -r ./requirements.txt

COPY ./python_bugs/flask_uploads.py /root/.pyenv/versions/3.9.14/lib/python3.9/site-packages/flask_uploads.py