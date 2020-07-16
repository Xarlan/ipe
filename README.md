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