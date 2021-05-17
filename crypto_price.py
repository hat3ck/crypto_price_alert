import yfinance as yf
import pandas as pd
import time
import math
import ftplib
import os
import re
import time
import sys
import time
import smtplib
import numpy as np
from datetime import datetime
pd.set_option('max_rows', 99999)
pd.set_option('max_colwidth', 99999)



method = input("""set method for checking the price
'min' for alerting when the price reaches a low point
'max' for alerting when price reaches a high point
(your input): """).lower()

while(method not in ['min','max']):
    print("your input is incorrect please try again!")
    method = input("""set method for checking the price
    'min' for alerting when the price reaches a low point
    'max' for alerting when price reaches a high point
    (your input): """).lower()


# set ticker and price
ticker = input("""please find the symbol for your crypto in finance.yahoo.com
i.e ADA-USD
(your input): """).upper()
data = yf.download(ticker, period = '1d', interval='1m', progress = False,  threads= False)
while(data.empty):
    print("symbol not found, please try again later!")
    ticker = input("""please find the symbol for your crypto in finance.yahoo.com
    i.e ADA-USD
    (your input): """).upper()
    data = yf.download(ticker, period = '1d', interval='1m', progress = False,  threads= False)

price = input("""please enter your target price
(your input): """)
while (not price.replace('.','',1).isnumeric()):
    print("please check your entry, the price is not acceptable!")
    price = input("""please enter your target price
    (your input): """)

interval = input("""please enter the frequency of every check in seconds (for example if you enter 10 it will check the price every 10 seconds)
(your input): """)
while (not interval.isnumeric()):
    print("your input was incorrect please try again!")
    interval = input("""please enter the frequency of every check in seconds (for example if you enter 10 it will check the price every 10 seconds)
    (your input): """)

print("""
    ######### This part is to send email #################
 In order for this to work you need to enable 2factor authentication and set up an app password for this program in your gmail account.
 Otherwise you might get a "critical security alert" when gmail detects that a non-Google apps is trying to login your account.
""")
email_setup = input("""Do you want to set up an email?(Y/N)
(your input): """)

if(email_setup.upper() == 'Y'):
    gmail_user = input("""please enter your gmail user
    (your input): """)
    gmail_password = input("""please enter your Gmail's app password ( password is different for less secure apps once you set it up you'll have access to it)
    (your input): """)
    to = input("""please enter your receipiant's emaill address if more than one separate them by ',' (i.e. username@mail.com,username@gmail.com).
    (your input): """).split(",")
    to = list(to)
    sent_from = gmail_user

print("""program is working!
Once the target price reaches, you'll get an alert!""")
def get_price(ticker):
  data = yf.download(ticker, period = '1d', interval='1m', progress = False,  threads= False)
  return(data.iloc[-1,:]['Close'])
def check_price(ticker, interval, x):
  #interval for each try
    time.sleep(int(interval))
    try:
      return(get_price(ticker))
    except:
      return(x)

if(method=='min'):
    x =1000000000000000000000000000000000
    while (x > float(price)):
        x = check_price(ticker, interval, x)
elif(method=='max'):
    x = 0
    while (x < float(price)):
        x = check_price(ticker, interval, x)

print("price of {} at {} is: {}".format(ticker, datetime.now(), x))

if(email_setup.upper() == 'Y'):
    subject = "Price Alert for {}".format()
    body = "The price of {} is {} \n\n- You".format(ticker, x)
    message = 'Subject: {}\n\n{}'.format(subject, body)
    try:
        server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        server.ehlo()
        server.login(gmail_user, gmail_password)
        server.sendmail(sent_from, to, message)
        server.close()

        print('Email sent!')
    except:
        print("""Failed to send the email!
        please check your email credentials""")
