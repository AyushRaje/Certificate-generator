import pythoncom
import shutil
import tempfile
import os
from pptxtopdf import convert
import pandas as pd
from datetime import datetime
from utils.google_drive_utils import upload_file
from decouple import config
from utils.google_drive_utils import get_service

def ppt_to_pdf_convertor(input_file, output_path):
    # Create a temporary directory for copying the input file
    with tempfile.TemporaryDirectory() as temp_dir:
        # Create a unique copy of the input file in the temporary directory
        temp_input_file = os.path.join(temp_dir, os.path.basename(input_file))
        shutil.copy2(input_file, temp_input_file)

        # Set the output file path in the specified directory (current working directory in this case)
        output_file = os.path.join(output_path)

        # Initialize COM
        pythoncom.CoInitialize()
        
        try:
            # Convert using the temporary input file and save the output to the specified directory
            created_output_file_path = convert(temp_input_file, output_file)
            print(f"File successfully converted to '{output_file}'")
            print(created_output_file_path)
            print("Uploading file to drive.....")
            service = get_service()
            file_link = upload_file(service=service,
                                    base_folder_id=config('DRIVE_BASE_FOLDER_ID'),
                                    file_path=created_output_file_path)
            
            if os.path.exists(created_output_file_path):
                os.remove(created_output_file_path)

            return file_link

        except Exception as e:
            print(f"Error converting file '{input_file}': {e}")
        finally:
            # Uninitialize COM
            pythoncom.CoUninitialize()


def data_to_excel_report_convertor(certificate_data,request_email):
    try:
        df = pd.DataFrame(certificate_data)
        df = df[['roll_no','candidate_name','course_name','course_id','certificate_id','credentials','drive_link']]
        
        filename = r"demo_outputs\\Certificates-"+str(datetime.now().strftime("%d_%m_%Y_%I-%M%p"))+".xlsx" 
        df.to_excel(filename, index=True, index_label='sr_no')

        return filename, len(df[['roll_no']])
    except Exception as e:
        print("Exception in data_to_excel_convertor:", str(e))
        return ""


    