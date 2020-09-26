

# *** The data is combination of TIF image (tif) of one line of text and txt Image (gt.txt) which is the lable of the image
# *** The name of the tif and the matching txt file should be the same - becouse there are lot of diffrent handwrite
# *** the user will insert his own ID and the name of each image will be calculate from uniqe ID of the image (integer)
# *** and the user ID - like: 1-316550797.tif, 1-316550797.gt.txt, 2-316550797.tif, 2-316550797.gt.txt etc.

def Insert_to_database():
    Check_data()
    pass


def delete_from_database(lineID_start, lineID_stop = None):
    if lineID_stop == None:
        lineID_stop = lineID_start
    pass

def Check_data():
    pass