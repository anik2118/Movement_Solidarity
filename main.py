import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import asyncio
import os
import re
from dotenv import load_dotenv

import logging
# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Loading all the necessary environment variables
load_dotenv()


"""
sender mail-> your email address
sender_mail_app_passwords->>follow https://www.youtube.com/watch?v=74QQfPrk4vE 
this video will drive to create the app pasword.

"""
sender_email = os.getenv('SENDER_EMAIL')
sender_apppassword = os.getenv('SENDER_APP_PASSWORD')

# Load environment variables
script_dir = os.path.dirname(os.path.abspath(__file__))

# Construct the full path to the receiver list file
receiver_list_path = os.path.join(script_dir, "reciever_list.txt")
with open(receiver_list_path , 'r') as file:
    reciever_list = file.read().splitlines()


class EmailSender:
    def __init__(self, sender_email, sender_apppassword):
        self.sender_email = sender_email
        self.sender_apppassword = sender_apppassword
        self.server = None

    async def connect(self):
        try:
            # Using SMTP_SSL for secure connection
            self.server = smtplib.SMTP_SSL('smtp.gmail.com', 465, timeout=60) 
            self.server.login(self.sender_email, self.sender_apppassword)
            logging.info("Logged in to SMTP server")
        except Exception as e:
            logging.error(f"Failed to connect to SMTP server: {e}")
            self.server = None

    async def disconnect(self):
        if self.server:
            self.server.quit()
            logging.info("Disconnected from SMTP server")

    def validate_email(self, email):
        # checking for valid email address
        regex = re.compile(r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$')
        return re.match(regex, email)

    async def send_email(self, receiver_email, subject, body):
        if not self.server:
            logging.error("SMTP server not connected")
            return

        if not self.validate_email(receiver_email):
            logging.error(f"Invalid email address: {receiver_email}")
            return

        try:
            message = MIMEMultipart()
            message['From'] = self.sender_email
            message['To'] = receiver_email
            message['Subject'] = subject
            message.attach(MIMEText(body, 'html'))

            self.server.sendmail(self.sender_email, receiver_email, message.as_string())
            logging.info(f"Email sent to {receiver_email} from {self.sender_email}")
        except Exception as e:
            logging.error(f"Email can't be sent to {receiver_email} :: error: {e}")

    async def email_body(self, receiver_list):
        logging.info(f"Sending emails from {self.sender_email}")
        body = """
            <!DOCTYPE html>
            <html lang="en">
            <body style="font-family: Arial, sans-serif; line-height: 1.6;">

            <p>Dear Concern,</p>

            <p>I hope this email finds you well.</p>

            <p>I am a common student in Bangladesh, and the students of our country are currently suffering due to the Quota movement. Tragically, a dozen students have already sacrificed their lives, with more lives at risk. University authorities have shut down all universities and are unable to protect their students. Specifically, Dhaka University, Jahangirnagar University, and Rajshahi University are under serious attack.</p>

            <p>Today, students have announced a total shutdown all over the country. I kindly request that you raise your voice on this issue so that we can achieve justice and have the demands of the students fulfilled.</p>

            <p>Your support in bringing this issue to light would mean a great deal to us.</p>

            <p>Thank you for your time and consideration.</p>

            <p>Best regards,<br>
            Student of Bangladesh<br>

            </body>
            </html>                          
        """
        subject = 'Urgent: Raise Your Voice for Bangladeshi Students in the Quota Movement'

        for mail in receiver_list:
            await self.send_email(mail, subject, body)
            # Additional idle time to hit the ratelimit threshold
            await asyncio.sleep(2)  

# Running the asynchronous function
async def run():
    email_sender = EmailSender(sender_email, sender_apppassword)
    await email_sender.connect()
    await email_sender.email_body(reciever_list)
    await email_sender.disconnect()

if __name__ == "__main__":
    asyncio.run(run())