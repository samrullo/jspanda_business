# To reload nginx

```bash
nginx -s reload -c /etc/nginx/nginx.conf
```

# Key files, directories and commands

- ```/etc/nginx/``` is the default configuration root for NGINX server. Within this directory you will find configuration files that instruct NGINX on how to behave
- ```/etc/nginx/nginx.conf``` is the default configuration entry point used by the NGINX service. This configuration file sets up global settings for things like worker process, tuning, logging, loading dynamic modules, and references to other NGINX configuration files. In a default configuration, the /etc/nginx/nginx.conf file includes the top-level http block, or context, which includes all configuration files in the directory described next
- /etc/nginx/conf.d directory contains the default HTTP server configuration file. Files in this directory ending in .conf are included in the top-level http block from within /etc/nginx/nginx.conf file. It is best practice to utilize include statements and organize yours