from django.urls import path
from apis.views import index, handle_upload,verify_certificate,get_request_status
urlpatterns = [
    path("",view=index, name="index"),
    path("upload", handle_upload, name='upload_file'),
    path('verify/<str:certificate_id>/', verify_certificate, name='verify certificate'),
    path('status/',get_request_status,name='get_request_status'),
]
