from argparse import ArgumentParser as ap
from base64 import b64decode as bd
from configparser import ConfigParser as cp
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
import os
from selenium import webdriver
import smtplib
import time
import warnings
warnings.filterwarnings("ignore")


def parser():
    parser = ap()
    parser.add_argument('-r', '--receiver', default="2707.swati@gmail.com", \
        help="Receiver's email address")
    arg = parser.parse_args()
    return arg

def fetch_creds():
    script_dir = os.path.dirname(__file__)
    conf_file_path = os.path.join(script_dir, "conf.ini")
    conf = cp()
    conf.read(conf_file_path)
    uname = conf.get('email', 'uname')
    pwd = conf.get('email', 'pwd')
    pwd = bd(pwd).decode("utf-8")
    return uname, pwd

def get_current_value(search_text):
    url = "https://www.google.com"
    driver = webdriver.Chrome(r'chromedriver.exe')
    driver.get(url)
    time.sleep(2)
    driver.find_element_by_xpath('//*[@id="tsf"]/div[2]/div[1]/div[1]/div/div[2]/input').send_keys(search_text)
    time.sleep(2)
    try:
        driver.find_element_by_xpath('//*[@id="tsf"]/div[2]/div[1]/div[2]/div[2]/ul/li[1]/div/div[2]/div[1]/span').click()
    except:
        driver.find_element_by_xpath('//*[@id="tsf"]/div[2]/div[1]/div[2]/div[2]/ul/li[1]/div/div[2]/div[1]/div[2]/span').click()
    time.sleep(2)
    amount = driver.find_element_by_xpath('//*[@id="knowledge-currency__updatable-data-column"]/div[1]/div[2]/span[1]')
    return amount.text

def send_email(user, passwrd, amt, receiver):
    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    server.login(user, passwrd)
    msg = MIMEMultipart()
    msg['From'] = user
    msg['To'] = receiver
    msg['Subject'] = "$1 = " + amt
    msg.attach(MIMEText("$1 = " + amt))
    server.send_message(msg)
    server.quit()


if __name__ == "__main__":
    arg = parser()
    user, passwrd = fetch_creds()
    if arg.receiver:
        receiver = arg.receiver
    amt = get_current_value("USD to INR")
    send_email(user, passwrd, amt, receiver)
