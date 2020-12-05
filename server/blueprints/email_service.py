from flask import Blueprint, request, render_template
import smtplib
import ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

email_service = Blueprint('emailer', __name__, template_folder='templates')


@email_service.route('/submit-form', methods=["POST"])
def send_email():

    # Get form data
    data = request.get_json() or request.form
    name = data["name"]

    # Configure the emailer, first setting sender and receiver to business
    port = 465
    smtp_server = "mail.optonline.net"
    sender = "mimspainting@optonline.net"
    receiver = "mimspainting@optonline.net"
    password = "#"

    # Create message from form message to send to business
    text = f'{data["message"]}\n\n\
        {data["name"]}\n\
        {data["email"]}\n\
        {data["pref"]}'
    message = MIMEMultipart()
    message["Subject"] = "Message from MFP Website"
    message["From"] = sender
    message["To"] = receiver
    message.attach(MIMEText(text, 'plain'))
    context = ssl.create_default_context()

    with smtplib.SMTP_SSL(smtp_server, port, context=context) as emailer:
        emailer.login(sender, password)
        emailer.sendmail(sender, receiver, message.as_string())

    # Create auto-reply to confirm that client's message did send
    # Will try to send html first; send text if not possible
    reply = MIMEMultipart("alternative")
    receiver = data["email"]
    reply["Subject"] = "MFP Got Your Message!"
    reply["From"] = sender
    reply["To"] = receiver
    text = f'Hi {data["name"]},\n\n \
        Thank you for contacting us at Mims Family Painting. We will review\
        your message and reply to you within 2 business days (Monday - Friday) by {data["pref"]}.\n\n \
        We look forward to speaking with you soon.\n\n \
        Best regards,\n \
        Mims Family Painting'
    html = """\
    <html>
        <head>
            <style>
                html {{
                    background: black;
                    color: white;
                }}
            </style>
        </head>
        <body>
            <p>Hi {name},</p>
            <p>
                Thank you for contacting us at Mims Family Painting. We will review\
                your message and reply to you within 2 business days (Monday - Friday) by {pref}.
            </p>
            <p>
                We look forward to speaking with you soon.
            </p>
             <p>
                Best regards,
            </p>
             <p>
                Mims Family Painting
            </p>
        </body>
    </html>
    """.format(name=data["name"], pref=data["pref"])

    part1 = MIMEText(text, "plain")
    part2 = MIMEText(html, "html")

    reply.attach(part1)
    reply.attach(part2)

    with smtplib.SMTP_SSL(smtp_server, port, context=context) as emailer:
        emailer.login(sender, password)
        emailer.sendmail(sender, receiver, reply.as_string())

    return render_template('results.html', name=name or None, userData=data or None)
