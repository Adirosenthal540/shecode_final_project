import Controller
import ImageProcessing
import HandwrittenDoc
import DataManager
#from DataManager import check_database
import cv2 as cv
from PIL import Image
import sys, numpy as np
from matplotlib import pyplot as plt
import os, math
from pdf2image import convert_from_path
from tkinter import *
from tkinter import messagebox, filedialog
from PIL import ImageTk, Image
from pdf2image.exceptions import PDFInfoNotInstalledError, PDFPageCountError, PDFSyntaxError


def Status_program(i):
    switcher={
        0: "Create_data" ,
        1: "Extract_text" ,
        }
    return switcher.get(i, " ")

def maessage_type(i):
    switcher={
        0: "information" ,
        1: "warning" ,
        2: "error"
        }
    return switcher.get(i, " ")

def insertDocuments(i):
    switcher={
        "Scanned":0  ,
        "Labeled":1 ,
        }
    return switcher.get(i, " ")

IMAGE_WIDTH_TO_SHOW = 500
IMAGE_HEIGHT_TO_SHOW = 500
INPUT_NUM_TRYS = 2
POPPLER_PATH = "C:\\poppler-20.09.0\\bin"

image_numpy_array = []
original_numpy_array = []
points = []
images_path = []
images = []
txt_file = []

global root
# folder_selected = ""
# markTextArea = False
# status_program = None
# image_selected_path = ""
# image_selected = None
# scannedInsertDocuments = None

def reset_global_parameters():
    global folder_selected, markTextArea, markTextArea, image_selected_path, images
    global image_selected, scannedInsertDocuments, delete_files, txtFiles, points
    folder_selected = ""
    markTextArea = False
    status_program = None
    image_selected_path = ""
    image_selected = None
    scannedInsertDocuments = None
    delete_files = []
    txtFiles = []
    points = []
    images =[]


def popup_message(message, type):
    if type.lower() == "information":
        response = messagebox.showinfo("information", message)
    elif type.lower() == "error":
        response = messagebox.showerror("ERROR", message)
    elif type.lower() == "warning":
        response = messagebox.showwarning("WARNING", message)


def CheckImage(file):
    valid_images = [".jpg", ".gif", ".png", ".tif", ".tiff"]
    ext = os.path.splitext(file)[1]
    if ext.lower() not in valid_images:
        return False
    else:
        return True

def CheckPDF(file):
    ext = os.path.splitext(file)[1]
    if ext.lower() =='.pdf':
        return True
    else:
        return False

# The Image of the training will be extract to same path where it save
def ExtractImagesFromPDF(file, files):
    global delete_files
    order = HandwrittenDoc.check_PDF_name(file)
    images = convert_from_path(file, fmt="jpeg", poppler_path =POPPLER_PATH)
    outputpath, namefile = os.path.split(file)
    handwrite_ID = namefile.split("_")[0]
    i = 0
    for image in images:
        # image = Image.open(im)
        new_path_image = os.path.join(outputpath, handwrite_ID +"_"+ str(order[i]) + ".tif")
        j=0
        while (new_path_image in files):
            new_path_image = os.path.join(outputpath, handwrite_ID + "_"+str(j)+"_" + str(order[i]) + ".tif")
            j += 1
        i += 1
        image.save(new_path_image, 'TIFF')
        files.append(new_path_image)
        delete_files.append(new_path_image)
    return files

# the func save all the paths of the images and text files(optional)
# input: path of a folder,  is_txtFiles = true if want to find also text files
# output: list of all the images ans text files (if is_txtFiles is true)
def Extract_files_from_folder(folder, scanned = False):
    imagesInFolder = []
    txtFiles = []
    files = os.listdir(folder)
    flag = 0
    for file in files:
        if (CheckImage(file) == False) :
            if (CheckPDF(file) == True and scanned):
                files = files + ExtractImagesFromPDF(os.path.join(folder,file), files)
            continue
        elif not scanned:
            nameImage = os.path.splitext(file)[0]
            if nameImage+".txt" in files :
                txtFiles.append(os.path.join(folder, nameImage+".txt"))
            elif nameImage+".gt.txt" in files:
                txtFiles.append(os.path.join(folder, nameImage + ".gt.txt"))
            else:
                popup_message("the image '" + file + "' has no .txt file",  maessage_type(1))
                continue
        else:
            if not HandwrittenDoc.Check_image_name(file):
                namefile = os.path.basename(file)
                popup_message("WRONG INPUT IMAGE NAME - "+namefile,  maessage_type(1))
                continue
        imagesInFolder.append(os.path.join(folder, file))

    return imagesInFolder, txtFiles


def deleteFiles(delete_files):
    for file in delete_files:
        os.remove(file)


def openFolder():
    global frame_scanned_label, folder_selected, frame, root, mark_Button
    root.withdraw()
    folder_selected = filedialog.askdirectory()
    root.deiconify()
    mylabel_folder = Label(frame_scanned_label, text=folder_selected)
    mylabel_folder.grid(row=9, column=0,  sticky = W+E)
    mark_Button = Button(frame_scanned_label, text="Mark the text", command=Popup_Mark_the_text, bg="hot pink").grid(row=5, column=0, columnspan = 2, sticky=W + E)
    run_Button = Button(frame_scanned_label, text = "RUN", command = run_program, bg="turquoise").grid(row=6, column=0, columnspan = 2, sticky=W + E)


def clicked_Radiobutton(value):
    global myButton, frame, frame_scanned_label, folder_selected
    global folder_selected, scannedInsertDocuments

    frame_scanned_label.destroy()
    frame_scanned_label = Frame(frame)
    frame_scanned_label.grid(row=4, column=0, columnspan=2, sticky=W + E)
    folder_selected = ""
    # choose Scanned handwrite
    if value ==insertDocuments("Scanned"):

        scannedInsertDocuments = True
        myButton = Button(frame_scanned_label, text="Select Folder with scanned paged (PDF \ Image formats)", padx = 10, pady = 20,  command=openFolder)

    elif value ==insertDocuments("Labeled"):
        scannedInsertDocuments = False
        myButton = Button(frame_scanned_label, text="Select Folder with your files (tif, txt)",
                          padx=10, pady=20, command=openFolder)

    myButton.grid(row=1,column = 0, columnspan=5)
    mainloop()

def Popup_Mark_the_text():
    global markTextArea
    response = messagebox.askyesno("Mark the text", "Do you wont to select the area of the text on the documents?")
    markTextArea = response

def chooseScannedOrLabeled():
    global mylabel_radio, clicked, frame, frame_scanned_label
    frame_scanned_label = Frame(frame)
    frame_scanned_label.grid(row=4, column =0, columnspan = 2, sticky = W+E)
    r = IntVar()
    r.set("1")
    myLabel = Label(frame, text="Colecting data for training tesseract")
    Radiobutton1 = Radiobutton(frame, text = "Scanned handwrite", variable = r, value = 0, command = lambda:clicked_Radiobutton(r.get()))
    Radiobutton2 = Radiobutton(frame, text = "Labeled Image", variable = r, value = 1, command = lambda:clicked_Radiobutton(r.get()))

    myLabel.grid(row=0, column=0, columnspan =2, sticky = W+E)
    Radiobutton1.grid(row=3, column=0, sticky = W+E)
    Radiobutton2.grid(row=3, column=1, sticky = W+E)
    frame.mainloop()

def show_image():
    global frameExtract, image_selected, flag_show, canvas_image
    canvas_image = Canvas(frameExtract, width = image_selected.width(), height = image_selected.height())
    canvas_image.grid(row=1, column=0, columnspan=3, sticky=W + E)
    #image_label = Label(frameExtract, image=image_selected).grid(row=4, column = 0, columnspan = 3, sticky=W + E)
    canvas_image.create_image((image_selected.width()/2,image_selected.height()/2) , image = image_selected)
    flag_show = 0
    show_image_butten = Button(frameExtract, text="show image", state=DISABLED).grid(row=0, column=0, sticky=W + E)
    hide_image_butten = Button(frameExtract, text="hide image", command=hide_image).grid(row=0, column=1, sticky=W + E)

def hide_image():
    global frameExtract, image_selected, canvas_image
    canvas_image.delete('all')
    canvas_image.grid_forget()
    show_image_butten = Button(frameExtract, text="show image", command=show_image).grid(row=0, column=0, sticky=W + E)
    hide_image_butten = Button(frameExtract, text="hide image", state=DISABLED).grid(row=0, column=1, sticky=W + E)

def showImageAndExtractedText():
    global image_selected, frame, frameExtract, image_label, frameMarkRun
    image_label = None

    frameExtract.destroy()
    frameExtract = Frame(frame)
    frameMarkRun = Frame(frameExtract).grid(row=2, column=0, columnspan=2, sticky=W + E)
    frameMarkRun = Frame(frameExtract).grid(row=2, column=0, columnspan=2, sticky = W+E)
    frameExtract.grid(row=3, column=0, columnspan=2, sticky = W+E)

    insert_image_butten = Button(frame, text="Open image", command=get_image).grid(row=2, column=0, columnspan=2, sticky=W + E)

def get_image():
    global root, image_selected, frame, clicked, options, flag_show, frameExtract, image_selected_path, mark_Button, frameMarkRun
    frameMarkRun = Frame(frameExtract)
    frameMarkRun.grid(row=2, column=0, columnspan=2, sticky=W + E)
    flag_show = 1
    root.filename = filedialog.askopenfilename(title="select a file", filetype=(("ALL FILES", "*.*"),("JPEG", "*.jpg"),("PNG", "*.png"), ("TIF", "*.tif")))
    image_selected_path = root.filename
    image_array = cv.imread(image_selected_path, 0)
    width, height = calculate_width_height(image_array, IMAGE_WIDTH_TO_SHOW, IMAGE_HEIGHT_TO_SHOW)
    image_selected = ImageTk.PhotoImage(Image.open(image_selected_path).resize((width, height)))

    show_image_butten = Button(frameExtract, text="show image", command=show_image).grid(row=0, column=0, sticky=W + E)
    hide_image_butten = Button(frameExtract, text="hide image", state=DISABLED).grid(row=0, column=1, sticky=W + E)
    mark_Button = Button(frameMarkRun, text="Mark the text", command=Popup_Mark_the_text, bg="hot pink").grid(row=5, column=0, columnspan = 2, sticky=W + E)
    run_Button = Button(frameMarkRun, text="RUN", command=run_program, bg="turquoise").grid(row=6, column=0, columnspan = 2, sticky=W + E)

def Select_train_test(var):
    global myLabel, clicked, frame, options, root, status_program, image_label, image_selected, image_selectedTK, frameExtract, frameMarkRun
    reset_global_parameters()
    frame.destroy()
    frameExtract.destroy()
    frame_text.destroy()
    value = clicked.get()
    frame = Frame(root)
    frame.grid(row=3, column=0, columnspan=2, sticky = W+E)

    #is Train - collect Data
    if value == Status_program(0):
        status_program = Status_program(0)
        myLabel = Label(frame, text="Collecting data for training tesseract").grid(row=0, sticky = W+E)

        drop = OptionMenu(root, clicked, *options, command=Select_train_test)
        drop.grid(row=1, column=0, columnspan = 2, sticky = W+E)
        chooseScannedOrLabeled()

    if value == Status_program(1):
        status_program = Status_program(1)
        myLabel = Label(frame, text="Run tesseract on the lateset training machine").grid(row=0, sticky = W+E)
        drop = OptionMenu(root, clicked, *options, command=Select_train_test)
        drop.grid(row=1, column=0, columnspan = 2, sticky = W+E)
        insert_image_butten = Button(frame, text="Open image", command=get_image).grid(row=2, column=0, columnspan = 2, sticky = W+E)
        showImageAndExtractedText()
    frame.mainloop()

def eccept(image_number):
    global my_image, button_eccept, button_remove, good_Image, bad_Image, image_list, root_window
    global status, good_Image, image_list
    good_Image.append(image_path_list[image_number])

    status.grid_forget()
    button_eccept = Button(root_window, text="OK", padx=70, pady=20, state=DISABLED, fg="black",
                           bg="green")
    button_remove = Button(root_window, text="Error", padx=70, pady=20, state=DISABLED, fg="black",
                           bg="red")

    my_image.grid(row=0, column=0, columnspan=3, sticky = W+E)
    button_eccept.grid(row=1, column=1, sticky = W+E)
    button_remove.grid(row=1, column=2, sticky = W+E)

def remove(image_number):
    global my_image, button_eccept, button_remove, status, good_Image, bad_Image, image_list, image_path_list, root_window
    bad_Image.append(image_path_list[image_number])
    my_image.grid_forget()
    button_eccept = Button(root_window, text="OK", padx=70, pady=20, state=DISABLED, fg="black",
                           bg="green")
    button_remove = Button(root_window, text="Error", padx=70, pady=20, state=DISABLED, fg="black",
                           bg="red")
    my_image.grid(row=0, column=0, columnspan=3)
    button_eccept.grid(row=1, column=1)
    button_remove.grid(row=1, column=2)

def foward(sign, image_number):
    global my_image, button_eccept, button_remove, status, good_Image, bad_Image, image_list, image_path_list, root_checkData

    if sign:
        good_Image.append(image_path_list[image_number - 1])
    else:
        bad_Image.append(image_path_list[image_number - 1])
    my_image.grid_forget()

    my_image = Label(root_checkData, image=image_list[image_number])
    button_eccept = Button(root_checkData, text="OK", padx=70, pady=20, command=lambda: foward(True, image_number + 1),
                           fg="black", bg="green")
    button_remove = Button(root_checkData, text="Error", padx=70, pady=20,
                           command=lambda: foward(False, image_number + 1), fg="black", bg="red")
    status = Label(root_checkData, text="Image " + str(image_number + 1) + " of " + str(len(image_list)), bd=1, relief=SUNKEN)

    if image_number == len(image_list) - 1:
        button_eccept = Button(root_checkData, text="OK", padx=70, pady=20, command=lambda: eccept(image_number), fg="black",
                               bg="green")
        button_remove = Button(root_checkData, text="Error", padx=70, pady=20, command=lambda: remove(image_number),
                               fg="black", bg="red")

    my_image.grid(row=0, column=0, columnspan=3)
    button_eccept.grid(row=1, column=1)
    button_remove.grid(row=1, column=2)
    status.grid(row=2, column=0, columnspan=3)

def exit_program():
    global root_checkData, good_Image, bad_Image
    root_checkData.destroy()


def checkData(path_list, top):
    global my_image, good_Image, bad_Image, image_list, status, image_path_list
    image_path_list = path_list
    # root = Tk()
    # root.title("Check Data")
    #root.iconbitmap(r"C:\Users\Adi Rosental\Documents\she_code\shecode_final_project\test_images\tesseracticon_dk8_icon.ico")
    good_Image = []
    bad_Image = []
    image_list = []
    root_checkData = top
    for image_path in path_list:
        image_list.append(ImageTk.PhotoImage(Image.open(image_path)))

    status = Label(root_checkData, text = "Image 1 of " + str(len(image_list)), bd =1, relief = SUNKEN)

    my_image = Label(root_checkData, image = image_list[0])
    my_image.grid(row = 0, column = 0, columnspan = 3)

    button_exit = Button(root_checkData, text = "Exit",padx = 30, pady = 20, command = exit_program)

    button_eccept = Button(root_checkData, text="OK", padx=70, pady=20, command=lambda: foward(True, 1), fg="black", bg="green")
    button_remove = Button(root_checkData, text="Error", padx=70, pady=20, command=lambda: foward(False, 1), fg="black", bg="red")


    button_exit.grid(row = 1, column = 0)
    button_eccept.grid(row = 1, column = 1)
    button_remove.grid(row = 1, column = 2)
    status.grid(row=2, column = 0 , columnspan = 3, sticky = W+E)
    root_checkData.mainloop()
    return bad_Image

def new_window_check_database(root):
    path_list = DataManager.list_image_path_database()
    top = Toplevel()
    top.title("check database")
    bad_Image = checkData(path_list, top)
    DataManager.delete_from_database(bad_Image)

def click_CutImage(num_image) :
    global points, file, img_toCut, top2, w, path_list, image_numpy_array, num_image_to_cut, cv_array, original_numpy_array
    top2 = Toplevel()
    top2.title("Cut image window")
    points = []
    w = Canvas(top2, width=IMAGE_WIDTH_TO_SHOW, height=IMAGE_HEIGHT_TO_SHOW)
    cv_array = original_numpy_array[num_image].copy()

    img_toCut = ImageTk.PhotoImage(Image.fromarray(cv_array))
    image_numpy_array[num_image] = cv_array.copy()
    num_image_to_cut = num_image
    w.create_image(0, 0, image=img_toCut, anchor="nw")
    w.grid(row=0)
    top2.bind("<Button 1>", CutImage)


def CutImage(eventorigin):
    global x, y, points, img_toCut, top2, w, path_list, image_numpy_array, num_image_to_cut, cv_array, root_window

    while(len(points)<4):
        x = eventorigin.x
        y = eventorigin.y

        cv_array = cv.circle(cv_array, (x, y), 3, 0, -1)
        points.append((x, y))
        if len(points) >= 2:
            cv_array = cv.line(cv_array, points[-1], points[-2], 50, 3)

        img_toCut = ImageTk.PhotoImage(Image.fromarray(cv_array))
        w.create_image(0, 0, image=img_toCut, anchor="nw")

        top2.bind("<Button 1>", CutImage)
        top2.mainloop()
    top2.destroy()

    image_numpy_array[num_image_to_cut] = ImageProcessing.WrapImage(image_numpy_array[num_image_to_cut], np.array(points[0:4]))
    image_list[num_image_to_cut] = ImageTk.PhotoImage(Image.fromarray(image_numpy_array[num_image_to_cut]))

    status = Label(root_window, text = "Image "+str(num_image_to_cut+1)+" of " + str(len(image_list)), bd =1, relief = SUNKEN)
    my_image = Label(root_window, image = image_list[num_image_to_cut])
    my_image.grid(row = 0, column = 1, columnspan = 3)
    button_exit = Button(root_window, text = "Exit",padx = 70, pady = 20, command = exit_wrap)
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

def exit_wrap():
    global root_window, good_Image, bad_Image
    root_window.destroy()
    run_program(finishWrop = True)

def wrap_data(root, width, height):
    global my_image, image_list, status, image_path_list, root_window, path_list, image_numpy_array, root_window, original_numpy_array
    image_path_list = path_list
    root_window = root
    good_Image = []
    bad_Image = []
    image_list = []
    for image_path in path_list:
        image_array = cv.imread(image_path, 0)
        width, height = calculate_width_height(image_array, IMAGE_WIDTH_TO_SHOW, IMAGE_HEIGHT_TO_SHOW)
        image_array = cv.resize(image_array, (width, height))
        image_numpy_array.append(image_array)
        image_list.append(ImageTk.PhotoImage(Image.fromarray(image_array)))
    original_numpy_array = image_numpy_array.copy()
    status = Label(root_window, text = "Image 1 of " + str(len(image_list)), bd =1, relief = SUNKEN)

    my_image = Label(root_window, image = image_list[0])
    my_image.grid(row = 0, column = 1, columnspan = 3)

    button_exit = Button(root_window, text = "Exit",padx = 70, pady = 20, command = exit_wrap)

    button_wrap = Button(root_window, text = "Cut Image",padx = 70, pady = 20, command = lambda: click_CutImage(0))

    button_next = Button(root_window, text=">>", padx=70, pady=20, command=lambda: next(1), fg="black")
    button_previous = Button(root_window, text="<<", padx=70, pady=20, state = DISABLED, fg="black")

    button_exit.grid(row = 1, column = 0)
    button_wrap.grid(row = 1, column = 1,  columnspan = 2, sticky = W+E)
    button_next.grid(row = 0, column =4)
    button_previous.grid(row = 0, column = 0)
    status.grid(row=2, column = 0 , columnspan = 3, sticky = W+E)
    root.mainloop()

def new_window_wrap_images(root, path_list_images, width, height):
    global path_list
    path_list = path_list_images
    top = Toplevel()
    top.title("Cropp the image")
    wrap_data(top, width, height)


def calculate_width_height(image_array, max_width_to_show, max_height_to_show):
    width_original = image_array.shape[1]
    height_original = image_array.shape[0]
    if width_original < max_width_to_show and height_original  < max_height_to_show:
        return width_original, height_original

    if width_original > height_original:
        new_width = max_width_to_show
        new_height = math.floor(height_original * (max_width_to_show / width_original))
    else:
        new_height = max_height_to_show
        new_width = math.floor(width_original * (max_height_to_show / height_original))

    return new_width, new_height

def extractResult(result):
    root.withdraw()
    folder_to_save = filedialog.askdirectory()
    root.deiconify()
    baseNameImage = os.path.basename(images[0].imagePath)
    nameImage = os.path.splitext(baseNameImage)[0]
    f = open(os.path.join(folder_to_save,  nameImage+ ".txt"), "w+", encoding="utf-8")
    f.write(result)
    f.close()

def showResults(root, result):
    global frame_scanned_label, frame, mark_Button, frameMarkRun, frame_text
    if  status_program == Status_program(0):
        run_Button = Button(frame_scanned_label, text="RUN", state = DISABLED).grid(row=6, column=0,columnspan=2,sticky=W + E)
    else:
        insert_image_butten = Button(frame, text="Open image",  state=DISABLED).grid(row=2, column=0, columnspan=2, sticky=W + E)
        frameMarkRun.destroy()
    frame_text = Frame(root, relief =  SUNKEN)

    xscrollbar = Scrollbar(frame_text, orient = HORIZONTAL)
    xscrollbar.grid(row = 2, column = 0, sticky = E+W)

    yscrollbar = Scrollbar(frame_text)
    yscrollbar.grid(row = 0, column = 10, sticky = N + S)
    my_result = Text(frame_text, bg = "CadetBlue1", bd = 4, width = 50, xscrollcommand = xscrollbar.set )
    my_result.tag_configure('tag-right', justify='right')
    my_result.insert('end', str(result) , 'tag-right')
    #my_result.insert(INSERT, result)
    scrl = Scrollbar(root, command=my_result.yview)
    my_result.config(yscrollcommand=scrl.set)
    my_result.grid(row=0, column=0, sticky = N+S+E+W)

    xscrollbar.config(command = my_result.xview)
    yscrollbar.config(command = my_result.yview)

    frame_text.grid(row=4, column=0, columnspan=3)

    if status_program == Status_program(0) and scannedInsertDocuments:
        popup_message("Secceeded reading the scanned pages and insert into the Database", maessage_type(0))
    elif status_program == Status_program(0):
        popup_message("Secceeded insert the labeled data into the database", maessage_type(0))
    else:
        popup_message("Finish the export of the text from the image - look at the results :)", maessage_type(0))

    try_again_Button = Button(frame_text, text="Try again", command=lambda: Select_train_test(0)).grid(row=1, column=0,columnspan=2,sticky=W + E)
    save_Button = Button(frame_text, text="Extract result", command=lambda: extractResult(result)).grid(row=2, column=0,columnspan=2,sticky=W + E)


def run_program(finishWrop = False):
    global folder_selected, markTextArea, image_selected_path, image_selected, scannedInsertDocuments, root
    global images, txtFiles, points, delete_files, images_path
    print(1111)
    print ("folder_selected: "+folder_selected)
    print ("scannedInsertDocuments "+str(scannedInsertDocuments))
    print ("markTextArea "+str(markTextArea))
    print ("status_program "+str(status_program))
    print ("image_selected_path "+image_selected_path)
    isTrain = status_program == Status_program(0)
    if (not markTextArea):
        if status_program == Status_program(0):
            images_path, txtFiles = Extract_files_from_folder(folder_selected,  scannedInsertDocuments)

            for image_path in images_path:
                image_array = cv.imread(image_path, 0)
                width, height = calculate_width_height(image_array, IMAGE_WIDTH_TO_SHOW ,IMAGE_HEIGHT_TO_SHOW)
                image_numpy_array.append(cv.resize(image_array, (width, height)))

            for i in range(len(images_path)):
                handwrite_ID = os.path.basename(images_path[i]).split("_")[0]
                if scannedInsertDocuments:
                    images.append( ImageProcessing.ImageProcessing(image_numpy_array[i], imagePath=images_path[i], handwrite_ID=handwrite_ID))
                else:
                    txt_file = open(txtFiles[i], "r", encoding="utf-8")
                    text = txt_file.read()
                    txt_file.close()
                    images.append(ImageProcessing.ImageProcessing(image_numpy_array[i], label= text, imagePath=images_path[i], writerID=handwrite_ID))

        # no resize for the selected image
        elif status_program == Status_program(1):
            image_array = cv.imread(image_selected_path, 0)
            # width, height = calculate_width_height(image_array, IMAGE_WIDTH_TO_SHOW, IMAGE_HEIGHT_TO_SHOW)
            # image_array = cv.resize(image_array, (width, height))
            images.append(ImageProcessing.ImageProcessing( image_array, imagePath=image_selected_path))

    elif not finishWrop:
        if status_program == Status_program(0):
            images_path, txtFiles = Extract_files_from_folder(folder_selected,  scannedInsertDocuments)
            new_window_wrap_images(root, images_path, IMAGE_WIDTH_TO_SHOW, IMAGE_HEIGHT_TO_SHOW)
        # no resize for the selected image
        elif status_program == Status_program(1):
            new_window_wrap_images(root, [image_selected_path], IMAGE_WIDTH_TO_SHOW, IMAGE_HEIGHT_TO_SHOW)

    # after cropp of the images
    else:
        if status_program == Status_program(0):
            for i in range(len(images_path)):
                handwrite_ID = os.path.basename(images_path[i]).split("_")[0]
                if scannedInsertDocuments:
                    images.append(ImageProcessing.ImageProcessing(image_numpy_array[i], imagePath=images_path[i], handwrite_ID=handwrite_ID))
                else:
                    txt_file = open(txtFiles[i], "r", encoding="utf-8")
                    text = txt_file.read()
                    txt_file.close()
                    images.append(ImageProcessing.ImageProcessing(image_numpy_array[i], label = text, imagePath=images_path[i],
                                              writerID=handwrite_ID))
        elif status_program == Status_program(1):
            images.append(ImageProcessing.ImageProcessing(image_numpy_array[0], imagePath=image_selected_path))

    controller = Controller.Controller(isTrain, images, root, isScanned = scannedInsertDocuments)
    result = controller.main()
    showResults(root, result)
    print(result)

def main():
    global folder_selected, markTextArea, image_selected_path, image_selected, scannedInsertDocuments
    global txtFiles, points, delete_files, clicked, root, options, frame , frameExtract, frame_text
    reset_global_parameters()
    root = Tk()
    root.title("convert a picture in Hebrew to machine encoded text - Adi Rosenthal")

    frame = Frame(root)
    frame.grid(row=3, column=0,  sticky = W+E)
    frameExtract = Frame(frame)
    frameExtract.grid(row=3, column=0, columnspan=2, sticky=W + E)
    frame_text = Frame(root, relief=SUNKEN)
    frame_text.grid(row=4, column=0, columnspan=3)
    menubar = Menu(root)

    filemenu = Menu(menubar, tearoff=0)
    filemenu.add_separator()
    filemenu.add_command(label="Exit", command=root.destroy)
    menubar.add_cascade(label="File", menu=filemenu)

    datamenu = Menu(menubar, tearoff=0)
    datamenu.add_command(label="Check Data", command=lambda: new_window_check_database(root))
    menubar.add_cascade(label="Data", menu=datamenu)

    helpmenu = Menu(menubar, tearoff=0)
    menubar.add_cascade(label="Help", menu=helpmenu)

    root.config(menu=menubar)

    options = ["-", Status_program(0),Status_program(1)]

    clicked = StringVar()
    clicked.set(options[0])
    myLabel = Label(root, text="Choose one of the options - "+Status_program(0)+" or "+Status_program(1) +":")
    drop = OptionMenu(root, clicked, *options, command=Select_train_test)

    myLabel.grid(row=0, column=0,  sticky = W+E)
    drop.grid(row=1, column=0,  sticky = W+E)

    deleteFiles(delete_files)
    root.mainloop()

if __name__ == "__main__":
    main()



    # 1) switch case : enum - with all the values
    # 2) print errors with the gui
    # 3) work on the power point - vm, docker ,  vedio -

