#!/usr/bin/python

import sys
import time
import os

# Packages for sending emails and attachments
import smtplib
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart

watchdir = '/home/pi/picam/'
contents = os.listdir(watchdir)
count = len(watchdir)
dirmtime = os.stat(watchdir).st_mtime

# email settings
emailFrom = 'raspiofme@gmail.com'
emailFromPwd = 'password'
emailTo = 'tome@gmail.com'
emailSubject = 'MOTION DETECTED!!!';

# Send an email with a picture attached
def sendEmail(emailTo, filenames):
    # Create the container (outer) email message
    msg = MIMEMultipart()
    msg['Subject'] = emailSubject
    msg['From'] = emailFrom
    msg['To'] = emailTo

    # Open the files in binary mode and let the MIMEImage class automatically
    # guess the specific image type
    for file_path in filenames:
        try:
            with open(file_path, 'rb') as fp:
                part = MIMEImage(fp.read(), name=os.path.basename(file_path))
		fp.close()
                msg.attach(part)
        # except IOError:
	except :
	     print "error: Can't open the file %s"%file_path	
	     pass             

    # Send the email via the Gmail SMTP server
    smtp = smtplib.SMTP('smtp.gmail.com:587')
    smtp.starttls()
    smtp.login(emailFrom, emailFromPwd)
    smtp.sendmail(emailFrom, emailTo, msg.as_string())
    smtp.quit()

while True:
    newmtime = os.stat(watchdir).st_mtime
    if newmtime != dirmtime:
        dirmtime = newmtime
        newcontents = os.listdir(watchdir)
        added = set(newcontents).difference(contents)
        if added:
            print "Files added: %s" %(" ".join(added))
	    filenames = [ watchdir + s for s in added ]
	    print filenames
	    try:	
	    	sendEmail(emailTo, filenames)
	    except :
		    print "error! but passed."	
		    pass

        contents = newcontents
    time.sleep(30)
