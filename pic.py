#!/usr/bin/python3
#-*- coding: utf-8 -*-
from PIL import Image
import face_recognition
import numpy as np



class Picture:
    """
    """


    # transpose
    FLIP_LEFT_RIGHT = 0
    FLIP_TOP_BOTTOM = 1
    ROTATE_90 = 2
    ROTATE_180 = 3
    ROTATE_270 = 4
    TRANSPOSE = 5

    # resampling filters
    NEAREST = NONE = 0
    BOX = 4
    BILINEAR = LINEAR = 2
    HAMMING = 5
    BICUBIC = CUBIC = 3
    LANCZOS = ANTIALIAS = 1

    def __init__(self, file_path, open=False):
        self.file_path = file_path
        self.im = None
        self.raw = []
        self.face_location = []
        self.nb_face = 0

        if open:
            self.open()

    def open(self):
        self.im = Image.open(self.file_path)
    
    def save(self, outfile_path="", format=None):
        if outfile_path == "":
            outfile_path = self.file_path
        self.im.save(outfile_path, format)
    
    def show(self):
        if self.im == None:
            self.open()

        self.im.show()

    def image2raw(self):
        """
        Loads image into 3D Numpy array of shape 
        (width, height, bands)
        """
        if self.im == None:
            self.open()
        
        im_arr = np.fromstring(self.im.tobytes(), dtype=np.uint8)
        im_arr = im_arr.reshape((self.im.size[1],
                                 self.im.size[0], 
                                 self.im.im.bands))
        self.raw = im_arr


    def find_face(self, fromraw=True):
        """
        Update the list of the locations of the faces found on the Picture
        
        """
        if fromraw:
            
            if self.raw == []:
                self.image2raw()
            
            pic = self.raw
        else:
            pic = face_recognition.load_image_file(self.file_path)
            
        face_location = face_recognition.face_locations(pic)
        # current format : (top, right, bottom, left)
        # switching to (left, top, right, bottom) used by PIL
        for face in face_location:
            self.face_location.append((face[3], face[0],
                                       face[1], face[2]))

        self.nb_face = len(self.face_location)
        
    
    def rotate(self, method):
        """
        Rotate the image in 90 degree steps

        :param method: One of :py:attr:`hubphoto.FLIP_LEFT_RIGHT`,
          :py:attr:`hubphoto.FLIP_TOP_BOTTOM`, :py:attr:`hubphoto.ROTATE_90`,
          :py:attr:`hubphoto.ROTATE_180`, :py:attr:`hubphoto.ROTATE_270` or
          :py:attr:`hubphoto.TRANSPOSE`.
        :returns: Returns a flipped or rotated copy of this image.
        """
        self.im = self.im.transpose(method)

    def resize(self, size, conserv_ratio=0, resample=1):
        """
        resize the image
        if conserv_ratio = 1, conserv the original ratio of the picture
        """
        x, y = size
        if conserv_ratio:
            if self.im.width >= self.im.height:
                y = int(self.im.height * (x/self.im.width))
            else:
                x = int(self.im.width * (y/self.im.height))
        
        self.im = self.im.resize((x,y), resample)
        # we lose the location of faces
        self.face_location = []

    def ratio_cut(self, ratio, center=None):
        """
        Cut the edges of the image to have the correct ratio
        Can be centered on a specific place of the image
        """
        if center is None:
            center = (int(self.im.width/2), int(self.im.height/2))
        x, y = self.im.size
        if int(x*ratio[1] - y*ratio[0]) == 0:
            pass
        elif int(x*ratio[1] - y*ratio[0]) > 0:
            new_width = y*(ratio[0]/ratio[1])
            self.crop_on_place((int(center[0] - new_width/2), 0,
                                int(center[0] + new_width/2), self.im.height))
        else:
            new_height = x*(ratio[1]/ratio[0])
            self.crop_on_place((             0, int(center[1] - new_height/2),
                                self.im.height, int(center[1] + new_height/2)))
            

    def crop(self, box=None):
        """
        Cut a rectangular region from this image. The box is a
        4-tuple defining the left, upper, right, and lower pixel
        coordinate.
        """
        return self.im.crop(box)

    def update_face_location(self, box):
        face_locations = []
        nb_face = 0
        for i in range(self.nb_face):
            face = self.face_location[i]
                
            # check if this face is still on the picture
            if (     face[2] > box[2] 
                    or face[3] > box[3]
                    or face[0] < box[0]
                    or face[1] < box[1]):

                print("Face", i, "is cut")
            else:
                new_face = (face[0] - box[0], face[1] - box[1],
                            face[2] - box[0], face[3] - box[1])
                face_locations.append(new_face)
                nb_face += 1

        return (face_locations, nb_face)

    def crop_on_place(self, box):
        """
        crop the image and update it
        also update the location of faces
        """

        self.im = self.crop(box)
        self.face_location, self.nb_face = self.update_face_location(box)


    def face_crop(self, whichface=0, nb_face=1):
        pass