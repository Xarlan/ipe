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

## How to run this tool
1. In file `config.py` type in your database settings in variable `SQLALCHEMY_DATABASE_URI`
2.  `python ipe.py generate-secret-key `  
    Insert the result of command in variable `SECRET_KEY` in file `config.py`
3. In file `src/webui/static/prod/config.js` type in protocol and host
4. In file `ipe.py` change `IPE_RUN_HOST` and `IPE_RUN_PORT` to your values
5. `python ipe.py initdb`
6. Create new user with command:  
    `python ipe.py register-user`
7. `python ipe.py run`

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