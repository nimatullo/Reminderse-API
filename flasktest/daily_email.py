import smtplib
from datetime import date, timedelta
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from flasktest import db, app
from flasktest.models import Users, Links, Text

from flasktest.email import send_links

import os

# Log into Zoho Mail Server
MAIL_SERVER = 'smtp.zoho.com'
MY_ADDRESS = "hello@reminderse.com"
PASSWORD = os.environ['MAIL_PASSWORD']
s = smtplib.SMTP_SSL(MAIL_SERVER, 465)
s.login(MY_ADDRESS, PASSWORD)


def send_to_each_user():
    app.logger.info("Quering database for users...")
    list_of_users = Users.query.filter_by(email_confirmed=True).all()
    users_sent_to = []

    for user in list_of_users:
        print(f'Getting links for {user.email}')
        links = Links.query.filter_by(user_id=user.id).filter_by(
            date_of_next_send=date.today()).all()

        print(f'Getting texts for {user.email}')
        text = Text.query.filter_by(user_id=user.id).filter_by(
            date_of_next_send=date.today()).all()

        print(f'Found {len(links)} links and {len(text)} texts')
        if len(links) == 0 and len(text) == 0:
            continue

        users_sent_to.append(user)
        move_date(links)
        move_date(text)
        build_email(user.email, links, text)
    return users_sent_to


def move_date(entries):
    for item in entries:
        print("Moving date for entry")
        date = item.date_of_next_send + timedelta(days=int(3))
        item.date_of_next_send = date
        app.logger.info("New date is: " + date.strftime("%m/%d/%y"))
        db.session.commit()


def build_email(email, list_of_links, list_of_texts):
    html_mid = html_links(list_of_links)
    html_mid += html_texts(list_of_texts)
    send_links(email, html_mid)


def html_links(list_of_links):
    '''
    Returns HTML list (<li>) of Links whose date_of_next_send matches today's date.
    '''
    html_mid = ""
    for link in list_of_links:
        html_mid += '''<tr>
                        <td><a style="color: #e96d77;" href="{0}">{1}</a></td>
                    </tr>'''.format(link.url, link.entry_title)
    return html_mid


def html_texts(list_of_texts):
    '''
    Returns HTML list (<li>) of Links whose date_of_next_send matches today's date.
    '''
    html_mid = ""
    for text in list_of_texts:
        url = f'https://reminderse.com/entries'
        html_mid += '''<tr>
                        <td><a style="color: #e96d77;" href="{0}">{1}</a></td>
                    </tr>'''.format(url, text.entry_title)
    return html_mid
