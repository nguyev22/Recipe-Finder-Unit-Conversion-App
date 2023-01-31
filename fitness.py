# from tkinter import Button
# from tkinter import messagebox
import tkinter as tk
import tkinter.font as font
from tkinter import *


window = tk.Tk()
window.title("Fitness Conversion")
window.geometry('300x400')


def prompt(option):
    textbox.destroy()

def popUp(): #https://www.youtube.com/watch?v=tpwu5Zb64lQ
    global textbox
    textbox = Toplevel(window)
    textbox.title('Prompt to Edit')
    textbox.geometry('400x200')
    textbox.config(bg='pink')

    global image
    image = PhotoImage(file='C:/Users/viwhe/Desktop/CS361Project/warning.png')
    label = Label(textbox, text='Would You Like to Proceed?', font=('helvetica', 20))
    label.pack(pady=10)

    new_frame = Frame(textbox)
    new_frame.pack(pady=5)

    picture = Label(new_frame, image=image, borderwidth=0)
    picture.grid(row=0, column=0, padx=10)

    yes = Button(new_frame, text='YES', command=lambda: prompt("yes"))
    yes.grid(row=0, column=1)

    no = Button(new_frame, text='NO', command=lambda: prompt("no"))
    no.grid(row=0, column=5)

def showUnits():
    label.config(text=clicked.get())

def grams_to_lbs():
    user_input = ent_change.get()
    pounds_ans = int(user_input) * (float(0.00220462))
    cvrt_ans["text"] = f"{round(pounds_ans, 5)}" + " lbs"

def g_fat_to_cals():
    user_input = ent_change2.get()
    cals_ans = int(user_input) * 9
    cvrt_ans2["text"] = f"{(cals_ans)}" + " cals"

def g_carb_to_cals():
    user_input = ent_change3.get()
    cals_ans = int(user_input) * 4
    cvrt_ans3["text"] = f"{(cals_ans)}" + " cals"

def g_protein_to_cals():
    user_input = ent_change4.get()
    cals_ans = int(user_input) * 4
    cvrt_ans4["text"] = f"{(cals_ans)}" + " cals"

def homeWindow():
    new_wind = tk.Tk()
    new_wind.title('Home')
    new_wind.geometry('300x400')

def searchWindow():
    new_wind = tk.Tk()
    new_wind.title('Search')
    new_wind.geometry('300x400')

def historyWindow():
    new_wind = tk.Tk()
    new_wind.title('History Log')
    new_wind.geometry('300x400')

def moreWindow():
    new_wind = tk.Tk()
    new_wind.title('More')
    new_wind.geometry('300x400')

def recipeWindow():
    new_wind = tk.Tk()
    new_wind.title('More')
    new_wind.geometry('300x400')


#################################
textResize = font.Font(family='Helvetica', size=36, weight='bold')
frame1 = tk.Frame(window)
label_frame1 = tk.Label(master=frame1, text='Home', font=textResize, bg='pink', fg='white')
label_frame1.pack()

frame1.pack()

conversion1_entry = tk.Frame(frame1)
ent_change = tk.Entry(frame1, width=10)
lbl_unit = tk.Label(frame1, text="grams")

ent_change.pack(side=tk.LEFT)
conversion1_entry.pack(side=tk.LEFT)
lbl_unit.pack(side=tk.LEFT)

button_cvrt = tk.Button(frame1, text="\N{RIGHTWARDS BLACK ARROW}", command=grams_to_lbs)
cvrt_ans = tk.Label(frame1, text="lbs")

button_cvrt.pack(side=tk.LEFT)
cvrt_ans.pack(side=tk.LEFT)
#################################

frame2 = tk.Frame(window)
frame2.pack()

conversion2_entry = tk.Frame(frame2)
ent_change2 = tk.Entry(frame2, width=10)
lbl_unit2 = tk.Label(frame2, text="grams of fat")

ent_change2.pack(side=tk.LEFT)
conversion2_entry.pack(side=tk.LEFT)
lbl_unit2.pack(side=tk.LEFT)

button_cvrt2 = tk.Button(frame2, text="\N{RIGHTWARDS BLACK ARROW}", command=g_fat_to_cals)
cvrt_ans2 = tk.Label(frame2, text="cals")

button_cvrt2.pack(side=tk.LEFT)
cvrt_ans2.pack(side=tk.LEFT)
#################################

frame2 = tk.Frame(window)
frame2.pack()

conversion3_entry = tk.Frame(frame2)
ent_change3 = tk.Entry(frame2, width=10)
lbl_unit3 = tk.Label(frame2, text="grams of carbs")

ent_change3.pack(side=tk.LEFT)
conversion3_entry.pack(side=tk.LEFT)
lbl_unit3.pack(side=tk.LEFT)

button_cvrt3 = tk.Button(frame2, text="\N{RIGHTWARDS BLACK ARROW}", command=g_carb_to_cals)
cvrt_ans3 = tk.Label(frame2, text="cals")

button_cvrt3.pack(side=tk.LEFT)
cvrt_ans3.pack(side=tk.LEFT)

#################################

frame2 = tk.Frame(window)
frame2.pack()

conversion4_entry = tk.Frame(frame2)
ent_change4 = tk.Entry(frame2, width=10)
lbl_unit4 = tk.Label(frame2, text="grams of protein")

ent_change4.pack(side=tk.LEFT)
conversion4_entry.pack(side=tk.LEFT)
lbl_unit4.pack(side=tk.LEFT)

button_cvrt4 = tk.Button(frame2, text="\N{RIGHTWARDS BLACK ARROW}", command=g_protein_to_cals)
cvrt_ans4 = tk.Label(frame2, text="cals")

button_cvrt4.pack(side=tk.LEFT)
cvrt_ans4.pack(side=tk.LEFT)

#################################

textResize = font.Font(family='Helvetica', size=12, weight='bold')
buttonHome = Button(window, text='Home', font=textResize, fg='red', command=homeWindow)
buttonHome.place(x=5, y=300)

buttonSearch = Button(window, text='Search', font=textResize, fg='red', command=searchWindow)
buttonSearch.place(x=68, y=300)

buttonLog = Button(window, text='History Log', font=textResize, fg='red', command=historyWindow)
buttonLog.place(x=140, y=300)

buttonMore = Button(window, text='More', font=textResize, fg='red', command=moreWindow)
buttonMore.place(x=245, y=300)

rightArrow = Button(window, font=textResize, text="\N{RIGHTWARDS BLACK ARROW}")
leftArrow = Button(window, font=textResize, text="\N{LEFTWARDS BLACK ARROW}")
leftArrow.place(x=15, y=350)
rightArrow.place(x=255, y=350)
################################# https://www.geeksforgeeks.org/dropdown-menus-tkinter/

frame2 = tk.Frame(window)
frame2.pack()

menu_btn = ['grams', 'g fat to cals', 'g carbs to cals', 'g prot to cals']
clicked = StringVar()

clicked.set("Select Measurement")

menu = OptionMenu(frame2, clicked, *menu_btn)
menu.pack()
#################################

affirm_button = Button(frame2, text='Edit Button', command=popUp)
affirm_button.pack()

window.mainloop()



