#!/usr/bin/python

"""
Python source code - Developed to
send email or SMS to a list of recipients after a fresh reboot as a
component of the TorilMUD bot Katumi
"""

import smtplib
import tokens
from email.mime.text import MIMEText

def boot_notify():
    msg = MIMEText('Katumi detected a new TorilMUD boot.')
    password = 'password'
    password = tokens.epw
    me = 'example@gmail.com'
    me = tokens.gmail
    you = ('bob@example.com',
            '55566677777@tmomail.net',
            'tom@example')
    you = tokens.elist


    msg['Subject'] = 'TorilMUD reboot/crash:'
    msg['From'] = me
    #msg['To'] = you # commented out to prevent people seeing other addrs

    server = smtplib.SMTP('smtp.gmail.com:587')
    server.starttls()
    server.login(me, password)
    server.sendmail(me, you, msg.as_string())
    server.quit()
