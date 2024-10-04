import pythoncom
import shutil
import tempfile
import os
from pptxtopdf import convert
import pandas as pd
from datetime import datetime


def ppt_to_pdf_convertor(input_file, output_path, output_filename):
    # Create a temporary directory for copying the input file
    with tempfile.TemporaryDirectory() as temp_dir:
        # Create a unique copy of the input file in the temporary directory
        temp_input_file = os.path.join(temp_dir, os.path.basename(input_file))
        shutil.copy2(input_file, temp_input_file)

        # Set the output file path in the specified directory (current working directory in this case)
        output_file = os.path.join(output_path, output_filename)

        # Initialize COM
        pythoncom.CoInitialize()
        
        try:
            # Convert using the temporary input file and save the output to the specified directory
            convert(temp_input_file, output_file)
            print(f"File successfully converted to '{output_file}'")
        except Exception as e:
            print(f"Error converting file '{input_file}': {e}")
        finally:
            # Uninitialize COM
            pythoncom.CoUninitialize()

def data_to_excel_report_convertor(certificate_data,request_email):
    df = pd.DataFrame(certificate_data)
    df = df[['roll_no','candidate_name','course_name','course_id','certificate_id','credentials']]
    
    filename = r"demo_outputs\\Certificates-"+str(datetime.now().strftime("%d_%m_%Y_%I-%M%p"))+".xlsx" 
    df.to_excel(filename, index=True, index_label='sr_no')


    