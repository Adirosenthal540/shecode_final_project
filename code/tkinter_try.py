from tkinter import *
import cv2 as cv
from PIL import Image, ImageTk
import numpy as np
import ImageProcessing

IMAGE_WIDTH_TO_SHOW = 450
IMAGE_HEIGTH_TO_SHOW = 600

image_numpy_array = []
original_numpy_array = []
points = []


def click_CutImage(num_image) :
    global points, file, img_toCut, top2, w, path_list, image_numpy_array, num_image_to_cut, cv_array, original_numpy_array
    print (num_image)
    top2 = Toplevel()
    top2.title("secend window")
    points = []
    w = Canvas(top2, width=500, height=500)
    cv_array = original_numpy_array[num_image].copy()

    img_toCut = ImageTk.PhotoImage(Image.fromarray(cv_array))
    image_numpy_array[num_image] = cv_array.copy()
    num_image_to_cut = num_image
    w.create_image(0, 0, image=img_toCut, anchor="nw")
    w.grid(row=0)
    top2.bind("<Button 1>", CutImage)
    #print("end cut")

def CutImage(eventorigin):
    global x, y, points, img_toCut, top2, w, path_list, image_numpy_array, num_image_to_cut, cv_array, root_window

    while(len(points)<4):
        x = eventorigin.x
        y = eventorigin.y
        print(x, y)

        cv_array = cv.circle(cv_array, (x, y), 3, 0, -1)
        points.append((x, y))
        if len(points) >= 2:
            cv_array = cv.line(cv_array, points[-1], points[-2], 50, 3)

        img_toCut = ImageTk.PhotoImage(Image.fromarray(cv_array))
        w.create_image(0, 0, image=img_toCut, anchor="nw")

        top2.bind("<Button 1>", CutImage)
        top2.mainloop()
    print (points)
    top2.destroy()

    image_numpy_array[num_image_to_cut] = ImageProcessing.WrapImage(image_numpy_array[num_image_to_cut], np.array(points[0:4]))
    image_list[num_image_to_cut] = ImageTk.PhotoImage(Image.fromarray(image_numpy_array[num_image_to_cut]))

    status = Label(root_window, text = "Image "+str(num_image_to_cut+1)+" of " + str(len(image_list)), bd =1, relief = SUNKEN)
    my_image = Label(root_window, image = image_list[num_image_to_cut])
    my_image.grid(row = 0, column = 1, columnspan = 3)
    button_exit = Button(root_window, text = "Exit",padx = 70, pady = 20, command = exit_program)
    button_wrap = Button(root_window, text = "try again Cut Image",padx = 70, pady = 20, command = lambda: click_CutImage(num_image_to_cut))
    if num_image_to_cut == len(path_list)-1:
        button_next = Button(root_window, text=">>", padx=70, pady=20, state=DISABLED, fg="black")
    else:
        button_next = Button(root_window, text=">>", padx=70, pady=20, command=lambda: next(num_image_to_cut + 1),
                             fg="black")

    if num_image_to_cut ==0:
        button_previous = Button(root_window, text="<<", padx=70, pady=20, state = DISABLED, fg="black")
    else:
        button_previous = Button(root_window, text="<<", padx=70, pady=20, command=lambda: back(num_image_to_cut - 1),
                                 fg="black")

    button_exit.grid(row = 1, column = 0)
    button_wrap.grid(row = 1, column = 1,  columnspan = 2, sticky = W+E)
    button_next.grid(row = 0, column =4)
    button_previous.grid(row = 0, column = 0)
    status.grid(row=2, column = 0 , columnspan = 3, sticky = W+E)
    root_window.mainloop()

def next( image_number):
    global my_image, button_next, button_previous, status, good_Image, bad_Image, image_list, image_path_list, root_window

    my_image.grid_forget()

    my_image = Label(root_window, image=image_list[image_number])

    if image_number == len(image_list) - 1:
        button_next = Button(root_window, text=">>", padx=70, pady=20, state=DISABLED, fg="black")
    else:
        button_next = Button(root_window, text=">>", padx=70, pady=20, command=lambda: next(image_number + 1),fg="black")

    button_previous = Button(root_window, text="<<", padx=70, pady=20,command=lambda: back(image_number -1), fg="black")

    status = Label(root_window, text="Image " + str(image_number+1) + " of " + str(len(image_list)), bd=1, relief=SUNKEN)
    button_wrap = Button(root_window, text="Cut Image", padx=70, pady=20, command=lambda: click_CutImage(image_number))

    button_wrap.grid(row=1, column=1, columnspan=2, sticky=W + E)
    my_image.grid(row=0, column=1, columnspan=3)
    button_next.grid(row = 0, column =4)
    button_previous.grid(row=0, column=0)
    status.grid(row=2, column=0, columnspan=3, sticky = W+E)


def back( image_number):
    global my_image, button_next, button_previous, status, good_Image, bad_Image, image_list, image_path_list, root_window
    print(image_number)
    my_image.grid_forget()

    my_image = Label(root_window, image=image_list[image_number])
    button_next = Button(root_window, text=">>", padx=70, pady=20, command=lambda: next(image_number + 1), fg="black")

    if image_number == 0:
        button_previous = Button(root_window, text="<<", padx=70, pady=20,state = DISABLED, fg="black")
    else:
        button_previous = Button(root_window, text="<<", padx=70, pady=20, command=lambda: back(image_number - 1), fg="black")

    button_wrap = Button(root_window, text="Cut Image", padx=70, pady=20, command=lambda: click_CutImage(image_number))
    status = Label(root_window, text="Image " + str(image_number +1) + " of " + str(len(image_list)), bd=1, relief=SUNKEN)

    button_wrap.grid(row=1, column=1, columnspan=2, sticky=W + E)
    my_image.grid(row=0, column=1, columnspan=3)
    button_next.grid(row = 0, column =4)
    button_previous.grid(row=0, column = 0)
    status.grid(row=2, column=0, columnspan=3, sticky = W+E)

def exit_program():
    global root_window, good_Image, bad_Image
    root_window.destroy()

def wrap_data(root):
    global my_image, image_list, status, image_path_list, root_window, path_list, image_numpy_array, root_window, original_numpy_array
    image_path_list = path_list
    root_window = root
    good_Image = []
    bad_Image = []
    image_list = []
    for image_path in path_list:
        image_array = cv.resize(cv.imread(image_path), (IMAGE_WIDTH_TO_SHOW, IMAGE_HEIGTH_TO_SHOW))
        image_numpy_array.append(image_array)
        image_list.append(ImageTk.PhotoImage(Image.fromarray(image_array)))
    original_numpy_array = image_numpy_array.copy()
    status = Label(root_window, text = "Image 1 of " + str(len(image_list)), bd =1, relief = SUNKEN)

    my_image = Label(root_window, image = image_list[0])
    my_image.grid(row = 0, column = 1, columnspan = 3)

    button_exit = Button(root_window, text = "Exit",padx = 70, pady = 20, command = exit_program)

    button_wrap = Button(root_window, text = "Cut Image",padx = 70, pady = 20, command = lambda: click_CutImage(0))

    button_next = Button(root_window, text=">>", padx=70, pady=20, command=lambda: next(1), fg="black")
    button_previous = Button(root_window, text="<<", padx=70, pady=20, state = DISABLED, fg="black")

    button_exit.grid(row = 1, column = 0)
    button_wrap.grid(row = 1, column = 1,  columnspan = 2, sticky = W+E)
    button_next.grid(row = 0, column =4)
    button_previous.grid(row = 0, column = 0)
    status.grid(row=2, column = 0 , columnspan = 3, sticky = W+E)
    root.mainloop()

def new_window_wrap_images(root, path_list_images):
    global path_list
    path_list = path_list_images
    top = Toplevel()
    top.title("Cropp the image")
    p = wrap_data(top)


# myButton = Button(root, text = "", padx = 50, pady = 20, command = lambda: new_window_wrap_images(root), fg = "black", bg = "green")
# myButton.grid(row = 1, column = 0)
class PageCroppImage():
    def __init__(self, rootTK, path_list_images):
        self.root = rootTK
        self.path_list_images = path_list_images












def main():
    root = Tk()
    path_list_images = [img1, img2, img3, img4]
    new_window_wrap_images(root, path_list_images)
    root.mainloop()

main()
