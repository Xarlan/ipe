#!/usr/bin/env python3

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/

import click
import src.webui as webui

CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])


@click.group(context_settings=CONTEXT_SETTINGS)
def cli():
    pass


@click.command()
def initdb():
    print("init db")


@click.command()
def run():
    print("run ipe")
    webui.app.run()


cli.add_command(initdb)
cli.add_command(run)


if __name__ == '__main__':
    cli()