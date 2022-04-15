# Practical commands

## Connect to database

```
psql -d database -U  user -W
```

Connect to database on another host

```
psql -h host -d database -U user -W
```

## Switch connection to a new database

```
\c dbname username
```

## List databases

```
\l
```

## Create database

```
CREATE DATABASE <new db>
```

## List tables

```
\dt
```

## Describe table

```
\d <table>
```

## List views

```
\dv
```

## Run previous command

```
\g
```

## Help on psql commands

```
\?
```

# PostgreSQL copy database from a server to another

There are several ways to copy a database between PostgreSQL database servers.

If the size of the source database is big and the connection between the database servers is slow, you can dump the source database to a file, copy the file to the remote server, and restore it:

First, dump the source database to a file.

```
pg_dump -U postgres -d sourcedb -f sourcedb.sql
```

Second, copy the dump file to the remote server.

Third, create a new database in the remote server:

```
CREATE DATABASE targetdb;
```

Finally, restore the dump file on the remote server:

```
psql -U postgres -d targetdb -f sourcedb.sql
```

# To restart identity auto increment from a different number

Run below on table id_seq

```
ALTER SEQUENCE shipment_weight
```
