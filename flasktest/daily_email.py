import smtplib
from datetime import date, timedelta
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from flasktest import db
from flasktest.models import Users, Links, Text

# Log into Zoho Mail Server
MAIL_SERVER = 'smtp.zoho.com'
MY_ADDRESS = "no-reply@turtle.nyc"
PASSWORD = "2CsD#U66GHW6"
s = smtplib.SMTP_SSL(MAIL_SERVER, 465)
s.login(MY_ADDRESS, PASSWORD)


def send_to_each_user():
    print("Quering database for users...")
    list_of_users = Users.query.filter_by(email_confirmed=True).all()

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
        move_date(links)
        move_date(text)
        build_email(user.email, links, text)
    return len(list_of_users)


def move_date(entries):
    for item in entries:
        print("Moving date for entry")
        date = item.date_of_next_send + timedelta(days=int(3))
        item.date_of_next_send = date
        print("New date is: " + date.strftime("%m/%d/%y"))
        db.session.commit()


def build_email(email, list_of_links, list_of_texts):
    html_mid = html_links(list_of_links)
    html_mid += html_texts(list_of_texts)
    msg = build_html_body(email, html_mid)
    send(msg)


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


def build_html_body(email, html_mid):
    '''
    Returns MimeText HTML body to be sent out. It uses the <li> from the get_todays_links() function.
    '''
    msg = MIMEMultipart()
    msg['From'] = MY_ADDRESS
    msg['To'] = email
    msg['Subject'] = "Reminder from Reminderse"
    html = """ <html xmlns="https://www.w3.org/1999/xhtml">

<head>
    <meta http-equiv="Content-Type" content="text/html; charset=UTF-8" />
    <meta http-equiv="X-UA-Compatible" content="IE=edge" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0 " />
    <style>
        li {{
                list-style-type: none;
            }}

        * {{
                font-family: Arial, Helvetica, sans-serif;
            }}
    </style>

<body>
    <table align="center" border="0" cellpadding="0" cellspacing="0" width="600">
        <tr>
            <td bgcolor="#341952" align="center">
                <img style="display: block;" width="60%;"
                    src="https://lh3.googleusercontent.com/8kSEzNUGXPy95APnM53fKy1Aec6_r42FFRodgn4RDsKvfdMRCM9tBxzjKkhrax6NHOR8xo-1cON37ZAXmcxlqgId9l-283w0wqGkNQwKIVOk2e5-kVI4YoSDgduSf29Co7dNvQO765o0O4nYjg5DpdUJf4HtF1nbQpkXNj9scOfTjNJ5dtyt3d_j0xKOCiOkXj6Ce0rIeXvWotryvVjxXnzUHuzifYuw5DlXbvuuU-w9zqdf45aBFH36ougCHb4kgSGx6-w0C2bWzfKv9JrNxyykgqTPah5KmiohaGy9Pc35gvdcjLYpJsyjDfBBWr-MI8-8vMQoFH8-au4Ozs1ahSy-OFrkoki1n_eZjw0NM273sqaH-tl0fe18YYN8CUK2yAv-RksfV3Q7N6MClgBXttPwJurN9TRdq-34pm7r4ZrR7BWRIgtwCYBxKf1yppi19x3pPYKSvIDnK_-MuqqbOcB8qjclXK0w6WiO_6dcCcVd_HM8cDHn_2Ie4hnIbrdPDGr0nmaM-CeVGWyKlGlvEE5UgL2oPH8Vb9MOjTjHjDudHJOc0i36400FGsV4oq3s_dXH-l_a9DXcUi7qmboj-KKs4I27sYXZhrGdL9lB55hwytJzDmMah2HYdJKBsw569vayDDsA2ZVpiQQzdMIzrNegdzTOYJUHTnkwmoFAOEPX7FbjYlXX8K0=w1471-h606-no"
                    alt="Reminderse by Turtle Enterprises">
            </td>
        </tr>
        <tr>
            <td bgcolor="#341952" style="padding: 40px 30px 40px 30px;">
                <table border="0" cellpadding="0" cellspacing="0" width="100%" style="color: white;">
                    <tr>
                        <td>
                            <h1>Here are your daily links.</h1>
                        </td>
                    </tr>
                    <tr>
                        <td>
                            <p>You've read these in the past. Don't forget about them.</p>
                        </td>
                    </tr>
                    <tr>
                        <td>
                            <table border="0" cellpadding="0" style="font-size: 14px;">
                                {0}
                            </table>
                        </td>
                    </tr>
                    <tr>
                        <td>
                            <p>
                                If you'd like to make changes to the intervals of any of these links,
                                <a href="https://reminderse.com/entries">click here.</a>
                            </p>
                        </td>
                    </tr>
                </table>
            </td>
        </tr>
        <tr>
            <td bgcolor="#f7f7f7" align="center" style="color:#88898c; padding: 30px 30px 30px 30px;">
                <table border="0" cellpadding="0" cellspacing="0" width="95%">
                    <tr>
                        <td width="75%">
                            &copy; 2020 Reminderse by Turtle Enterprises<br />
                            If you do not wish to receive any further emails from us, please <a href="https://reminderse.com/settings">click here.</a>
                        </td>
                        <td align="right">
                            <table border="0" cellpadding="0" cellspacing="0">
                                <tr>
                                    <td>
                                        <a href="http://www.twitter.com/">
                                            <img src="https://img.icons8.com/android/24/88898c/twitter.png">
                                        </a>
                                    </td>
                                    <td style="font-size: 0; line-height: 0;" width="20">&nbsp;</td>
                                    <td>
                                        <a href="https://www.instagram.com/sherzodnimatullo">
                                            <img src="https://img.icons8.com/android/24/88898c/instagram-new.png">
                                        </a>
                                    </td>
                                </tr>
                            </table>
                        </td>
                    </tr>
                </table>
            </td>
        </tr>
    </table>
</body>
</head>
            """.format(html_mid)

    msg.attach(MIMEText(html, 'html'))
    return msg


def send(message):
    '''
    Sends MimeText Message to email.
    '''
    s.send_message(message)
    print("Links and Text email sent to user.")
