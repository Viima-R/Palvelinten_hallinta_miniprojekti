# Setting up a database server using infrastructure as code

This work is part of Haaga-Helia university of applied sciences Server Management course.

Work was done with Ansible on Debian 13.4.0 using PostgreSQL.

## First manually

### Install PostgreSQL

First we install PostgreSQL server, client tools and extra utilities.

```
sudo apt update
sudo apt install postgresql postgresql-contrib -y
```

Check if PostgreSQL is running and enabled, so it starts on boot.

```
sudo systemctl status postgresql
```

<img width="815" height="74" alt="Image" src="https://github.com/user-attachments/assets/3f588db4-9023-48d0-a6f7-de64a9ca99ab" />

Start/enable if PostgreSQL is not active and enabled.

```
sudo systemctl start postgresql
sudo systemctl enable postgresql
```

### Create database, user and grant privileges for user

Access PostgreSQL shell with the user postgres.

```
sudo -u postgres psql
```

Your command prompt should look like this: postgres=#

In the prompt use the following query to create database.

```
CREATE DATABASE projekti;
```

Next create a user.

```
CREATE USER mini WITH ENCRYPTED PASSWORD 'omitted';
```

Set encoding to UTF8, this prevents character issues.

```
ALTER ROLE myuser SET client_encoding TO 'utf8';
```

Set timezone

```
SET timezone TO 'Europe/Helsinki';
```

Give privileges.

```
GRANT ALL PRIVILEGES ON DATABASE mydb TO myuser;
```
