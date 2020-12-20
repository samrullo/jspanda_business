# How I managed to remote access mysql server on digital ocean droplet

## First follow instructions on 
https://www.digitalocean.com/community/tutorials/how-to-allow-remote-access-to-mysql

# Important findings

```
RENAME USER 'samrullo'@'2400:2412:3c1:8300:540a:68f3:23f0:c6c3' TO 'samrullo'@'softbank060070023127.bbtec.net';
GRANT all ON *.* TO samrullo@'softbank060070023127.bbtec.net' IDENTIFIED BY 'my_password';
```

You would have to run above commands after connecting to mysql server with root account.
By default root user has no password.
If you accidentally set it, you can reset it by running below

```
sudo /usr/sbin/mysqld --skip-grant-tables --skip-networking &
```

## Opening port 3306

It is unsafe to open port 3306 for any remote machine.
But you might have done it for testing purposes.

```
sudo ufw allow from remote_IP_address to any port 3306
sudo ufw allow 3306
```

To remove a certain firewall rule
```buildoutcfg
sudo ufw enable
sudo ufw status numbered
sudo ufw delete {number}

```

## To dump database
```
mysqldump -h <mysql server host> -u <user> -p --databases <database_name> > <dump to filename>.sql
```

Above will prompt for your mysql password

## To import mysql database
After connecting to your mysql server
```
>source <dumped sql file full path>;
```