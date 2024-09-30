from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework.parsers import MultiPartParser, FormParser
import pandas as pd
import json
from utils.create_certificates import run_script
import subprocess
from threading import Thread
# Create your views here.

def index(request):
    return render(request,'index.html')

@api_view(['POST'])
def handle_upload(request):
    parser_classes = (MultiPartParser, FormParser)

    # Check if 'file' and 'dictionary' are provided in the request
    if 'file' not in request.FILES or 'dictionary' not in request.data:
        return Response({'error': 'File and dictionary are required.'}, status=status.HTTP_400_BAD_REQUEST)

    # Read the file (either CSV or Excel)
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

    # Parse the dictionary from the request
    try:
        dictionary = json.loads(request.data['dictionary'])
    except json.JSONDecodeError:
        return Response({'error': 'Invalid dictionary format. Please provide a valid JSON object.'}, status=status.HTTP_400_BAD_REQUEST)

    # Response containing both data from file and dictionary
    
    
    thread = Thread(target=run_script, args=(df,dictionary))
    thread.start()

    data = {
        'message': 'The certificate generation has started, you will receive the reports and certificates in the email'
    }
    # print(df)

    return Response(data, status=status.HTTP_200_OK)

