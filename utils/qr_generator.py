import qrcode

class QrGenerator:

    def generate_qr(data):

        qr = qrcode.QRCode(
        version=1, 
        error_correction=qrcode.constants.ERROR_CORRECT_L,  
        box_size=10,  
        border=4, 
        )

        qr.add_data(data) 
        qr.make(fit=True)
        img = qr.make_image(fill="black", back_color="white")
        return img
    
if __name__ == '__main__':
    QrGenerator.generate_qr("https://www.google.com")    
