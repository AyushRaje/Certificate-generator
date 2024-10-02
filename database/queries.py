from apis.models import CertificateRequest, Certificate, FailedCertificates

def create_request(email):

    certificate_request = CertificateRequest.objects.create(email=email,status='EXECUTING')
    certificate_request.save()

    return certificate_request

def save_certificate(candidate_name, course_name, course_id, certificate_id, certificate_request_id, is_created, credentials):

    try:
        certificate = Certificate.objects.create(candidate_name = candidate_name, 
                                             course_name = course_name,
                                             course_id =course_id,
                                             certificate_id = certificate_id,
                                             certificate_request_id =certificate_request_id,
                                             is_created = is_created,
                                             credentials = credentials)
    
        certificate.save()
        return True
    except Exception as e:
        print("Exception in save certificate: ",str(e))    
        return False

def save_failed_certificate(certificate_request_id, certificate):

    failed_certificate = FailedCertificates.objects.create(certificate_request_id=certificate_request_id,certificate =certificate)
    failed_certificate.save()

