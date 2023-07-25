import cv2
from PIL import Image
import numpy as np
import os 
from smtplib import SMTP
import pyautogui
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import winsound;
# from twilio.rest import Client
# import pywhatkit as pwk

   
recognizer = cv2.face.LBPHFaceRecognizer_create()
recognizer.read('trainer.yml')

face_cascade_Path = "haarcascade_frontalface_default.xml"


faceCascade = cv2.CascadeClassifier(face_cascade_Path)

font = cv2.FONT_HERSHEY_SIMPLEX

id = 0
# names related to ids: The names associated to the ids: 1 for Mohamed, 2 for Jack, etc...
names = ['None','Matin','Arbaj'] # add a name into this list
#Video Capture
cam = cv2.VideoCapture(0)
cam.set(3, 640)
cam.set(4, 480)

flag=0
cnt=0
# Min Height and Width for the  window size to be recognized as a face
minW = 0.1 * cam.get(3)
minH = 0.1 * cam.get(4)
while True:
    ret, img = cam.read()
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    faces = faceCascade.detectMultiScale(
        gray,
        scaleFactor=1.2,
        minNeighbors=5,
        minSize=(int(minW), int(minH)),
    )

    for (x, y, w, h) in faces:
        cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)
        id, confidence = recognizer.predict(gray[y:y + h, x:x + w])
        if (confidence < 50):
            id = names[id]
            cnt=0
            confidence = "  {0}%".format(round(100 - confidence))
        else:
            # Unknown Face
            id = "Unknown"
            
            confidence = "  {0}%".format(round(100 - confidence))
            cnt=cnt+1
            if(flag==0 and cnt==15):
                # take screenshot using pyautogui
                image = pyautogui.screenshot()
                duration=3000
                freq=840
                winsound.Beep(freq,duration)
                
                # since the pyautogui takes as a 
                # PIL(pillow) and in RGB we need to 
                # convert it to numpy array and BGR 
                # so we can write it to the disk
                image = cv2.cvtColor(np.array(image),
                                    cv2.COLOR_RGB2BGR)
                
                # writing it to the disk using opencv
                cv2.imwrite("Unknown_Member.png", image)

               #smtp server ddress of mail provider
                fromaddr = "arbaj.22120230@viit.ac.in"
                toaddr = "rohitpatil787898@gmail.com"
                
                # instance of MIMEMultipart
                msg = MIMEMultipart()
                
                # storing the senders email address  
                msg['From'] = fromaddr
                
                # storing the receivers email address 
                msg['To'] = toaddr
                
                # storing the subject 
                msg['Subject'] = "Alert..!"
                
                # string to store the body of the mail
                body = "Unknown Member Detected At Your House.."
                
                # attach the body with the msg instance
                msg.attach(MIMEText(body, 'plain'))
                
                # open the file to be sent 
                # filename = "image1.jpg"

                # dir=os.listdir(r"E:\AI Project\Unknown")

                # for path in dir:
                #     attachment = path
 
                
                # instance of MIMEBase and named as p
                # p = MIMEBase('application', 'octet-stream')
                
                # To change the payload into encoded form
                # p.set_payload((attachment).read())
                
                # encode into base64
                # encoders.encode_base64(p)
                
                # p.add_header('Content-Disposition', "attachment; filename= %s" % filename)
                
                # attach the instance 'p' to instance 'msg'
                # msg.attach(p)
                
                # creates SMTP session
                s = smtplib.SMTP('smtp.gmail.com', 587)
                
                # start TLS for security
                s.starttls()
                
                # Authentication
                s.login(fromaddr, "Arbaj@2002")
                
                # Converts the Multipart msg into a string
                text = msg.as_string()
                
                # sending the mail
                s.sendmail(fromaddr, toaddr, text)
                
                # terminating the session
                s.quit()


                #sending Whatsapp Message

                # client=Client()
                # from_wht='whatsapp:+919022279418'
                # to_No='whatsapp:+918698774774'
                # client.messages.create(body='Alert.... ! <br> Someone is arrived at your place', 
                #                         media_url='https://demo.twilio.com/Unknown_Member.png',
                #                         from_=from_wht,
                #                         to=to_No)

                # print("Alert is sent on whatsapp") 

                # account_sid = 'ACa74e07d3b8e295878d9a0a2df7397bdf' 
                # auth_token = '[Redacted]' 
                # client = Client(account_sid, auth_token) 
                
                # message = client.messages.create( 
                #                             from_='whatsapp:+14155238886',  
                #                             body='Hello! This is an editable text message. You are free to change it and write whatever you like.',      
                #                             to='whatsapp:+917666878546' 
                #                         ) 
                
                # print(message.sid)

                # pwk.sendwhatmsg("+917666878546", "Hi, how are you?", 22, 52)
                # 97LOrBtt2d2rM8SzIaGEAz8LTM_DeJYjy2hjRUIr
                # using Exception Handling to avoid unexpected errors
                # try:
                #     # sending message in Whatsapp in India so using Indian dial code (+91)
                #     pwk.sendwhatmsg("+91XXXXXX5980", "Hi, how are you?", 20, 34)
                
                #     print("Message Sent!") #Prints success message in console
                
                #     # error message
                # except: 
                #     print("Error in sending the message")
                flag=1

        cv2.putText(img, str(id), (x + 5, y - 5), font, 1, (255, 255, 255), 2)
        cv2.putText(img, str(confidence), (x + 5, y + h - 5), font, 1, (255, 255, 0), 1)

    cv2.imshow('camera', img)
    # Escape to exit the webcam / program
    k = cv2.waitKey(10) & 0xff
    if k == 27:
        break
print("\n [INFO] Exiting Program.")
cam.release()
cv2.destroyAllWindows()