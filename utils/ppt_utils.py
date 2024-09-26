from pptx import Presentation
from pptx.util import Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN

class PptUtils:

    def __init__(self,slide):
        self.slide = slide


    def cm_to_inches(self, cm_value):
        return cm_value / 2.54

    def cm_to_emu(self, cm_value):
        inches_value = self.cm_to_inches(cm_value)
        return int(inches_value * 914400)
    
    def add_textbox_to_slide(self, text, left, top, width, height, font_family,font_size, font_color=(0, 0, 0)):
        
        textbox = self.slide.shapes.add_textbox(left=self.cm_to_emu(left), 
                                                top=self.cm_to_emu(top), 
                                                width=self.cm_to_emu(width), 
                                                height=self.cm_to_emu(height))
        
        frame = textbox.text_frame
        frame.fit_text(font_family=font_family, max_size=self.cm_to_emu(4))
        frame.word_wrap=True
        p = frame.add_paragraph()
        p.alignment = PP_ALIGN.CENTER
        run = p.add_run()
        run.text = text
        font = run.font
        font.name = font_family
        font.size = Pt(font_size)
        font.color.rgb = RGBColor(*font_color)

if __name__== '__main__':

    input_slide = ""
    prs =Presentation(r"C:\Projects\Automatic-Certificate-generator\blank_slide.pptx")
    slide = prs.slides[0]
    PptUtils(slide=slide).add_textbox_to_slide("""This is to certify that Mr. Ayush Raje S/O Mr. Nitin Raje has successfully completed the course of Motor & Circuit Development (CS183) under Skill Development Training Program scheme at Mahatma Jyotiba Phule Research And Training Institute,(MAHAJYOTI), Nagpur
""",2.24,6.69,20.89,3.36,'Alice',17.2)
    prs.save("output.pptx")

