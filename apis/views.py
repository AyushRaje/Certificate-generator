from django.shortcuts import render
from rest_framework.decorators import api_view, parser_classes
from rest_framework.response import Response
from rest_framework import status
import pandas as pd
import json
from utils.create_certificates import run_script
import subprocess
from rest_framework.parsers import MultiPartParser, FormParser
from threading import Thread
import ast
from database.queries import get_certificate_from_certificate_id, get_all_certificate_requests, get_certificate_requests_from_email
from io import StringIO
# Create your views here.

def index(request):
    return render(request,'index.html')

@api_view(['POST'])
@parser_classes([MultiPartParser, FormParser])
def handle_upload(request):

    try:
        if request.method == 'POST':
            
            file = request.FILES['file']
            dictionary = request.POST['dictionary']
    except Exception as e:
        return Response("Error: "+str(e),status=status.HTTP_200_OK)        

    df = pd.read_excel(file)
    thread = Thread(target=run_script, args=(df,dictionary))
    thread.start()
    email = ast.literal_eval(dictionary).get('email')
    data = {
        'email': email,
        'message': 'The certificate generation has started, you will receive the reports and certificates in the email',
        'certificates_requested':len(df[['NAME']])
    }
    # print(df)

    return Response(data, status=status.HTTP_200_OK)

@api_view(['GET'])
def verify_certificate(request, certificate_id):
    message = f"Certificate with {certificate_id} is not found or is invalid."
    data = {}
    certificate = get_certificate_from_certificate_id(certificate_id=certificate_id)
    if certificate is None:
        response_status = status.HTTP_404_NOT_FOUND
    else:
        message=f"Certificate found and is valid."
        data = certificate.values('candidate_name','created_at','course_name','course_id','drive_link')
        response_status = status.HTTP_202_ACCEPTED

    return Response({
        'data':data,
        'message':message
    },status=response_status)

@api_view(['GET'])
def get_request_status(request):
    response_status = status.HTTP_202_ACCEPTED
    data= {}
    message="Requests Found"
    email = request.query_params.get('email',None)
    if email is None:
        certificate_requests = get_all_certificate_requests()
        data = certificate_requests.values('email','created_at', 'report_sent','status').order_by('-created_at')
    else:
        certificate_requests = get_certificate_requests_from_email(email=email)
        if certificate_requests is None:
            message = "No Requests with this email"
            response_status =  status.HTTP_204_NO_CONTENT
        else:
            data = certificate_requests.values('created_at', 'report_sent','status').order_by('-created_at')

    return Response({
        'message': message,
        'data':data,

    },status=response_status)         






