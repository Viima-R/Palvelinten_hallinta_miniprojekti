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

Access PostgreSQL shell using the user postgres.

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
GRANT ALL PRIVILEGES ON DATABASE projekti TO mini;
```

Exit PostgreSQL shell
```
\q
```

### Configure PostgreSQL

PostgreSQL configuration is in /etc/postgresql/17/main/postgresql.conf 

Change the timezones to match yours.

```
log_timezone = 'Europe/Helsinki'
timezone = 'Europe/Helsinki'
```

We're using the database locally for now so use the following.

```
listen_addresses = 'localhost'
```

Keep all others default for now.

We could also configure which addresses have access to the database in /etc/postgresql/17/main/pg_hba.conf but we are only running locally for now so keep the defaults.

Since we made changes to the configuration files, we need to restart PostgreSQL

```
sudo systemctl restart postgresql
```

### Open port for PostgreSQL


Check if nftables is on and enabled.

```
sudo systemctl status nftables
```

Start and enable if it's not.

```
sudo systemctl start nftables
sudo systemctl enable nftables
```

Lets create a ruleset for our use, replace micro with the text editor you use.

```
sudo micro /etc/nftables.conf
```

And enter configuration that allows for local traffic, SSH, PostgreSQL locally and drop everything else.

```
table inet filter {
  chain input {
    type filter hook input priority 0;

    # Allow loopback
    iif lo accept

    # Allow established/related traffic
    ct state established,related accept

    # Allow SSH 
    tcp dport 22 accept

    # Allow PostgreSQL locally
    ip saddr 127.0.0.1 tcp dport 5432 accept

    # Drop everything else inbound
    drop
  }

  chain output {
    type filter hook output priority 0;
    accept
  }
}
```

Restart nftables

```
sudo systemctl restart nftables
```

### Testing connection

Lets connect to the database we created in localhost with the user we created.

```
psql -h localhost -U mini -d projekti
```

It will then prompt you for a password and then you're in.

<img width="545" height="163" alt="kuva" src="https://github.com/user-attachments/assets/9e58b1ca-211e-4792-9da8-e1fddbe2b5e8" />
