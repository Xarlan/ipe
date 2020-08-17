# ipe
IPE: Integration Pentest Envinronment

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

### Create user and DB for web-application and 
1. sudo -u postgres psql
2. create database ipe;
3. CREATE USER ipeuser WITH PASSWORD 'ipeuser';
4. \c ipe
5. GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO "ipeuser";
6. \q

## How to develop fronted

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