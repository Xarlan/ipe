# ipe
IPE: Integrated Pentest Envinronment

Authors:
- [Alexander Ustinov](https://github.com/alustinoff)
- me


This is will be more flexibility tool than [pwnOSINT](https://github.com/Xarlan/pwnOSINT)


## How to prepare Postgresql

### Installing postgresql

1. sudo apt update
2. sudo apt install postgresql postgresql-contrib
3. sudo service postgresql start

### Set password for postgres user
1. sudo passwd postgres

### Create user and DB for web-application
1. sudo -u postgres psql
2. create database ipe;
3. CREATE USER ipeuser WITH PASSWORD 'ipeuser';
4. \c ipe
5. GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO "ipeuser";
6. \q

## How to install this tool
1. $ git clone this project
2. $ cd ipe
3. $ sudo apt install python3-venv python3-dev libcurl4-gnutls-dev librtmp-dev build-essential
4. $ python3 -m venv ./venv
5. $ . venv/bin/activate
6. (venv)$ pip install --upgrade pip
7. (venv)$ pip install -r requirements.txt

## How to run this tool (for release version)
1. In file `config.py` type in your database settings in variable `SQLALCHEMY_DATABASE_URI`
2.  `$ python ipe.py generate-secret-key `  
    Insert the result of command in variable `SECRET_KEY` in file `config.py`
3. In file `config.py` change `SERVER_HOST` and `SERVER_PORT` to your values
4. `$ python ipe.py initdb`
5. Create new user with command:  
    `$ python ipe.py register-user` 
    <pre>
    --name      new user name  
    --email     new user email  
    --role      new user role: 0 - god, 1 - regular, 2 - viewer  
    --password  new user password
    
    Field email is unique for users.
    
    Example:
    $ python ipe.py register-user --name testuser --email test@mail.com --role 1 --password qwerty11
    Success
    
    Or using hiding password via prompt password:
    $ python ipe.py register-user --name testuser --email test@mail.com --role 1
    password:
    </pre>  
    
    If you don't want use HTTPS you can go to step 8.
    
6. Generate self-signet certificate for https
    <pre>
    openssl req -x509 -newkey rsa:4096 -nodes -out ipe_cert.pem -keyout ipe_key.pem -days 365
    </pre>
   Copy 2 resulted files `ipe_cert.pem` and `ipe_key.pem` in directory with file `ipe.py`

7. In file `config.py` change variables like below (only if you done previous step):
    <pre>
    ...
    SESSION_COOKIE_SECURE = True
    REMEMBER_COOKIE_SECURE = True
    ...
    SERVER_PROTO = "https://"
    ...
    IPE_CERT = "ipe_cert.pem"
    IPE_KEY = "ipe_key.pem"
    </pre>

8. `$ python ipe.py run`  
    <pre>
    --host      Host of server. For example: 192.168.1.125
    --port      Port of server. For example: 3333
    
    Default: SERVER_HOST:SERVER_PORT from config.py
    
    You can run ipe with:
    $ python ipe.py run --host <192.168.1.125> --port <3333>
    
    Or just:
    $ python ipe.py run
    </pre>

## Migrating from old version of IPE
1. `python ipe.py database upgrade`

## How to develop frontend

#### Requirements:
1. NodeJS (last stable)
2. npm (last stable)

#### Steps:
1. Go to directory /src/webui/static
2. npm install
3. In first terminal: python ipe.py run 
4. In second terminal: npm run dev
4. before pushing execute "npm run prod"

#### How to release:
1. Create branch release
2. rebase from master
3. npm install --only=production
4. remove folder /src/webui/static/src
5. remove all frontend configs
6. push to release branch