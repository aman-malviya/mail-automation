import smtplib
from email.message import EmailMessage
import xlrd
from dotenv import dotenv_values
from mako.template import Template

config = dotenv_values(".env")
EMAIL_ADDRESS = config['EMAIL']
EMAIL_PASSWORD = config['PASSWORD']

wb = xlrd.open_workbook("./sheet.xlsx")
sheet = wb.sheet_by_index(0)

#If you have images in your template, host your images somewhere (e.g. freeimage.host) and update the src of images in the template prior to automating mailing
body = Template(filename='./Template/template.html')

with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
    smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
    for i in range(sheet.nrows):
        msg = EmailMessage()
        reciever = sheet.cell_value(i, 0)
        msg['Subject'] = "Welcome!"
        msg['From'] = EMAIL_ADDRESS
        msg['To'] = reciever
        msg.set_content('This is an email')
        msg.add_alternative(body.render(
            name=sheet.cell_value(i, 1)), subtype='html')
        smtp.send_message(msg)
        print("Mail sent to " + reciever)
