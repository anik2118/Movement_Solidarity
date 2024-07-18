import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import asyncio

import logging
# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Load environment variables

with open(r"Quota_movement\sender_list.txt", 'r') as file:
    reciever_list = file.read().splitlines()
"""
sender mail-> your email address
sender_mail_app_passwords->>follow https://www.youtube.com/watch?v=74QQfPrk4vE 
this video will drive to create the app pasword.

"""
sender_email="Your email address"
sender_apppassword=" your app password "


class EmailSender():
    def __init__(self):
        super().__init__()
    async def email_body(self, sender_email, password, receiver_list):
        logging.info(f"Sending emails from {sender_email}")
        for mail in receiver_list:

            body = f"""
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
  student of Bangladesh<br>

</body>
</html>                          
                """           
                         
            subject = 'Urgent: Raise Your Voice for Bangladeshi Students in the Quota Movement '
            try:
                message = MIMEMultipart()
                message['From'] = sender_email
                message['To'] = mail
                message['Subject'] = subject
                message.attach(MIMEText(body, 'html'))               
                server = smtplib.SMTP('smtp.gmail.com', 587, timeout=60)
                server.starttls()
                server.login(sender_email, password)
                server.sendmail(sender_email, mail, message.as_string())
                server.quit()
                await asyncio.sleep(1)
                logging.info(f"Email sent to {mail} from {sender_email}")
            except Exception as e:
                logging.error(f"Email can't be sent to {mail} :: error: {e}")

# Running the asynchronous function
async def run():
    email_sender = EmailSender()
    await email_sender.email_body(sender_email,sender_apppassword,reciever_list)
if __name__ == "__main__":
    asyncio.run(run())

    
