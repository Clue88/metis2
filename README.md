# Metis

### Configuration
Set up a user account with sudo privileges.
```
$ ssh root@<server-ip> // then enter your password
$ adduser --gecos "" ubuntu
$ usermod -aG sudo ubuntu
```
You can now log out of root. Next, secure the server with password-less logins.

If you don't have RSA keys, generate them on your host computer:
```
$ ssh-keygen
```
Then copy the public key to the server and remove password logins.
```
$ ssh-copy-id ubuntu@<server-ip>
$ ssh ubuntu@<server-ip> // then enter your password
$ sudo nano /etc/ssh/sshd_config // set PermitRootLogin and PasswordAuthentication to no, then press ⌘X then Y to save.
$ sudo service ssh restart
```

Install a firewall.
```
$ sudo apt-get install -y ufw
$ sudo ufw allow ssh
$ sudo ufw allow http
$ sudo ufw allow 443/tcp
$ sudo ufw --force enable
$ sudo ufw status
```

### Installation
Install the required system dependencies.
```
$ sudo apt-get -y update
$ sudo apt-get -y install python3 supervisor nginx git
$ sudo apt-get -y install postgresql
$ sudo apt-get -y install python3-pip
$ pip3 install virtualenv
```

Install Metis.
```
$ git clone https://github.com/Clue88/metis2.git
$ cd metis2
$ virtualenv env
$ source ./env/bin/activate
$ pip3 install -r requirements.txt
```

Write the following to `.env`:
```
SECRET_KEY=<A-SECRET-KEY>
DATABASE_URL="postgresql:///metis"
```
You can generate a secret key with the following:
```python3 -c "import uuid; print(uuid.uuid4().hex)"```

Define the flask app.
```
$ echo "export FLASK_APP=metis.py" >> ~/.profile
```

### PostgreSQL Setup
```
$ sudo su - postgres
$ createuser ubuntu
$ createdb -O ubuntu metis // use ⌘D to exit
```

Test that the database is working.
```
$ flask db upgrade
```

### Gunicorn and Supervisor Setup
```
$ sudo cp deployment/supervisor/metis.conf /etc/supervisor/conf.d
$ sudo supervisorctl reload
```

### Nginx Setup
Certs should be put into the `/certs` directory as `cert.pem` and `key.pem`.
Follow the instructions on https://certbot.eff.org/lets-encrypt/ubuntufocal-nginx.
```
$ sudo cp deployment/nginx/metis /etc/nginx/sites-enabled
$ sudo service nginx reload
```

### Deploying Updates
```
(venv) $ git pull
(venv) $ sudo supervisorctl stop metis
(venv) $ flask db upgrade
(venv) $ sudo supervisorctl start metis
```
