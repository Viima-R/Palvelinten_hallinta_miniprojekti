# Setting up a database server and a server where a Flask application runs that connects to the database using Ansible

This work is part of Haaga-Helia university of applied sciences Server Management course.

Operating system used Debian 13.4.0.

# Install guide

1) On your master machine you need to:
- install ssh, ansible and git

```
sudo apt update
sudo apt install -y openssh-server git ansible
```

- generate ssh key

```
ssh-keygen -t ed25519
```

- copy ssh public key to your slave machines, make sure you copy the .pub key

```
ssh-copy-id user@slave-machine ~/.ssh/id_ed25519.pub
```

2) On your slave machine you need to:
- install ssh
- have sudo access

3) Clone this repository to your master machine.

```
git clone git@github.com:Viima-R/Palvelinten_hallinta_miniprojekti.git
```

4) Make following changes in the repository you cloned.
- Modify hosts.ini to match the user@ip of your slave machines
- Modify group_vars/all.yml you need to change "postgresql_ip: "192.168.1.235"" to match your database server ip.
- You may also change other variables in group_vars/all.yml like database name, password and timezones.
- Modify roles/postgresql/files/pg_hba.conf you need to change the line in the bottom row to match: your database name, database user, and app server ip.
```
host    db_name        db_user            192.168.1.69/32        scram-sha-256
```
Dont remove the /32!


5) Run ansible playbook in the ansible directory of the cloned repository.

```
ansible-playbook -i hosts.ini site.yml -K
```

6) Test that everything works

In the browser of your app server enter.
```
http://127.0.0.1:5000
```
This shows if your webserver is up, after you've confirmed your webserver is up enter.
```
http://127.0.0.1:5000/data
```
This shows if your app connects to the database, it displays the configured time in the database.

## Demo video (steps 1-4 already done)

https://www.youtube.com/watch?v=BkIeHgBWyX8


# Roles explained

Description on what each role does.

## PostgreSQL
- Installs PostgreSQL packages and makes sure it is running
- Ensures that the user, database and required privileges exist
- Sets listen addresses and ports
- Sets a timezone for the database and logs
- Adds a copy of the configuration file pg_hba.conf
- Installs nftables and makes sure it is running
- Adds a copy of the nftables configuration file

End result is that it sets up a working PostgreSQL server with the required database configuration, local-only listening, timezone settings and firewall rules.

## App
- Installs required packages for Python and virtual environments
- Creates a dedicated application directory at /opt/app
- Sets up a virtual environment (venv)
- Install required Python libraries inside venv
- Creates a service out of the application script (flaski.py), using a template.
- Enables and starts the application as a systemd service.
- Triggers handlers to reload the service if changes made.

End result is it deploys a Flask application, configures it as a systemd service with a virtual environment and required dependencies, ensures it's enabled and running and it connects to the PostgreSQL database.



# Sources

- https://terokarvinen.com/
- https://docs.ansible.com/projects/ansible/latest/index.html

## Acknowledgements
ChatGPT (OpenAI GPT-5.3) was asked for assistance in code suggestions and explanations.
