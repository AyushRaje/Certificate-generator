from database.queries import check_certificate_request_for_report,get_certificates_of_request
from utils.convertor import data_to_excel_report_convertor
from utils.email_utils import send_email_with_attachment
import threading
import datetime
from decouple import config


def background_task_for_report(certificate_requests):
    print("Executing Background Task....")
    print(certificate_requests)
    print("Name: Report Generator \n TimeStamp:"+ str(datetime.datetime.now())+"\n")
    
    for request in certificate_requests:
        print(request)
        certificates = get_certificates_of_request(request.id)
        report_location, certifcates_generated = data_to_excel_report_convertor(certificate_data=certificates,request_email=request.email)
        failed_certificates = 0 
        if len(report_location):
            request.report_sent = True
            request.save()    
            print("Executing Background Task....")
            print("Name: Sending Email \n TimeStamp:"+ str(datetime.datetime.now())+"\n")
            print("Host Mail: ",config('HOST_EMAIL'))
            send_email_with_attachment(
                subject="Certificate Report",
                message= f"""This is a system generated message.Please do not reply it.\nYour certificate generation request has been completed successfully.\n
                Total Certificate Generated: {certifcates_generated} \n
                Failed Certificates: {failed_certificates} \nA Complete report is attached with this email including credentials of the certificates.""",
                recipient_list=[request.email],
                file_path=report_location
            )
            print("Completed Background Task....")    
    print("Completed Background Task....")

   


        

def generate_report_task():
    certificate_requests = check_certificate_request_for_report()
    if certificate_requests.exists():
        thread = threading.Thread(target=background_task_for_report, args=(certificate_requests,))
        thread.start()