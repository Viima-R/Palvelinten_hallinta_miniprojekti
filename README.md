# Setting up a database server and a server where a Flask application runs that connects to the database using Ansible

This work is part of Haaga-Helia university of applied sciences Server Management course.

Operating system used Debian 13.4.0.

# Install guide

1) On your master machine you need to:
- install ssh, ansible and git
- generate ssh key
- copy ssh public key to your slave machines

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

## Demo video (steps 1-4 already done)

https://www.youtube.com/watch?v=BkIeHgBWyX8


# Roles explained

Description on what each role does.

## PostgreSQL

## App
- Installs required packages for Python and virtual environments
- Creates a dedicated application directory at /opt/app
- Sets up a virtual environment (venv)
- Install required Python libraries inside venv
- Creates a service out of the application script (flaski.py), using a template.
- Enables and starts the application as a systemd service.
- Triggers handlers to reload the service if changes made.

End result is it deploys a Flask application, configures it as a systemd service with a virtual environment and required dependencies, ensures it's enabled and running and it connects to the PostgreSQL database.
