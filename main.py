from tkinter import *
import gtts
from io import BytesIO
import pygame
# import smtplib
# import time
import imaplib
import email
import traceback

#uses pygame to conver the text into sound
def extract_data():
    speech = text_box.get('1.0', 'end')  # saves the text from the gui
    # tts = gtts.gTTS(speech)
    # tts.save("path_goes_here")

    mp3_fp = BytesIO()
    tts = gtts.gTTS(speech)
    tts.write_to_fp(mp3_fp)  # writes the text to an audio file
    pygame.init()
    pygame.mixer.init()
    pygame.mixer.music.load(mp3_fp, 'mp3')
    pygame.mixer.music.play()  # plays the text


# text to speech emails again
def retrieve_emails():
    text_box.delete(1.0, END)
    text_box.insert(END, read_email_from_gmail())
    extract_data()


# creates the main block of the gui
root = Tk()
root.geometry("500x500")
root.configure(bg="#e835b5")

# set the window and customization
labelText = StringVar()
label = Label(root, textvariable=labelText, relief=RAISED)
text_box = Text(
    root,
    height=16,
    width=50,
    wrap='word',
    bg='lightblue',
    relief='sunken',
    highlightthickness=1,
    borderwidth=2,
    font=("Times New Roman", 18),
)
labelText.set("Put text into the box")
root.title('Email to speech program')

# text_file = open("data.txt", "r")
#
# email = text_file.read()
#
# text_file.close()
#
# text_box.insert(END, email)

# pack all elements into the window

label.pack()
Button(
    root,
    text='speech',
    command=extract_data
).pack(expand=True)
Button(
    root,
    text='retrieve emails',
    command=retrieve_emails,

).pack(expand=True)

# fetching email content

ORG_EMAIL = "@gmail.com"
FROM_EMAIL = "your_email" + ORG_EMAIL
# gmail two authentification password
FROM_PWD = "your_password"
SMTP_SERVER = "imap.gmail.com"
SMTP_PORT = 993


def read_email_from_gmail():
    try:
        # go to email inbox
        mail = imaplib.IMAP4_SSL(SMTP_SERVER)
        mail.login(FROM_EMAIL, FROM_PWD)
        mail.select('inbox')

        # seperate emails into an array and traverse
        data = mail.search(None, 'ALL')
        mail_ids = data[1]
        id_list = mail_ids[0].split()
        # first_email_id = int(id_list[0])
        latest_email_id = int(id_list[-1])
        emailReturn = ""

        # go through 10 latest emails
        for i in range(latest_email_id, latest_email_id - 10, -1):
            data = mail.fetch(str(i), '(RFC822)')
            for response_part in data:
                arr = response_part[0]
                if isinstance(arr, tuple):
                    # adds email content on string and returns that content
                    msg = email.message_from_string(str(arr[1], 'utf-8'))
                    email_subject = msg['subject']
                    email_from = msg['from']
                    print('From : ' + email_from + '\n')
                    print('Subject : ' + email_subject + '\n')
                    emailReturn += 'From : ' + email_from + '\n'
                    emailReturn += 'Subject : ' + email_subject + '\n'
        return emailReturn
    except Exception as e:
        traceback.print_exc()
        print(str(e))


latestEmails = read_email_from_gmail()

# add final data into gui
text_box.insert(END, latestEmails)
text_box.pack(expand=True)
root.after(2000, extract_data)
root.mainloop()
