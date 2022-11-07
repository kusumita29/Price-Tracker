from bs4 import BeautifulSoup
import requests
import time
import datetime
import smtplib
import ssl
import csv 

def send_mail(title, price, URL): 
    email_sender = 'XXXX@gmail.com'
    email_password = 'XXXXXXXXXXXXXXXX' #App Password
    email_receiver = 'XXXX@gmail.com'

    subject ="Price for " + title + " has dropped"
    body = f"""
    Hi! 
    The price for {title} has dropped to {price}.
    Buy it as soon as possible.
    Link: {URL}
    """

    msg = f"Subject: {subject}\n\n{body}"

    context123 = ssl.create_default_context()

    with smtplib.SMTP_SSL('smtp.gmail.com', 465, context = context123) as smtp:
        smtp.login(email_sender, email_password)
        smtp.sendmail(email_sender, email_receiver, msg)



def check_price(URL, price_bar):
    headers = {"User-Agent": "", "Accept-Encoding":"gzip, deflate", "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8", "DNT":"1","Connection":"close", "Upgrade-Insecure-Requests":"1"}
    
    page = requests.get(URL, headers=headers)
    soup = BeautifulSoup(page.content, "html.parser")

    title = soup.find(id='productTitle').get_text().strip()
    price = soup.find(class_='a-offscreen').get_text().strip()[1:]
    rating = soup.find(class_='a-icon-alt').get_text().split(" ")[0]
    today = datetime.date.today()

    
    data = [title, price, rating, today]

    with open('PriceLog.csv', 'a+', newline='', encoding='UTF8') as f:
        writer = csv.writer(f)
        writer.writerow(data)
 
    if int(price[:-3]) <= price_bar:
        send_mail(title, price, URL)

URL = input("Enter the URL of the Amazon product you want to track: ")
price_bar = int(input("Enter the price below which you want to be notified: "))
track_time = int(input("For how many days do you want to track the prices? "))

total_time_in_secs = track_time * 24 * 60

header = ['Title', 'Price', 'Rating', 'Date']

with open('PriceLog.csv', 'a+', newline='', encoding='UTF8') as f:
    writer = csv.writer(f)
    writer.writerow(header)

while (total_time_in_secs > 0):
    check_price(URL, price_bar)
    time.sleep(1800)
    total_time_in_secs -= 1800