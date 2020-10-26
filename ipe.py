#!/usr/bin/env python3

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/

import click
import src.webui as webui
from src.db.entities import db
from src.Controllers.user_controller import register_new_user, delete_user as delete_one_user, change_passwd
import uuid
from flask_migrate import init as init_migration, migrate, upgrade, downgrade, current, history, revision as manual_migrate
from config import Config

CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])
server_host = None
server_port = None


@click.group(context_settings=CONTEXT_SETTINGS)
def cli():
    pass


@click.command()
def initdb():
    print("init db")
    with webui.app.app_context():
        upgrade()


@click.command()
def drop_db():
    print("delete all tables in db")
    db.drop_all()


@click.command()
@click.option('--host', help="new user name")
@click.option('--port', help="new user name")
def run(host, port):
    webui.app.debug = True
    global server_host
    global server_port

    if host and not port:
        print("run ipe")
        server_host = host
        webui.app.run(host=host, port=Config.SERVER_PORT)
    elif port and not host:
        print("run ipe")
        server_port = port
        webui.app.run(host=Config.SERVER_HOST, port=port)
    elif port and host:
        server_host = host
        server_port = port
        print("run ipe")
        webui.app.run(host=host, port=port)
    else:
        print("run ipe")
        webui.app.run(host=Config.SERVER_HOST, port=Config.SERVER_PORT)


@click.command()
@click.option('--name', prompt="name", help="new user name")
@click.option('--email', prompt="email", help="new user email")
@click.option('--role', prompt="role", help="new user role: 0 - god, 1 - regular, 2 - viewer")
@click.option('--password', prompt="password", help="new user password", hide_input=True)
def register_user(name, email, password, role):
    register_new_user(str(name), str(email), str(password), int(role))


@click.command()
@click.option("--email", prompt="email", help="user's email")
def delete_user(email):
    delete_one_user(str(email))


@click.command()
@click.option("--email", prompt="email", help="user's email")
@click.option('--password', prompt="password", help="new user password", hide_input=True)
def change_password(email, password):
    change_passwd(str(email), str(password))


@click.command()
def generate_secret_key():
    print(uuid.uuid4().hex)


@click.command()
@click.argument('action')
@click.option('--revision', help="move to this migration")
@click.option('--message', help="comment for migration")
def database(action, revision, message):
    with webui.app.app_context():
        # creates folder /migrations with necessary files for migrations
        if action == "init":
            init_migration()

        # creates migration with current state of models
        elif action == "migrate":
            comment = str(message) if message else ""
            migrate(message=comment)

        # upgrades current state to latest version of database or to defined revision
        elif action == "upgrade":
            if revision:
                upgrade(revision=revision)
            else:
                upgrade()

        # downgrades current state to previous version of database or to defined revision
        elif action == "downgrade":
            if revision:
                downgrade(revision=revision)
            else:
                downgrade()

        # shows current migration
        elif action == "current":
            return current()

        # shows history of migrations until current migration
        elif action == "history":
            return history()

        # creates migration manually with comment = message
        elif action == "create-migration":
            comment = str(message) if message else ""
            return manual_migrate(message=comment)


cli.add_command(initdb)
cli.add_command(drop_db)
cli.add_command(run)
cli.add_command(register_user)
cli.add_command(delete_user)
cli.add_command(change_password)
cli.add_command(generate_secret_key)
cli.add_command(database)


@webui.app.context_processor
def get_server_proto():
    def get_server_proto():
        return Config.SERVER_PROTO

    def get_server_host():
        if server_host and server_port:
            return server_host + ":" + server_port
        elif not server_host and server_port:
            return Config.SERVER_HOST + ":" + server_port
        elif server_host and not server_port:
            return server_host + ":" + Config.SERVER_PORT
        else:
            return Config.SERVER_HOST + ":" + Config.SERVER_PORT

    return dict(get_server_proto=get_server_proto, get_server_host=get_server_host)


if __name__ == '__main__':
    cli()
