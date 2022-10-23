# Goal
I want to run my python web application based on Flask or Django on nginx, a popular web server.

To achieve this we will have to leverage WSGI (Web Server Gateway Interface) for python, which is described
in https://peps.python.org/pep-0333/

Also https://www.digitalocean.com/community/tutorials/how-to-set-up-uwsgi-and-nginx-to-serve-python-apps-on-ubuntu-14-04#definitions-and-concepts is a good article
to implement python application running on nginx by implementing WSGI.

# Quick introduction

Before we jump in, we should address some confusing terminology associated with the interrelated concepts we will be dealing with. These three separate terms that appear interchangeable, but actually have distinct meanings:

- WSGI: A Python spec that defines a standard interface for communication between an application or framework and an application/web server. This was created in order to simplify and standardize communication between these components for consistency and interchangeability. This basically defines an API interface that can be used over other protocols.
- uWSGI: An application server container that aims to provide a full stack for developing and deploying web applications and services. The main component is an application server that can handle apps of different languages. It communicates with the application using the methods defined by the WSGI spec, and with other web servers over a variety of other protocols. This is the piece that translates requests from a conventional web server into a format that the application can process.
- uwsgi: A fast, binary protocol implemented by the uWSGI server to communicate with a more full-featured web server. This is a wire protocol, not a transport protocol. It is the preferred way to speak to web servers that are proxying requests to uWSGI.


## WSGI Application requirements
WSGI defines the interface between a web server and an application.
In this context web server is *uWSGI* which can translate client requests to the application, python application in this case.

Web Server sends request to the application by triggering a defined *callable*.
A *callable* is literally a callable python function that accepts following parameters
- dictionary like data that usually holds environmental variables
- a callable sent by the web server that the application has to call. This callable accepts two arguments, **HTTP status code**
and **list of tuples each of which defines a response header with its corresponding value**

Application in response returns an iterable that is used to render html page.

# How nginx talks to python web application via uwsgi

Essentially *nginx* is sending or proxying client request to *uWSGI* application server
which can then interact with python web application via WSGI interface.

So we have to install and start *uWSGI* server for nginx be able to server our python web application

we install *uWSGI* by running 
```pip install uwsgi```

After defining our ```wsgi.py``` entry script with ```def application``` function as below
we can start our *uWSGI* server and serve a very simple python web application, which in this
example just one function which simply returns ```hello world```

```python
def application(environ,start_response):
    start_response("200 OK",[("Content-type","text/html")])
    return [b"<h1> hello galaxy</h1>"]
```

Then we can start *uWSGI* server as below

```
(venv)$ uwsgi --socket 0.0.0.0:80 --protocol=http -w <name of python script that has application callable>
```

But to have *nginx* serve our python web application, we have to set up a *system service* that 
starts at the boot and also triggers *uWSGI* server to listen on a socket based on *.ini* file

For instance we can define *ini* file as below

```
[uwsgi]
module = wsgi:application

master = true
processes = 5

socket = myapp.sock
chmod-socket = 664
vacuum = true

die-on-term = true
```

Then we can create a system service by defining a file */etc/systemd/system/mysimplewsgi.service*

```bash
[Unit]
Description=uWSGI occasion to serve myproject
After=community.goal

[Service]
Person=root
Group=www-data
WorkingDirectory=/var/data/mysimplewsgi
Surroundings="PATH=/var/data/mysimplewsgi/venv/bin"
ExecStart=/var/data/mysimplewsgi/venv/bin/uwsgi --ini mysimplewsgi.ini

[Install]
WantedBy=multi-user.goal
```

You can see that above new system service sets the working directory, path and executes uwsgi with --ini option

Once we defined our new service we can start it by running

```bash
systemctl start mysimplewsgi
```

With above we have our *uWSGI* server listening on socket defined in **mysimplewsgi.ini** file in the working directory.

Finally we create config for nginx to talk to our application.

We do this by creating a new config **/etc/nginx/sites-available/mysimplewsgi.conf**

```
server {
    listen 80;
    server_name localhost;

    location / {
        include         uwsgi_params;
        uwsgi_pass      unix:/var/data/mysimplewsgi/myapp.sock;
    }
}
```

and creating symlink under ```/etc/nginx/sites-enabled/``` with the same name which can be achieved by running below

```bash
ln -s /etc/nginx/sites-available/mysimplewsgi.conf /etc/nginx/sites-enabled
```

With above reload nginx and you can now access your python web application. Congrats

```bash
nginx -s reload
```

Everytime you are changing your python web application, you have to restart the new system service that you defined above.
Essentially you are restarting *uWSGI* server.

```systemctl restart mysimplewsgi```
