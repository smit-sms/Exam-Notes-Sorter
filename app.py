import tkinter as tk
from tkinter import messagebox, filedialog
from tkinter import *
from PIL import ImageTk, Image
import cv2, os, imutils
import numpy as np 
from keras.preprocessing.image import img_to_array
from keras.models import load_model

root = tk.Tk()
root.title("Exam Notes Sorter")
model = load_model('model.h5')

class Folder:
    def __init__(self, folder, output_folder):
        self.folder = folder        
        self.output_folder = output_folder
        
    def sort(self):
        folder = self.folder
        output_folder = self.output_folder
        if not os.path.exists(folder):
            messagebox.showerror("Error", "No Folder Selected/Folder Not Found")
        else:
            if not os.path.exists(output_folder):
                messagebox.showerror("Error", "No Output Folder Selected/Some Error Occured")
            else:
                image = []

                for img in os.listdir(folder):
                    temp_name = img
                    image = cv2.imread(os.path.join(folder, img))
                    orig = image.copy()
                    
                    # Preprocessing the image & Prediction
                    image = cv2.resize(image, (28, 28))
                    image = image.astype('float')/255.0	
                    image = img_to_array(image)
                    image = np.expand_dims(image, axis=0)
                    (not_notes, notes) = model.predict(image)[0]
                    label = 'notes' if notes > not_notes else "not_notes"
                    proba = notes if notes > not_notes else not_notes
                    final_label = "{}: {:.2f}%".format(label,proba*100)
                    output = imutils.resize(orig,width=400)
                    cv2.putText(output, final_label,(10,25), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0,255,0), 2)
                    
                    # Sorting in Respective folders
                    if(label == "not_notes"):
                        if not os.path.exists(output_folder+'/Not_Notes'):
                            os.makedirs(output_folder+'/Not_Notes')

                        path = output_folder+'/Not_Notes/'+temp_name
                    else:
                        if not os.path.exists(output_folder+'/Notes'):
                                os.makedirs(output_folder+'/Notes')

                        path = output_folder+'/Notes/'+temp_name
                
                    cv2.imwrite(path, output)
                messagebox.showinfo("Success", "Successfully Sorted the Notes!", parent=root)


class View:
    def __init__(self):
        self.label = tk.Label(root,text="")
        
    def view_notes(self):
        self.label.grid(row=8, column=2, padx=10, pady=10)
        self.label.config(image='')
        def next_img():
            try:
                img = next(images)  # get the next image from the iterator
            except StopIteration:
                messagebox.showinfo("Prompt", "No more Images!")
                return  # if there are no more images, do nothing

            # load the image and display it
            img = Image.open(img)
            width, height = img.size
            img = ImageTk.PhotoImage(img.resize((int(width/2), int(height/2))))
            self.label.img = img  # keep a reference so it's not garbage collected
            self.label['image'] = img    
        
        images = []
        folder = f.output_folder+"/Notes/"
        if not os.path.exists(folder):
            messagebox.showerror("Error", "Output Folder Not Found")
        else:
            for img in os.listdir(folder):
                images.append(folder+img)
            images = iter(images)  # make an iterator
            
            next_img()
            button6=tk.Button(root, text="Next", command = next_img)
            button6.grid(row=9,column=2)
            l = tk.Label(text="")
            l.grid(row=10, column=0)


    def view_not_notes(self):
        self.label.config(image='')
        self.label.grid(row=8, column=2, padx=10, pady=10)
        def next_img():
            try:
                img = next(images)  # get the next image from the iterator
            except StopIteration:
                messagebox.showinfo("Prompt", "No more Images!")
                return  # if there are no more images, do nothing

            # load the image and display it
            img = Image.open(img)
            width, height = img.size
            img = ImageTk.PhotoImage(img.resize((int(width/2), int(height/2))))
            self.label.img = img  # keep a reference so it's not garbage collected
            self.label['image'] = img    
        
        images = []
        folder = f.output_folder+"/Not_Notes/"
        if not os.path.exists(folder):
            messagebox.showerror("Error", "Output Folder Not Found")
        else:
            for img in os.listdir(folder):
                images.append(folder+img)
            images = iter(images)  # make an iterator
            
            next_img()
            button6=tk.Button(root, text="Next", command = next_img)
            button6.grid(row=9,column=2)
            l = tk.Label(text="")
            l.grid(row=10, column=0)

def input_folder():
    folder = filedialog.askdirectory()
    f.folder = folder
    mystr.set(folder)
    e1 = tk.Entry(width=len(mystr.get()),textvariable=mystr, state=DISABLED).grid(row=1, column=2, padx=10, pady=10)

def output_folder():
    folder = filedialog.askdirectory()
    f.output_folder = folder
    mystr2.set(folder)
    e2 = tk.Entry(width=len(mystr2.get()),textvariable=mystr2, state=DISABLED).grid(row=2, column=2, padx=10, pady=10)

f = Folder("none", "none")
v = View()

# For Responsive
for i in range(0,11):
    root.grid_rowconfigure(i, weight=1)     # row
for j in range(0,4):
    root.grid_columnconfigure(j, weight=1)  # column

w = 650 # width for the Tk root
h = 700 # height for the Tk root

# get screen width and height
ws = root.winfo_screenwidth() # width of the screen
hs = root.winfo_screenheight() # height of the screen

# calculate x and y coordinates for the Tk root window
x = (ws/2) - (w/2)
y = (hs/2) - (h/2)

# set the dimensions of the screen 
# and where it is placed
root.geometry('%dx%d+%d+%d' % (w, h, x, y))

l = tk.Label(text="").grid(row=0, column=0)

##################
l1 = tk.Label(text="  Input Folder Path:")
l1.grid(row=1, column=0)

mystr = StringVar()
mystr.set('')
    
e1 = tk.Entry(width=40,textvariable=mystr, state=DISABLED).grid(row=1, column=2, padx=10, pady=10)

button1=tk.Button(root, text="Browse", command = input_folder).grid(row=1,column=3)
##################


##################
l1 = tk.Label(text="  Output Folder Path:").grid(row=2, column=0)

mystr2 = StringVar()
mystr2.set('')
    
e2 = tk.Entry(width=40,textvariable=mystr2, state=DISABLED).grid(row=2, column=2, padx=10, pady=10)

button1=tk.Button(root, text="Browse", command = output_folder).grid(row=2,column=3)

l = tk.Label(text="").grid(row=3, column=0)
##################


##################
button2=tk.Button(root, text="Sort", command = f.sort).grid(row=4,column=0)

button3=tk.Button(root, text="Cancel", command=root.destroy).grid(row=4,column=2)

l = tk.Label(text="")
l.grid(row=5, column=0)
l = tk.Label(text="")
l.grid(row=6, column=0)
##################


##################
l2 = tk.Label(text="   View sorted here:")
l2.grid(row=7, column=0)

button4=tk.Button(root, text="Notes", command = v.view_notes)
button4.grid(row=7,column=2)

button5=tk.Button(root, text="Not Notes", command = v.view_not_notes)
button5.grid(row=7,column=3, padx=20)

root.mainloop()