
from tkinter import *
from tkinter import filedialog
import customtkinter
from tkinter import messagebox
import tkinter
import requests
import time
import sys
import tkinter.scrolledtext as st
from tkinter import ttk
import vonage
import os
from tkinter import *
from tkinter import filedialog
from getmac import get_mac_address as gma
import sys

# URL of the JSON data
url = "https://api.npoint.io/161472186a46baa2483c"

# Send an HTTP GET request
response = requests.get(url)
if response.status_code == 200:
    resp = response.json()
    if resp['key'] != "khemirix2024" :
            messagebox.showerror("Error", " This script not activated .\n ask activation from telegram\n @khemirix")
            sys.exit()
else:
    messagebox.showerror("Error", " Need Connection to work . check your connection")
    sys.exit()
    
def main():
    
    API = api.get()
    SAPI = sapi.get()
    sender = SENDER.get()

    text = msg.get()
    file = browseFiles.filename
    typ = combo.get()
    print(API,'----------',SAPI)
    if typ == "Twilio":
        twillosend(API,SAPI,file,text,sender)

    elif typ == "Nexmo":
        vontagesend(API,SAPI,file,text,sender)
    else:
        print('chose 1 or 2 . depand on the Api u will use . ')



def vontagesend(api,sapi,file,text,sender):
    VONAGE_API_KEY = api
    VONAGE_API_SECRET = sapi

    # make connection to vonage ....
    client = vonage.Client(key=VONAGE_API_KEY, secret=VONAGE_API_SECRET)
    sms = vonage.Sms(client)
    line_count = linesnumber(file)
    f = open(file, "r")
    count = 0
    while f:
        x = f.readline().strip()
        count += 1
        if x == "":
            print('all done !')
            label_Resultat.insert('1.0', 'all done !')
            break
        responseData = sms.send_message({
            "from": sender,
            "to": x,
            "text": text,
        })
        print('from',sender,"to",x,'msg:',text,"api",VONAGE_API_KEY,"secret",VONAGE_API_SECRET)
        if responseData["messages"][0]["status"] == "0":
            label_Resultat.insert('1.0','[', count, '/', line_count, '] Msg to : ', x, ' - Message sent successfully. !')
        else:
            label_Resultat.insert(
                '1.0', "Message failed with error: {responseData['messages'][0]['error-text']}")


def twillosend(api,sapi,file,text,sender):
    import os
    from twilio.rest import Client
# Find your Account SID and Auth Token at twilio.com/console
    account_sid = api
    auth_token = sapi
    client = Client(account_sid, auth_token)
    line_count = linesnumber(file)
    f = open(file, "r")
    count = 0
    while f:
        x = f.readline().strip()
        count += 1
        if x == "":
            label_Resultat.insert('all done !')
            break
        message = client.messages.create(
            body=text,
            from_=sender,
            to=x
        )
        label_Resultat.insert(
            '[', count, '/', line_count, '] Msg to : ', x, ' - Message ', message.status, '. !')


def linesnumber(Nameofile):
    file = open(Nameofile, "r")
    line_count = 0
    for line in file:
        if line != "\n":
            line_count += 1
    file.close()
    return line_count


def getinput():
    print(' this demo for nexmo -- By Khemirix ')
    sender = from_
    text = msg + " By Khemirix "
    file = input(
        'to (type name of the list file . <put it in same folder of the script ) : ')
    typ = combo.values()
    if (typ == "1"):
        twillosend()
    elif (typ == "2"):
        vontagesend()
    else:
        print('chose 1 or 2 helllo. depand on the Api u will use . ')


# Modes: system (default), light, dark
customtkinter.set_appearance_mode("Dark")
# Themes: blue (default), dark-blue, green
customtkinter.set_default_color_theme("green")

app = customtkinter.CTk()  
app.geometry("1000x800")
app.title("Multi Sms Sender - By SmsPhoenix")


def browseFiles():
    browseFiles.filename = filedialog.askopenfilename(initialdir="/",
                                                      title="Select a File",
                                                      filetypes=(("Text files",
                                                                  "*.txt*"),
                                                                 ("all files",
                                                                  "*.*")))

    # Change label contents
    label_file_explorer.configure(text="File Opened: "+browseFiles.filename)


# Title
label = customtkinter.CTkLabel(master=app,
                               text="Multi SMS Sender",
                               text_color=("red"),
                               font=('Times New Roman bold', 70)
                               )
label2 = customtkinter.CTkLabel(master=app,
                                text="Telegram : @khemirix",
                                text_color=("Green"),
                                font=('Times New Roman bold', 20)
                                )

label_file_explorer = Label(app,
                            text="File Explorer",
                            width=100, height=4,
                            fg="blue", bg="black")

label.pack(padx=10, pady=10)
label2.pack(padx=10, pady=10)
label_file_explorer.pack(padx=10, pady=10)

label = customtkinter.CTkLabel(master=app,
                               text="Write Your Msg Here : ",
                               width=120,
                               height=25,
                               corner_radius=8,
                               text_color=("red"),
                               )
label.pack()
msg = customtkinter.CTkEntry(master=app,
                             width=600,
                             height=100,
                             corner_radius=10)
msg.pack()


label = customtkinter.CTkLabel(master=app,
                               text="From: ",
                               width=120,
                               height=25,
                               corner_radius=8,
                               text_color=("red"),
                               )
label.pack()
SENDER = customtkinter.CTkEntry(master=app,
                               width=600,
                               height=20,
                               corner_radius=10)
SENDER.pack()



label_Resultat = st.ScrolledText(app,
                                 width=100, height=20,
                                 fg="Green", bg="black")
label_Resultat.insert(INSERT, "Resultat Here : ")
label_Resultat.pack(padx=20, pady=20)


button = customtkinter.CTkButton(
    master=app, text="Add List", command=browseFiles)

button.pack(padx=20, pady=20)

button2 = customtkinter.CTkButton(master=app, text="Run", command=main)

button2.pack(padx=20, pady=20)

combo = customtkinter.CTkComboBox(
    app, state="readonly", values=["Nexmo", "Twilio"])
combo.place(x=20, y=20)

label = customtkinter.CTkLabel(master=app,
                               text="API: ",
                               width=120,
                               height=25,
                               corner_radius=8,
                               text_color=("red"),
                               )
label.place(x=20, y=60)
api = customtkinter.CTkEntry(master=app,
                             width=150,
                             height=20,
                             corner_radius=10)
api.place(x=20, y=90)




label = customtkinter.CTkLabel(master=app,
                               text="Secure: ",
                               width=120,
                               height=25,
                               corner_radius=8,
                               text_color=("red"),
                               )
label.place(x=20, y=120)
sapi = customtkinter.CTkEntry(master=app,
                              width=150,
                              height=20,
                              corner_radius=10)
sapi.place(x=20, y=150)
separator = ttk.Separator(app, orient='vertical')
separator.pack(fill='y')



app.mainloop()
