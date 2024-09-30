from django.urls import path
from apis.views import index, handle_upload
urlpatterns = [
    path("",view=index, name="index"),
    path("upload", handle_upload, name='upload_file'),
]
