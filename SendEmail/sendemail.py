import colorama
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
import getpass
import os
import os.path as op
from pyfiglet import *
import smtplib
import sys
from termcolor import *
import time
import tkinter.filedialog
from tkinter import *

colorama.init()

# Class for implementing the whole functionality of sending emails
class SendingEmail:

    # Clear up the screen
    def clrscr(self):
        try:
            os.system("clear")
        except:
            os.system("cls")

    # Display welcome screen
    def welcome(self):
        SendingEmail().clrscr()
        print("\n\n")
        cprint(figlet_format("Welcome", font='starwars'),"yellow", attrs=["bold"])
        cprint("This is an email client which lets you send plain emails as well as emails with attachments.", "red")
        print("\n\nPlease hit any key to proceed...")
        input()
        time.sleep(2)
    
    # Logging in
    def get_login_details_and_log_in(self):
        global username, password
        SendingEmail().clrscr()
        print("\n")
        cprint(figlet_format("SIGN IN", font='starwars'),"yellow", attrs=["bold"])
        cprint("PLease sign in with your email credentials.", "red")
        print("\n\n")
        username = input("Enter username: ")
        password = getpass.getpass("Enter password: ")
        try:
            # Logging into the gmail server
            server.login(username, password)
        except:
            print("\t\t")
            print(colored("Invalid Username/Password", "red", attrs=["bold"]))
            time.sleep(3)
            SendingEmail().welcome()
            SendingEmail().get_login_details_and_log_in()
        finally:
            print("\t\t")
            print(colored("Login Successful!", "green", attrs=["bold"]))
            time.sleep(1.5)
            SendingEmail().clrscr()
            print(colored("Welcome " + username + "\n\n\n", "blue", attrs=["bold"]))

    # Getting the subject from the user
    def get_subject(self):
        global subject
        subject = input(colored("Enter the subject:\n", attrs=["bold"]))
        print("\n\n")

    # Getting the message from the user
    def get_message(self):
        global body, msg
        msg = MIMEMultipart()
        body = input(colored("Enter your message:\n", attrs=["bold"]))
        while True:
            line = input()
            if line == '':
                break
            body = body + '\n' + line
        print("\n\n")

    # Ask for attachments and attach
    def get_attachments(self):
        global filepaths
        filepaths = []
        while input("Attach a file? Press Y or N: ").lower() == 'y':
            root = Tk()
            filepaths.append(tkinter.filedialog.askopenfilename())
            root.destroy()

    # Getting recipient's address
    def get_recipient_email_id(self):
        global send_to
        send_to = input("\n\nEnter recipient's email addresses (separated by spaces):\n")


if __name__ == "__main__":

    # Establishing connection with the server
    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()

    # Welcome Screen
    SendingEmail().welcome()

    # Enter your username and password to send email
    SendingEmail().get_login_details_and_log_in()

    # Enter the subject
    SendingEmail().get_subject()

    # Enter the message
    SendingEmail().get_message()

    # Attaching files
    SendingEmail().get_attachments()
    for path in filepaths:
        part = MIMEBase("application","octet-stream")
        with open(path,'rb') as file:
            part.set_payload(file.read())
        encoders.encode_base64(part)
        part.add_header('Content-Disposition','attachment;filename="{}"'.format(op.basename(path)))
        msg.attach(part)

    # Enter recipient(s) address(es)
    SendingEmail().get_recipient_email_id()

    # Readying Sender addr + Recipient adds + Subject + Message
    msg['From'] = username
    msg['To'] = send_to
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'html'))

    # Send email
    server.sendmail(username, send_to.split(), msg.as_string())
    
    # Exiting the Program
    time.sleep(1.5)
    SendingEmail().clrscr()
    print(colored("\n\tMail Sent!\n\n", attrs=["bold"]))
    input("Press enter to exit")

    server.quit()
