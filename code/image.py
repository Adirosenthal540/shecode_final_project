import numpy as np

class Image():
    def __init__(self, imageList, isHandwrite = 0, label = -1):
        self.image = imageList
        self.imageWidth = self.image.shape[1]
        self.imageHeight = self.image.shape[0]
        self.isHandwrite = isHandwrite
        self.label = label

    def cutImage(self, x1, y1, x2, y2):
        img_cut = self.image[min(y1,y2):max(y1,y2), min(x1,x2):max(x1,x2)]
        return img_cut

class Letter(Image):
    def __init__(self, imageList, isHandwrite=0, label=-1):
        super().__init__(self, imageList, isHandwrite=0, label=-1)

