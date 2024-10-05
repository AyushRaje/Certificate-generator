from pptx import Presentation
from pptx.util import Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from io import BytesIO
from utils.qr_generator import QrGenerator
from utils.convertor import ppt_to_pdf_convertor
from utils.ppt_utils import PptUtils
import tempfile
import os
from pptx import Presentation
from pptxtopdf import convert
from decouple import config
import datetime
import ast


from database.queries import create_request,save_certificate, save_failed_certificate


def run_script(data, template_data):
    
    template_data = ast.literal_eval(template_data)
    
    email = template_data.get('email')
    template_id = template_data.get('template_id')
    certificate_request = create_request(email=email)

    for index, student in data.iterrows():

        creation_status = False
        name = student['NAME']
        father_name = student['FATHER_NAME']
        gender = student['GENDER']
        course =  student['COURSE']
        course_id = student['COURSE_ID']
        center = student['CENTER']
        scheme = student['SCHEME']
        roll_no = student['ROLL_NO']

        

        unique_identifier =  student['COURSE_ID'] + roll_no

        qr_field = config('QR_BASE_URL') + unique_identifier

        current_date = str(datetime.date.today())

        try:
            # Create a temporary file to save the PowerPoint presentation
            with tempfile.NamedTemporaryFile(delete=False, suffix=".pptx") as temp_ppt:
                # Create the PowerPoint presentation object
                prs = Presentation(
                    r"C:\Projects\Automatic-Certificate-generator\certificate_templates\\"+ 
                    str(template_id)+
                    ".pptx")
                slide = prs.slides[0]

                
                # Main Text
                PptUtils(slide=slide).add_textbox_to_slide(f"""This is to certify that *{name} {gender} Mr.{father_name}* has successfully completed the course of *{course}* under *{scheme}* scheme at *{center}*
                """, 2.24, 6.69, 20.89, 3.36, 'Alice', 17.2)

                # Generate QR code and add to slide
                image = QrGenerator.generate_qr(qr_field)
                PptUtils(slide=slide).add_image_to_slide(image=image, left=10.93, top=12.26, width=3.48, height=3.48)

                # Date
                PptUtils(slide=slide).add_textbox_to_slide(f"*Date: {current_date}*", 2.02, 3.81, 20.89, 0.79, 'Alice', 17.2, alignment='')

                # Verification Link
                PptUtils(slide=slide).add_textbox_to_slide(qr_field,
                                                            7.34, 17.35, 20.89, 0.8, 'Alice', 12.6, font_color=(0, 0, 255), alignment='')

                # Save the presentation to the temporary file
                prs.save(temp_ppt.name)

                # Convert the saved PowerPoint to a PDF
                drive_link = ppt_to_pdf_convertor(temp_ppt.name, "demo_outputs/")

                creation_status = True

                
        except Exception as e:
            print(f"Error running script: {e}")
            creation_status = False
        finally:
            
            if creation_status == True:
                certificate_saved = save_certificate(candidate_name=name,
                                                     certificate_id=unique_identifier,
                                                     certificate_request_id=certificate_request,
                                                     course_name=course,
                                                     course_id=course_id,
                                                     is_created=True,
                                                     credentials = qr_field,
                                                     roll_no=roll_no,
                                                     drive_link=drive_link)
            else:
                certificate_saved = save_certificate(candidate_name=name,
                                                     certificate_id=unique_identifier,
                                                     certificate_request_id=certificate_request,
                                                     course_name=course,
                                                     course_id=course_id,
                                                     is_created=False,
                                                     credentials = None,
                                                     roll_no=roll_no,
                                                     drive_link=drive_link)
                
                failed_certificate = save_failed_certificate(certificate_request= certificate_request,
                                                        certificate=certificate_saved)
                
            # Clean up the temporary file
                
            if os.path.exists(temp_ppt.name):
                os.remove(temp_ppt.name)
    certificate_request.status = "COMPLETED"
    certificate_request.save()            

