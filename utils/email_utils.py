import threading
from django.core.mail import EmailMessage
from decouple import config

def send_email_with_attachment(subject, message, recipient_list, file_path):
    email = EmailMessage(subject, message, config('HOST_EMAIL'), recipient_list)
    
    # Attach the file
    with open(file_path, 'rb') as file:
        email.attach(file.name, file.read(), 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')  # Change 'application/pdf' to your file type
    
    email.send()

def send_email_thread(subject, message, recipient_list, file_path):
    # Create a thread to send the email
    email_thread = threading.Thread(target=send_email_with_attachment, args=(subject, message, recipient_list, file_path))
    email_thread.start()
