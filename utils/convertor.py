from pptxtopdf import convert
def ppt_to_pdf_convertor(input_file,output_file):
    
    input_dir = input_file
    output_dir = output_file

    convert(input_dir, output_dir)