#!/usr/bin/env python3

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/

import click
import src.webui as webui
from src.db.entities import db
from src.Controllers.user_controller import register_new_user, delete_user as delete_one_user, change_passwd
import uuid

CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])

IPE_RUN_HOST = "0.0.0.0"
IPE_RUN_PORT = "5000"


@click.group(context_settings=CONTEXT_SETTINGS)
def cli():
    pass


@click.command()
def initdb():
    print("init db")
    db.create_all()


@click.command()
def run():
    print("run ipe")
    webui.app.debug = False
    webui.app.run(host=IPE_RUN_HOST, port=IPE_RUN_PORT)


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


cli.add_command(initdb)
cli.add_command(run)
cli.add_command(register_user)
cli.add_command(delete_user)
cli.add_command(change_password)
cli.add_command(generate_secret_key)


if __name__ == '__main__':
    cli()
