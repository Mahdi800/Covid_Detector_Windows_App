from PIL import ImageTk, Image
import PIL.Image
from tkinter import filedialog, messagebox
import numpy as np
import tensorflow
from tensorflow.keras.preprocessing.image import img_to_array
import cv2
import tensorflow as tf
from keras.models import load_model
from keras.preprocessing import image
import os
from numpy import *
from tkinter import *
from customtkinter import *
from tkinter import ttk
from ttkthemes import ThemedTk
from customtkinter import *

def wrt(st,fname):
    file = open(fname,"w+")
    file.write(st)
    file.close() 

def red(fname):    
    file = open(fname,"r")
    f=file.read()
    file.close() 
    return f

model = load_model('new_model.h5') 

def forward(num):  
	callback(num)
	nameF.set(root.filename[num])
	if len(ImageList)<num+1:
		load(num)
	printImg(num)
	button_forward.config(command=lambda:forward(num+1))
	button_back.config(command=lambda:back(num-1), state=NORMAL)
	if num == (len(root.filename)-1):
		button_forward.config(state=DISABLED)


def back(num):     
	callback(num)
	nameF.set(root.filename[num])
	printImg(num)
	button_forward.config(command=lambda:forward(num+1), state=NORMAL)
	button_back.config(command=lambda:back(num-1))
	if num == 0:
		button_back.config(state=DISABLED)


def openfiles():
	global nameOf
	if root.filename:
		backup = root.filename
	del root.filename
	root.filename = filedialog.askopenfilenames(initialdir="/home/ruka/Anime&Manga", title="Select file", filetypes=(("all file",".*"), ("webp file",".webp"),("jpg file",".jpg"),("png file",".png")))
	nameF.set(root.filename[0])
	if not root.filename:
		exitComfirm = messagebox.askyesno("Exit the Programme?","You didn't choose any file. Exit the programme?")
		if exitComfirm == 1:
			quit()
		else:
			root.filename = backup
	else:
		global ImageList
		ImageList=[]
		load(0)
		printImg(0)
		inibutton()
	callback(0)

        
def callback(num):  
  #cell="\n IMAGE FILE NOT UPLOADED..."  
    index=1
    cell=''
    try:
            test_image=image.load_img(root.filename[num],target_size=(64,64))
            test_image=image.img_to_array(test_image)
            test_image=expand_dims(test_image,axis=0)
            test_image /= 255
            result = model.predict(test_image)
            result= result[0][0]
            result= (result)*100
            result=int(result)
            if result>50:
                if result==100:
                    result=99
                result=str(result)
                string=str(' احتمال '+result+' درصدی مبتلا نبودن ')
            else:
                result=100-result
                if result==100:
                    result=99
                result=str(result)
                string=str(' احتمال '+result+' درصدی مبتلا بودن به کووید-۱۹ ')
            output.set(string);print(index, cell)
            index+=1
    except:
        output.set(cell);print("Exception")


#set_appearance_mode('Light')  # Other: "Light", "Dark"
root =Toplevel()
root.title(" نرم افزار تشخیص کویید-۱۹") 

output=StringVar();
nameF=StringVar();

n_rows=7
n_columns=5

#root.attributes('-fullscreen',True)
canvas= Canvas(root, width=3000, height=1500, bg='ghost white')
canvas.grid(columnspan=n_columns,rowspan=n_rows)


bkImg = PIL.Image.open("network2.png")
resized_img2 = bkImg.resize((2000, 1000), PIL.Image.ANTIALIAS)
img3=ImageTk.PhotoImage(resized_img2)   
canvasLabel= Label(canvas, image = img3) 
canvasLabel.place(relwidth=1, relheight=1, relx=0, rely=0)


#frame2 = CTkFrame(canvas, corner_radius=20, fg_color='dodger blue')
#frame2.place(x=145, y=550, relwidth=0.8, relheight=0.25)

#Canvas for model prediction (output)
#canvas2 = Frame(root, bg='white')
#canvas2.place(x=410, y=650, relwidth=0.4, relheight=0.05)


#root['bg'] = 'black'
root.resizable(width = True, height = True) 

root.filename=Label(root)


defaultImg = PIL.Image.open("lungs.png")
resized_img3 = defaultImg.resize((300, 300), PIL.Image.ANTIALIAS)
img4=ImageTk.PhotoImage(resized_img3)  

frameC= Frame(root, bg='dodger blue')
frameC.grid(row=5, column=1, pady=(0,210), padx=(300,0))


myLabel=Label(frameC, image=img4)
#myLabel.grid(row=1, column=1, columnspan=3)
myLabel.grid(row=5, column=1)

frameB= Frame(root, bg='dodger blue')
frameB.grid(row=4, column=1, padx=(280,0))

img_label= Label(frameB, bg='dodger blue', text='تصویر', font=("Roboto", 20), width=70)
img_label.grid(row=4, column=1)

# Label Frame
#labelframe = LabelFrame(root, height=350, width=1000, text="This is a LabelFrame")
#labelframe.grid(row=1, columnspan=n_columns)

def resize(img):
	img = img.resize((300,300), PIL.Image.ANTIALIAS)
	ImageList.append(ImageTk.PhotoImage(img))

def load(num):
	img = PIL.Image.open(root.filename[num])
	resize(img)

def printImg(num):
	global myLabel
	myLabel.config(image=ImageList[num])
	status = ttk.Label(root,text=" تصویر "+str(num+1)+" از "+str(len(root.filename))+'   ', relief=SUNKEN, anchor=E)
	#status.grid(row=4,column=1,columnspan=1, sticky=W+E)
	status.grid(row=5, column=1, pady=(200,0), padx=(300,0))


    
    
#title2 = Label(root, bg='ghost white', text=" تشخیص کویید-۱۹ از روی سی تی اسکن ", font=('Roboto',25)).grid(row=0, columnspan=n_columns)


    
#canvas= Canvas(root, width=3000, height=1500)
#canvas.grid(columnspan=n_columns,rowspan=n_rows)


for i in range(n_rows):
    root.grid_rowconfigure(i,  weight =1)
for i in range(n_columns):
    root.grid_columnconfigure(i,  weight =1)

b1= Button(root, text = "باز کردن تصویر", command = openfiles, width=15, height=2)
b1.grid(row=5,column=3, padx=(0,200), pady=(0,200))

#l1= ttk.Label(root, text='< وضعیت بیمار >', font=("Roboto", 15))
#l1.grid(row=4, column=1, pady=(0,50))

#l2= ttk.Label(root, text='< جزئیات تصویر >', font=("Roboto", 15))
#l2.grid(row=2, column=1, pady=(0,100))

l3= Label(root, textvariable=output, font=("Roboto", 20))
l3.place(x=410, y=650, relwidth=0.4, relheight=0.05)

#b2= CTkButton(root, text='تشخیص', command = callback, corner_radius=15, fg_color='white', hover_color='light gray')
#b2.grid(row=4, column=3, padx=(200,0), pady=(0,0))

frameA= Frame(root, bg='dodger blue')
frameA.grid(row=2, column=1, padx=(280,0))

nameOf= Label(root, textvariable=nameF, font=("Roboto", 15), width=93, height=2).grid(row=3, column=1, pady=(10,0), padx=(280,0))

name_label= Label(frameA, bg='dodger blue', text='نام فایل', font=("Roboto", 20), width=70).grid(row=2, column=1)

def inibutton():
	global button_forward
	global button_back
    
	button_back = Button(root, text="<<", state=DISABLED, width=10, height=2)
	button_back.grid(row=5, column=1, padx=(0,0), pady=(200,0))
    
	#button_exit = Button(root, text="OPEN", command=openfiles)
	button_forward = Button(root, text=">>", command=lambda:forward(1), width=10, height=2)
	button_forward.grid(row=5, column=1, padx=(600,0), pady=(200,0))
    
	if len(root.filename)==1:
		button_forward.config(state=DISABLED)

	#button_exit.grid(row=2, column=1)
    
root.mainloop() 
