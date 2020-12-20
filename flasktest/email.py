import os
from socketlabs.injectionapi import SocketLabsClient
from socketlabs.injectionapi.message.basicmessage import BasicMessage
from socketlabs.injectionapi.message.emailaddress import EmailAddress
from flasktest import app, db
from flask import url_for
from flasktest.models import Users, Links, Text
from datetime import date, timedelta


serverId = int(os.environ['MAIL_SERVER_ID'])
injectionApiKey = os.environ['MAIL_API_KEY']
print("Hello world!")

client = SocketLabsClient(serverId, injectionApiKey)

message = BasicMessage()


def send(email, html_mid):
    print(f's.id: {serverId}, injAPI: {injectionApiKey}')
    message.subject = "Confirmation Email"
    message.html_body = f""" <html xmlns="https://www.w3.org/1999/xhtml">

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
                            <h1>Email Confirmation</h1>
                        </td>
                    </tr>
                    <tr>
                        <td>
                            <p>Thank you for using Reminderse! Confirm your email to unlock the full potential of the service.</p>
                        </td>
                    </tr>
                    <tr>
                        <td>
                            <table border="0" cellpadding="0" style="font-size: 14px;">
                                {html_mid}
                            </table>
                        </td>
                    </tr>
                    <tr>
                        <td>
                            <p>
                                If you did not sign up for this service, please delete this email and no confirmations will be made.
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
                            If you do not wish to receive any further emails from us, please unsubscribe.
                        </td>
                        <td align="right">
                            <table border="0" cellpadding="0" cellspacing="0">
                                <tr>
                                    <td>
                                        <a href="https://www.twitter.com/sherzodnimatullo">
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
            """

    message.from_email_address = EmailAddress("no-reply@turtle.nyc")
    message.to_email_address.clear()
    message.to_email_address.append(EmailAddress(email))
    print(message)
    response = client.send(message)
    print(f'Confirmation Email Sent to {email}')
