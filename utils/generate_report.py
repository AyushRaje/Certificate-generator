from database.queries import check_certificate_request_for_report,get_certificates_of_request
from utils.convertor import data_to_excel_report_convertor
import threading
import datetime

def background_task(certificate_requests):
    print("Executing Background Task....")
    print(certificate_requests)
    print("Name: Report Generator \n TimeStamp:"+ str(datetime.datetime.now())+"\n")
    for request in certificate_requests.values():
        print(request)
        certificates = get_certificates_of_request(request['id'])
        data_to_excel_report_convertor(certificate_data=certificates,request_email=request['email'])        
    print("Completed Background Task....")    
        

def generate_report_task():
    certificate_requests = check_certificate_request_for_report()
    if certificate_requests is not None:
        thread = threading.Thread(target=background_task, args=(certificate_requests,))
        thread.start()