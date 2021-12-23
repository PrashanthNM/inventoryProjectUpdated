import smtplib
from email.message import EmailMessage

def send_mail(qty,stri):
    if(stri=="received"):
        msg = EmailMessage()
        my_msg = "Dear Customer, This is a confirmation that your order of quantity " + str(qty) + " has been successfully delivered. Looking forward to collaborate with you again in future."
        msg.set_content(my_msg)
        msg['Subject'] = 'Order delivered Successfully'
    elif(stri=="ordered"):
        msg = EmailMessage()
        my_msg = "Dear Customer, This is a confirmation that your order of quantity " + str(qty) + " has been successfully placed. Looking forward to collaborate with you again in future."
        msg.set_content(my_msg)
        msg['Subject'] = 'Order placed Successfully'

    msg['From'] = "pran19cs@cmrit.ac.in"
    msg['To'] = "nm.prashanth.64@gmail.com,dishasaligrama1@gmail.com"
    # Send the message via our own SMTP server.
    server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
    server.login("pran19cs@cmrit.ac.in", "qwerty@123")
    server.send_message(msg)
    server.quit()

    

