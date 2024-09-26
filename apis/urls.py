from django.urls import path
from apis.views import *
urlpatterns = [
    path("",view=index, name="index"),
]
