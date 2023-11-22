import csv
import os
from twilio.rest import Client


def make_client() -> Client:
    account_sid = os.environ['TWILIO_ACCOUNT_SID']
    auth_token = os.environ['TWILIO_AUTH_TOKEN']
    client = Client(account_sid, auth_token)
    return client


def mass_sending(filename: str):
    c = make_client()
    with open(filename) as people:
        for person in csv.DictReader(people):
            send(person.get("number"), person.get("name"), person.get("this_year"), c)


# Find your Account SID and Auth Token at twilio.com/console
# and set the environment variables. See http://twil.io/secure
def send(recipient_number: str, gifter_name: str, giftee_name: str, client: Client):
    message_body = f"Dear {gifter_name}, Merry Christmas! This year you're going to be buying a present for {giftee_name}. " \
                   f"Don't forget to put some ideas in the WhatsApp group for your secret Santa! Lots of love, Santa"

    message = client.messages \
                    .create(
                         body=message_body,
                         from_='Santa Kerr',
                         to=recipient_number
                     )

    print(message.sid)


def reminder(recipient_number: str, gifter_name: str, client: Client):
    message_body = f"Dear {gifter_name}, Merry Christmas! There's not long now until the big day, so if you haven't " \
                   f"already done it please tell your Secret Santa what you want via the WhatsApp group. " \
                   f"Lots of love, Santa"
    message = client.messages.create(
        body=message_body,
        from_='Santa Kerr',
        to=recipient_number
    )
    print(message.sid)


def mass_reminder(filename:str):
    c = make_client()
    with open(filename) as people:
        for person in csv.DictReader(people):
            reminder(person.get("number"), person.get("name"), c)


