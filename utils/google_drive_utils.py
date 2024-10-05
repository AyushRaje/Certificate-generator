from google.oauth2 import service_account
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.http import MediaFileUpload
import os
import pickle

# Scopes for Google Drive API
SCOPES = ['https://www.googleapis.com/auth/drive']

service = None

def initialize_drive_service():
    """Initialize and return the Google Drive service."""
    global service
    try:
        creds = None
        # The file token.pickle stores the user's access and refresh tokens
        if os.path.exists('token.pickle'):
            with open('token.pickle', 'rb') as token:
                creds = pickle.load(token)

        # If there are no (valid) credentials available, let the user log in.
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    'credentials.json', SCOPES
                )
                creds = flow.run_local_server(port=8080)

            # Save the credentials for the next run
            with open('token.pickle', 'wb') as token:
                pickle.dump(creds, token)

        service = build('drive', 'v3', credentials=creds)
        print("Google Drive service initialized successfully.")
    except Exception as e:
        print(f"Error initializing Google Drive service: {e}")


def get_service():
    return service

# Function to upload a file to Google Drive under a specified folder
def upload_file(service, file_path, base_folder_id):
    try:
        if not service:
            raise Exception("Google Drive service not initialized.")
        
        file_metadata = {
            'name': os.path.basename(file_path),
            'parents': [base_folder_id]  # Specify the base folder ID
        }

        media = MediaFileUpload(file_path, mimetype='application/octet-stream')
        file = service.files().create(body=file_metadata, media_body=media, fields='id').execute()
        file_id = file.get("id")

        # Create the view link for the file
        view_link = f'https://drive.google.com/file/d/{file_id}/view'
        print(f'File uploaded: {file_path}, ID: {file_id}, View Link: {view_link}')
        
        return view_link  # Return the view link of the uploaded file
    except Exception as e:
        print(f"Error uploading file: {e}")
        return None

# Example usage
if __name__ == '__main__':
    drive_service = initialize_drive_service()
    if drive_service:
        # Specify the base folder ID
        base_folder_id = 'YOUR_BASE_FOLDER_ID'  # Replace with the ID of your base folder

        # Specify the file path
        file_path = 'path/to/your/file.txt'  # Replace with your actual file path
        
        # Upload the file to the base folder
        file_link = upload_file(drive_service, file_path, base_folder_id)
        
        if file_link:
            print(f'File can be viewed at: {file_link}')
