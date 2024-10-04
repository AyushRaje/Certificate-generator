from apis.models import CertificateRequest, Certificate, FailedCertificates

def create_request(email):

    certificate_request = CertificateRequest.objects.create(email=email,status='EXECUTING')
    certificate_request.save()

    return certificate_request

def save_certificate(candidate_name, course_name, course_id, certificate_id, certificate_request_id, is_created, credentials,roll_no):

    try:
        certificate = Certificate.objects.create(candidate_name = candidate_name, 
                                             course_name = course_name,
                                             course_id =course_id,
                                             certificate_id = certificate_id,
                                             certificate_request_id =certificate_request_id,
                                             is_created = is_created,
                                             credentials = credentials,
                                             roll_no=roll_no)
    
        certificate.save()
        return True
    except Exception as e:
        print("Exception in save certificate: ",str(e))    
        return False

def save_failed_certificate(certificate_request_id, certificate):

    failed_certificate = FailedCertificates.objects.create(certificate_request_id=certificate_request_id,certificate =certificate)
    failed_certificate.save()


def check_certificate_request_for_report():
    cetificate_requests = CertificateRequest.objects.filter(status='COMPLETED',report_sent=False)
    return cetificate_requests

def get_certificates_of_request(certificate_request):
    certificate_list = Certificate.objects.filter(certificate_request_id = certificate_request, is_created=True)
    return list(certificate_list.values())