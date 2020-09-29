import os
import numpy as np
from tkinter import *
from PIL import ImageTk, Image
import cv2 as cv

GRAYSHADE =150
MINPERCENT = 25
# *** The data is combination of TIF image (tif) of one line of text and txt Image (gt.txt) which is the lable of the image
# *** The name of the tif and the matching txt file should be the same - becouse there are lot of diffrent handwrite
# *** the user will insert his own ID and the name of each image will be calculate from uniqe ID of the image (integer)
# *** and the user ID - like: 1-316550797.tif, 1-316550797.gt.txt, 2-316550797.tif, 2-316550797.gt.txt etc.
DataFolder = r"C:\Users\Adi Rosental\Documents\she_code\shecode_final_project\DataBase"
infoFile = r"C:\Users\Adi Rosental\Documents\she_code\shecode_final_project\DataBase\info.txt"


def Insert_to_database(images_processed):
    f = open(infoFile, "r")
    list_of_lines = f.readlines()
    numImage = list_of_lines[0].split(" ")[-1]
    numStart = int(numImage)
    list_of_lines[0] = list_of_lines[0][:-(len(numImage))]
    numImage = int(numImage)
    image_path_list = []
    for imageP in images_processed:
        if CheckImage(imageP):
            nameImage = imageP.writerID +"_"+ str(numImage)
            pathNewImage = os.path.join(DataFolder, nameImage+".tif")
            image_path_list.append(pathNewImage)
            im = Image.fromarray(imageP.imageArray)
            im.save(pathNewImage, 'TIFF')
            f = open(os.path.join(DataFolder, nameImage+".gt.txt"), "w+", encoding="utf-8")
            f.write(imageP.Label)
            f.close()
            numImage += 1

    list_of_lines[0] = list_of_lines[0] + str(numImage)
    a_file = open(infoFile, "w", encoding="utf-8")
    a_file.writelines(list_of_lines)
    a_file.close()

    bad_Image = checkData(image_path_list)
    delete_from_database(bad_Image)
    return (numStart, numImage)

def delete_from_database(images_list_paths):
    for image_path in images_list_paths:
        os.remove(image_path)
        txt_file_path = image_path[:-4]+".gt.txt"
        os.remove(txt_file_path)

def CheckImage(imageP):
    imageArray = imageP.imageArray
    numDarkPixels = np.sum(imageArray < GRAYSHADE)
    numPixelsInImage = imageArray.size
    percent = (numDarkPixels / numPixelsInImage) * 100
    if percent > MINPERCENT:
        return False
    else:
        return True

def eccept(image_number):
    global my_label, button_eccept, button_remove, good_Image, bad_Image, image_list
    global status, good_Image, image_list
    good_Image.append(image_path_list[image_number])

    status.grid_forget()
    button_eccept = Button(root, text="OK", padx=70, pady=20, state=DISABLED, fg="black",
                           bg="green")
    button_remove = Button(root, text="Error", padx=70, pady=20, state=DISABLED, fg="black",
                           bg="red")

    my_label.grid(row=0, column=0, columnspan=3)
    button_eccept.grid(row=1, column=1)
    button_remove.grid(row=1, column=2)

def remove(image_number):
    global my_label, button_eccept, button_remove, status, good_Image, bad_Image, image_list, image_path_list
    bad_Image.append(image_path_list[image_number])
    my_label.grid_forget()
    button_eccept = Button(root, text="OK", padx=70, pady=20, state=DISABLED, fg="black",
                           bg="green")
    button_remove = Button(root, text="Error", padx=70, pady=20, state=DISABLED, fg="black",
                           bg="red")
    my_label.grid(row=0, column=0, columnspan=3)
    button_eccept.grid(row=1, column=1)
    button_remove.grid(row=1, column=2)

def foward(sign, image_number):
    global my_label, button_eccept, button_remove, status, good_Image, bad_Image, image_list, image_path_list

    if sign:
        good_Image.append(image_path_list[image_number - 1])
    else:
        bad_Image.append(image_path_list[image_number - 1])
    my_label.grid_forget()

    my_label = Label(image=image_list[image_number])
    button_eccept = Button(root, text="OK", padx=70, pady=20, command=lambda: foward(True, image_number + 1),
                           fg="black", bg="green")
    button_remove = Button(root, text="Error", padx=70, pady=20,
                           command=lambda: foward(False, image_number + 1), fg="black", bg="red")
    status = Label(root, text="Image " + str(image_number + 1) + " of " + str(len(image_list)), bd=1, relief=SUNKEN)

    if image_number == len(image_list) - 1:
        button_eccept = Button(root, text="OK", padx=70, pady=20, command=lambda: eccept(image_number), fg="black",
                               bg="green")
        button_remove = Button(root, text="Error", padx=70, pady=20, command=lambda: remove(image_number),
                               fg="black", bg="red")

    my_label.grid(row=0, column=0, columnspan=3)
    button_eccept.grid(row=1, column=1)
    button_remove.grid(row=1, column=2)
    status.grid(row=2, column=0, columnspan=3)

def exit_program():
    global root, good_Image, bad_Image

    print("Delete images: ")
    print(bad_Image)
    root.quit()


def checkData(path_list):
    global my_label, root, good_Image, bad_Image, image_list, status, image_path_list
    image_path_list = path_list
    root = Tk()
    root.title("Check Data")
    #root.iconbitmap(r"C:\Users\Adi Rosental\Documents\she_code\shecode_final_project\test_images\tesseracticon_dk8_icon.ico")

    good_Image = []
    bad_Image = []
    image_list = []
    for image_path in path_list:
        image_list.append(ImageTk.PhotoImage(Image.open(image_path)))

    status = Label(root, text = "Image 1 of " + str(len(image_list)), bd =1, relief = SUNKEN)

    my_label = Label(image = image_list[0])
    my_label.grid(row = 0, column = 0, columnspan = 3)

    button_exit = Button(root, text = "Exit",padx = 30, pady = 20, command = exit_program)

    button_eccept = Button(root, text="OK", padx=70, pady=20, command=lambda: foward(True, 1), fg="black", bg="green")
    button_remove = Button(root, text="Error", padx=70, pady=20, command=lambda: foward(False, 1), fg="black", bg="red")


    button_exit.grid(row = 1, column = 0)
    button_eccept.grid(row = 1, column = 1)
    button_remove.grid(row = 1, column = 2)
    status.grid(row=2, column = 0 , columnspan = 3, sticky = W+E)
    root.mainloop()
    return bad_Image