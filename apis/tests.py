
from django.test import TestCase
from django.core.mail import EmailMessage
class EmailSendingTestCase(TestCase):
    
    def test_send_email(self):
        subject = "Test Email Subject"
        message = "This is a test email message."
        from_email = "ayush.raje3153@gmail.com"  # Replace with your email
        recipient_list = ["ayush.raje315@gmail.com"]  # Replace with a real recipient
        
        # Send the email
        mail = EmailMessage(subject, message, from_email, recipient_list)
        mail.send()

