from pptx import Presentation
from pptx.util import Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from io import BytesIO
from utils.qr_generator import QrGenerator
from utils.convertor import ppt_to_pdf_convertor
from utils.ppt_utils import PptUtils
import time
import tempfile
import os
from pptx import Presentation
from pptxtopdf import convert


def run_script(data, template_data):

    for index, student in data.iterrows():


        try:
            # Create a temporary file to save the PowerPoint presentation
            with tempfile.NamedTemporaryFile(delete=False, suffix=".pptx") as temp_ppt:
                # Create the PowerPoint presentation object
                prs = Presentation(r"C:\Projects\Automatic-Certificate-generator\certificate_templates\blank_slide.pptx")
                slide = prs.slides[0]

                name = student['name']
                # Main Text
                PptUtils(slide=slide).add_textbox_to_slide(f"""This is to certify that *{name} S/O Mr. Nitin Raje* has successfully completed the course of *Motor & Circuit Development (CS183)* under *Skill Development Training Program* scheme at *Mahatma Jyotiba Phule Research And Training Institute (MAHAJYOTI), Nagpur*
                """, 2.24, 6.69, 20.89, 3.36, 'Alice', 17.2)

                # Generate QR code and add to slide
                image = QrGenerator.generate_qr("https://google.com", "test")
                PptUtils(slide=slide).add_image_to_slide(image=image, left=10.93, top=12.26, width=3.48, height=3.48)

                # Date
                PptUtils(slide=slide).add_textbox_to_slide("*Date: 19-08-2024*", 2.02, 3.81, 20.89, 0.79, 'Alice', 17.2, alignment='')

                # Verification Link
                PptUtils(slide=slide).add_textbox_to_slide("""https://vercel.grace-edunet.app/verify/""",
                                                            7.34, 17.35, 20.89, 0.8, 'Alice', 12.6, font_color=(0, 0, 255), alignment='')

                # Save the presentation to the temporary file
                prs.save(temp_ppt.name)

                # Convert the saved PowerPoint to a PDF
                ppt_to_pdf_convertor(temp_ppt.name, "demo_outputs/",name)
                
        except Exception as e:
            print(f"Error running script: {e}")
        finally:
            # Clean up the temporary file
            if os.path.exists(temp_ppt.name):
                os.remove(temp_ppt.name)

