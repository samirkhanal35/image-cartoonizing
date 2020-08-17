import tkinter as tk
from tkinter import filedialog
import cv2
from PIL import Image, ImageTk

#from tkinter import *
window = tk.Tk()

window.title("Cartoonizing")
window.geometry('1200x800')

#header
header = tk.Label(window, text="GET YOUR IMAGE CARTOONIZED HERE!", bg="red", fg="black" ,font=("none bold",35), anchor="n") 
#anchor=n for top-central justification
header.place(x=300,y=1)
#header.pack()

#left frame
left_frame = tk.Frame(window, width=400, height=400, highlightbackground="black", highlightthickness=1)
left_frame.place(x=40,y=150)
left_frame.pack_propagate(0)

#left image label
# inp_image = tk.Label(left_frame, text="Input Image", font=("none Bold",10))
# inp_image.pack()


#left label
left_label = tk.Label(window, text="Input Image", font=("none Bold",20))
left_label.place(x=200,y=120)


#rigt_frame
rigt_frame = tk.Frame(window, width=400, height=400, highlightbackground="black", highlightthickness=1)
rigt_frame.place(x=760,y=150)
rigt_frame.pack_propagate(0)

#right image label
# out_image = tk.Label(rigt_frame, text="Output Image", font=("none Bold",10))
# out_image.pack()



#right label
right_label = tk.Label(window, text="Output Image", font=("none Bold",20))
right_label.place(x=930,y=120)



class variables:
    img = ""
    inp_img = ""
    out_img = ""

    #left image label
    inp_image = tk.Label(left_frame, text="Input Image", font=("none Bold",10))
    inp_image.pack()

    #right image label
    out_image = tk.Label(rigt_frame, text="Output Image", font=("none Bold",10))
    out_image.pack()

def working_design():
    #image selection button
    img_selection_btn = tk.Button(window, text="Select Image", fg="black", font=("none Bold",20) , command=open_file)
    img_selection_btn.place(x=520, y=100)
    #*--------------------------------
    # #sketching button
    img_sketching_btn = tk.Button(window, text="Cartoonize", fg="black", font=("none Bold",20) , command=Cartoonizing)
    img_sketching_btn.place(x=520, y=150)


def open_file(): 
    filename = filedialog.askopenfilename(filetypes=(("JPEG","*.jpg"),("PNG","*.png"),("All Files","*.*"))) 

    if filename!="" :
        variables.img = cv2.imread(filename).astype('uint8')
        #resizing for image display
        variables.inp_img = resize_img(variables.img)
        #Rearranging the color channel
        b,g,r = cv2.split(variables.inp_img)
        img = cv2.merge((r,g,b))

        #convert image object into TkPhoto object
        im = Image.fromarray(img)
        img1 = ImageTk.PhotoImage(image=im)

        variables.inp_image.pack_forget()
        left_frame.update()

        variables.inp_image = tk.Label(left_frame, image=img1)
        variables.inp_image.image = img1
        variables.inp_image.pack()
        left_frame.update()

        
        
 

def resize_img(img):
    
    img1 = cv2.resize(img,(400,400)) #(a high-quality downsampling filter)       
    return img1

def Cartoonizing():
    img_rgb = variables.img
    img_oil = cv2.xphoto.oilPainting(img_rgb, 7, 1)
    img_pencil, img1 = cv2.pencilSketch(img_rgb, sigma_s=60, sigma_r=0.07, shade_factor=0.05) 
    
    img_pencil = cv2.adaptiveThreshold(img_pencil,255,cv2.ADAPTIVE_THRESH_MEAN_C,cv2.THRESH_BINARY,11,2)
    img_pencil = cv2.cvtColor(img_pencil, cv2.COLOR_GRAY2BGR )
    
    img = cv2.bitwise_and(img_pencil, img_oil)

    #resizing for image display
    variables.out_img = resize_img(img)
    #Rearranging the color channel
    b,g,r = cv2.split(variables.out_img)
    img = cv2.merge((r,g,b))
    #convert image object into TkPhoto object
    im = Image.fromarray(img)
    img1 = ImageTk.PhotoImage(image=im)
    
    variables.out_image.pack_forget()
    rigt_frame.update()

    variables.out_image = tk.Label(rigt_frame, image=img1)
    variables.out_image.image = img1
    variables.out_image.pack()
    rigt_frame.update()


working_design()

window.mainloop()
