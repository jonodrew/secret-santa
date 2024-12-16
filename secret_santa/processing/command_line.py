import csv

import click
from twilio.rest import Client

from secret_santa.processing.run import generate_matches
from send import send, reminder


@click.command()
@click.argument("year")
def secret_santa(year: int):
    matches = generate_matches(f"{year}-participants.csv")
    if click.confirm("Do you want to send these pairings?", abort=True):
        account_sid = click.prompt("Enter Twilio SID")
        auth_token = click.prompt("Enter Twilio auth token", hide_input=True)
        client = Client(account_sid, auth_token)
        if click.confirm("Definitely sending these, right?", abort=True):
            for match in matches:
                send(match.number, match.name, match.this_year, client)
        click.echo("Secret! Santa!")


@click.command
@click.argument("year")
def reminder(year: int):
    if click.confirm("Do you want to send these pairings?", abort=True):
        account_sid = click.prompt("Enter Twilio SID")
        auth_token = click.prompt("Enter Twilio auth token", hide_input=True)
        client = Client(account_sid, auth_token)
        if click.confirm("Definitely sending these, right?", abort=True):
            with open(f"{year}-participants.csv", "r") as people:
                for person in csv.DictReader(people):
                    reminder(person.get("number"), person.get("name"), client)
        click.echo("Secret! Santa!")
