import json
import socket
import requests
import smtplib
import sched, time
import sys
from websocket import create_connection

ws = create_connection("ws://127.0.0.1:9195/")
s = sched.scheduler(time.time, time.sleep)
smtp_pwd = ""
smtp_user = "notification@sophiatx.com"
smtp_server = "localhost"
email_array = ["matus.kysel@sophiatx.com"]
config = json.load(open("config.json", "r"))

def get_balance(account):
    ws.send(json.dumps({"jsonrpc": "2.0", "method": "get_account_balance", "params":[str(account)], "id": 0 }))
    return round(float(json.loads(ws.recv())["result"]) / 1000000, 6) 

def send_email(subject, msg):
    server = smtplib.SMTP(smtp_server)
    server.ehlo()
    # server.starttls()
    # server.login(smtp_user, smtp_pwd)
    for account in email_array:
        msg_out = "\r\n".join([
          "From: " + smtp_user,
          "To: " + account,
          "Subject: " + subject,
          "",
          str(msg)
          ])
        server.sendmail(smtp_user, account, msg_out)
    server.quit()

def run_bot():
    msg = ""
    for account in config:
        if(get_balance(account["name"]) < account["trash_hold"]):
            msg = account["name"] + " balace is under " + str(account["thrash_hold"]) + 
            " (" +str(get_balance(account["name"])) + ") \n"

    if(msg != ""):
        send_email("One or more accounts have no enought tokens", msg)


if __name__ == "__main__":
    s.enter(1, 1, run_bot)
    s.run()
