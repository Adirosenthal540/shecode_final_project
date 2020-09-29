from tkinter import *
from PIL import ImageTk, Image

# # 1
# root = Tk()
#
# myLabel = Label(root, text = "hello world")
#
# myLabel.pack()
#
# root.mainloop()

# # 2
# root = Tk()
# myLabel = Label(root, text = "hello world")
# myLabe2 = Label(root, text = "my name is Adi")
#
# myLabel.grid(row = 0, column = 0)
# myLabe2.grid(row = 1, column = 1)
#
# root.mainloop()

# # 3
#
# root = Tk()
#
# def MyClick():
#     myLabel = Label(root, text = "I clicked")
#     myLabel.pack()
#
# myButton = Button(root, text = "Click", padx = 50, pady = 20, command = MyClick, fg = "black", bg = "green")
# myButton.pack()
#
# root.mainloop()

# # 4
#
# root = Tk()
#
# e = Entry(root, width = 50, borderwidth = 5)
# e.pack()
# #e.insert(0, "Enter your name : ")
# def MyClick():
#     myLabel = Label(root, text ="hello " + e.get())
#     myLabel.pack()
#
# myButton = Button(root, text = "enter your name", padx = 50, pady = 20, command = MyClick, fg = "black", bg = "green")
# myButton.pack()
#
# root.mainloop()

# # 5
#
# root = Tk()
# root.title("title")
# e = Entry(root, width = 35, borderwidth = 5)
# e.grid(row = 0, column = 0, columnspan=3, padx=10, pady=10)
# action = "plus"
# f_num = None
# def button_click(number):
#     #e.delete(0,END)
#     current = e.get()
#     e.insert(len(current), number)
#
# def button_clear():
#     e.delete(0, END)
#
# def button_add():
#     first_num = e.get()
#     global f_num, action
#     if f_num!= None:
#         f_num = f_num + int(first_num)
#     else:
#         f_num = int(first_num)
#     e.delete(0, END)
#     action = "plus"
#
# def button_equal():
#     second_num = e.get()
#     e.delete(0, END)
#     if action == "plus":
#         e.insert(0, f_num + int(second_num))
#
# button1 = Button(root, text = "1", padx = 40, pady = 20, command = lambda: button_click(1))
# button2 = Button(root, text = "2", padx = 40, pady = 20, command = lambda: button_click(2))
# button3 = Button(root, text = "3", padx = 40, pady = 20, command = lambda: button_click(3))
# button4 = Button(root, text = "4", padx = 40, pady = 20, command = lambda: button_click(4))
# button5 = Button(root, text = "5", padx = 40, pady = 20, command = lambda: button_click(5))
# button6 = Button(root, text = "6", padx = 40, pady = 20, command = lambda: button_click(6))
# button7 = Button(root, text = "7", padx = 40, pady = 20, command = lambda: button_click(7))
# button8 = Button(root, text = "8", padx = 40, pady = 20, command = lambda: button_click(8))
# button9 = Button(root, text = "9", padx = 40, pady = 20, command = lambda: button_click(9))
# button0 = Button(root, text = "0", padx = 40, pady = 20, command = lambda: button_click(0))
# button_add = Button(root, text = "+", padx = 40, pady = 20, command = button_add)
# button_equal = Button(root, text = "=", padx = 91, pady = 20, command = button_equal)
# button_clear = Button(root, text = "Clear", padx = 79, pady = 20, command = button_clear)
#
#
# button1.grid(row = 3, column = 0)
# button2.grid(row = 3, column = 1)
# button3.grid(row = 3, column = 2)
#
# button4.grid(row = 2, column = 0)
# button5.grid(row = 2, column = 1)
# button6.grid(row = 2, column = 2)
#
# button7.grid(row = 1, column = 0)
# button8.grid(row = 1, column = 1)
# button9.grid(row = 1, column = 2)
#
# button0.grid(row = 4, column = 0)
#
# button_add.grid(row = 5, column = 0)
# button_equal.grid(row = 5, column = 1,  columnspan=2)
# button_clear.grid(row = 4, column = 1,  columnspan=2)
#
# root.mainloop()


# 6

root = Tk()
root.title("course part 6")
root.iconbitmap(r"C:\Users\Adi Rosental\Documents\she_code\shecode_final_project\test_images\tesseracticon_dk8_icon.ico")
good_Image = []
bad_Image = []
img1 = ImageTk.PhotoImage(Image.open(r"C:\Users\Adi Rosental\Documents\she_code\shecode_final_project\DataBase\316550797_0.tif"))
img2 = ImageTk.PhotoImage(Image.open(r"C:\Users\Adi Rosental\Documents\she_code\shecode_final_project\DataBase\316550797_1.tif"))
img3 = ImageTk.PhotoImage(Image.open(r"C:\Users\Adi Rosental\Documents\she_code\shecode_final_project\DataBase\316550797_2.tif"))
img4 = ImageTk.PhotoImage(Image.open(r"C:\Users\Adi Rosental\Documents\she_code\shecode_final_project\DataBase\316550797_3.tif"))

image_list = [img1, img2, img3, img4]
status = Label(root, text = "Image 1 of " + str(len(image_list)), bd =1, relief = SUNKEN)
def eccept(image_number):
    global my_label
    global button_eccept
    global button_remove
    global status
    good_Image.append(image_list[image_number])

    status.grid_forget()
    button_eccept = Button(root, text="OK", padx=70, pady=20, state = DISABLED, fg="black",
                           bg="green")
    button_remove = Button(root, text="Error", padx=70, pady=20, state = DISABLED, fg="black",
                           bg="red")

    my_label.grid(row = 0, column = 0, columnspan = 3)
    button_eccept.grid(row = 1, column = 1)
    button_remove.grid(row = 1, column = 2)

def remove(image_number):
    global my_label
    global button_eccept
    global button_remove
    global status
    bad_Image.append(image_list[image_number])
    my_label.grid_forget()
    button_eccept = Button(root, text="OK", padx=70, pady=20, state = DISABLED, fg="black",
                           bg="green")
    button_remove = Button(root, text="Error", padx=70, pady=20, state = DISABLED, fg="black",
                           bg="red")
    my_label.grid(row = 0, column = 0, columnspan = 3)
    button_eccept.grid(row = 1, column = 1)
    button_remove.grid(row = 1, column = 2)

def foward(sign, image_number):
    global my_label
    global button_eccept
    global button_remove, status

    if sign:
        good_Image.append(image_list[image_number-1])
    else:
        bad_Image.append(image_list[image_number-1])

    my_label.grid_forget()

    my_label = Label(image=image_list[image_number])
    button_eccept = Button(root, text="OK", padx=70, pady=20, command= lambda: foward(True, image_number + 1),
                           fg="black", bg="green")
    button_remove = Button(root, text="Error", padx=70, pady=20,
                           command=lambda: foward(False, image_number +1), fg="black", bg="red")
    status = Label(root, text="Image " + str(image_number + 1) + " of " + str(len(image_list)), bd=1, relief=SUNKEN)

    if image_number == len(image_list) -1:
        button_eccept = Button(root, text="OK", padx=70, pady=20, command=lambda: eccept(image_number), fg="black", bg="green")
        button_remove = Button(root, text="Error", padx=70, pady=20, command=lambda: remove(image_number), fg="black", bg="red")

    my_label.grid(row = 0, column = 0, columnspan = 3)
    button_eccept.grid(row = 1, column = 1)
    button_remove.grid(row = 1, column = 2)
    status.grid(row=2, column=0, columnspan=3)

def exit_program():
    print(good_Image)
    print(bad_Image)
    root.quit()

my_label = Label(image = img1)
my_label.grid(row = 0, column = 0, columnspan = 3)

# button_back = Button(root, text = "<<", command = lambda: back(1))
# button_foward = Button(root, text = ">>", command = lambda: foward(1))
button_exit = Button(root, text = "Exit",padx = 30, pady = 20, command = exit_program)

button_eccept = Button(root, text="OK", padx=70, pady=20, command=lambda: foward(True, 1), fg="black", bg="green")
button_remove = Button(root, text="Error", padx=70, pady=20, command=lambda: foward(False, 1), fg="black", bg="red")
# button_back.grid(row = 0, column = 0)
# button_foward.grid(row = 0, column = 3)
button_exit.grid(row = 1, column = 0)
button_eccept.grid(row = 1, column = 1)
button_remove.grid(row = 1, column = 2)
status.grid(row=2, column = 0 , columnspan = 3, sticky = W+E)
root.mainloop()