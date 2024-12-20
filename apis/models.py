from django.db import models

# Create your models here.
STATUS_CHOICES = (
    ('EXECUTING', 'EXECUTING'),
    ('COMPLETED', 'COMPLETED'),
)

COURSE_IDS=(
    ('CS183D','CS183D'),
)


class CertificateRequest(models.Model):

    id = models.AutoField(primary_key=True, auto_created=True, null=False)

    email = models.EmailField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    status = models.CharField(max_length=100, choices=STATUS_CHOICES)

    report_sent = models.BooleanField(default=False)

class Certificate(models.Model):

    id = models.AutoField(primary_key=True,auto_created=True,null=False)

    roll_no = models.CharField(max_length=100, null=True,blank=True)

    candidate_name = models.CharField(max_length=200, blank=True, null=True)

    course_name = models.CharField(max_length=200,blank=True,null=True)

    course_id = models.CharField(max_length=200,choices=COURSE_IDS,blank=True)

    certificate_id = models.CharField(max_length=100, unique=True)

    created_at = models.DateTimeField(auto_now_add=True)

    certificate_request_id = models.ForeignKey(CertificateRequest,on_delete=models.CASCADE)

    credentials = models.URLField(max_length=300, unique=True, null=True, blank=True)

    drive_link = models.URLField(max_length=500,null=True,blank=True, unique=True)

    is_created = models.BooleanField(default=False)

class FailedCertificates(models.Model):

    id = models.AutoField(primary_key=True)
    
    request_id = models.ForeignKey(CertificateRequest,on_delete=models.CASCADE)

    certificates = models.ForeignKey(Certificate,on_delete=models.CASCADE)

