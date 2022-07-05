# How it works
I followed mainly 3 resources below
- https://mindsers.blog/post/https-using-nginx-certbot-docker/
- https://rlagowski.medium.com/create-flask-app-with-uwsgi-nginx-certbot-for-ssl-and-all-this-with-docker-a9f23516618d
- https://pentacent.medium.com/nginx-and-lets-encrypt-with-docker-in-less-than-5-minutes-b4b8a60d3a71

As we know nginx looks up configurations in ```/etc/nginx/conf.d``` folder.
It turned out that NGINX reads all configurations within */etc/nginx/conf.d* folder.

In */etc/nginx/conf.d* I defined *app.conf* with below config which routes http request to https

```
server {
    listen 80;
    listen [::]:80;

    server_name jspanda.club www.jspanda.club;
    server_tokens off;

    location / {
        return 301 https://jspanda.club$request_uri;
    }
}

server {
    listen 443 ssl;

    location / {
        try_files $uri @app;
    }
    location @app {
        include uwsgi_params;
        uwsgi_pass unix:///tmp/uwsgi.sock;
    }
    location /static {
        alias /app/application/static;
    }

    ssl_certificate /etc/letsencrypt/live/jspanda.club/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/jspanda.club/privkey.pem;
    
}
```

The first *server* block routes all http requests to https

The second *server* block processes https requests.
It defines named location @app and serves flask application based on uwsgi.ini config.
It also defines ```ssl_certificate``` and ```ssl_certificate_key``` directives which probably certbot uses for validating the domain.

The tutorials above define certbot container in docker-compose.yml.
I hypothesize that it is only needed first time to issue ssl certificate and private key.
After that it doesn't run at all

# How I downloaded ssl_certificate from letsencrypt
As per https://pentacent.medium.com/nginx-and-lets-encrypt-with-docker-in-less-than-5-minutes-b4b8a60d3a71
Letsencrypt performs domain validation by requesting a well-known URL from a domain.
If it receives a certain response ("the challenge"), the domain is considered validated.
This is similar to how Google Search console establishes website ownership.
The response data is provided by certbot, so we need for nginx server to serve files from certbot.

First of all, we need two shared Docker volumes. One for the validation challenges, the other for the actual certificates.

Add this to the volumes list of the nginx section in docker-compose.yml.

- ./data/certbot/conf:/etc/letsencrypt
- ./data/certbot/www:/var/www/certbot

And this is the counterpart that needs to go in the certbot section:

volumes:
  - ./data/certbot/conf:/etc/letsencrypt
  - ./data/certbot/www:/var/www/certbot

Now we can make nginx serve the challenge files from certbot! Add this to the first (port 80) section of our nginx configuration (data/nginx/app.conf):

```
location /.well-known/acme-challenge/ {
    root /var/www/certbot;
}
```

After that, we need to reference the HTTPS certificates. Add the soon-to-be-created certificate and its private key to the second server section (port 443). Make sure to once again replace example.org with your domain name.

```
ssl_certificate /etc/letsencrypt/live/jspanda.club/fullchain.pem;
ssl_certificate_key /etc/letsencrypt/live/jspanda.club/privkey.pem;
```

And while we’re at it: The folks at Let’s Encrypt maintain best-practice HTTPS configurations for nginx. Let’s also add them to our config file. This will score you a straight A in the SSL Labs test!

```
include /etc/letsencrypt/options-ssl-nginx.conf;
ssl_dhparam /etc/letsencrypt/ssl-dhparams.pem;
```

**The Chicken or the Egg?**
Now for the tricky part. We need nginx to perform the Let’s Encrypt validation But nginx won’t start if the certificates are missing.

So what do we do? Create a dummy certificate, start nginx, delete the dummy and request the real certificates.
Luckily, you don’t have to do all this manually, I have created a convenient script for this.

Download the script to your working directory as init-letsencrypt.sh:

```
curl -L https://raw.githubusercontent.com/wmnnd/nginx-certbot/master/init-letsencrypt.sh > init-letsencrypt.sh
```

Edit the script to add in your domain(s) and your email address. If you’ve changed the directories of the shared Docker volumes, make sure you also adjust the data_path variable as well.

Then run chmod +x init-letsencrypt.sh and sudo ./init-letsencrypt.sh.

I did some changes into ```init_certbot.sh```, such as specifying domain name.
Initially I attempted running ```$sudo ./init_certbot.sh``` multiple times, but it failed saying can't serve ```jspanda.club/.well-known/acme-challenge/lkajdlfkjaldjf```
Then when I tried simply running ````$./init_certbot.sh``` it worked.
So still unclear what is causing initial failure, it can be due to directory ownership differences.