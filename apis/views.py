from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
import pandas as pd
import json
from utils.create_certificates import run_script
import subprocess
from threading import Thread
import ast
from database.queries import get_certificate_from_certificate_id, get_all_certificate_requests, get_certificate_requests_from_email
# Create your views here.

def index(request):
    return render(request,'index.html')

@api_view(['POST'])
def handle_upload(request):
    if 'file' not in request.FILES or 'dictionary' not in request.data:
        return Response({'error': 'File and dictionary are required.'}, status=status.HTTP_400_BAD_REQUEST)

    file = request.FILES['file']
    file_name = file.name.lower()
    try:
        if file_name.endswith('.csv'):
            df = pd.read_csv(file)
        elif file_name.endswith(('.xls', '.xlsx')):
            df = pd.read_excel(file)
        else:
            return Response({'error': 'Invalid file format. Only CSV or Excel files are allowed.'}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({'error': f'Failed to read the file: {str(e)}'}, status=status.HTTP_400_BAD_REQUEST)
    try:
        dictionary = json.loads(request.data['dictionary'])
    except json.JSONDecodeError:
        return Response({'error': 'Invalid dictionary format. Please provide a valid JSON object.'}, status=status.HTTP_400_BAD_REQUEST)
    
    
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
        data = certificate.values('candidate_name','roll_no','course_name','course_id')
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






