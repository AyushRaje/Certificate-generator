from django.contrib import admin
import apis.models as m
# Register your models here.
admin.site.register(m.Certificate)

admin.site.register(m.CertificateRequest)

admin.site.register(m.FailedCertificates)