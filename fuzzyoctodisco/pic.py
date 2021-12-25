#!/usr/bin/python3
# -*- coding: utf-8 -*-

from copy import deepcopy

import face_recognition
import numpy as np
from path import Path
from PIL import Image


def image2raw(img):
    """
    Loads image into 3D Numpy array of shape
    (width, height, bands)
    """

    im_arr = np.frombuffer(img.tobytes(), dtype=np.uint8)
    im_arr = im_arr.reshape(
        (img.size[1], img.size[0], img.im.bands)
    )  # doesn't always works... (img formatting)
    return im_arr


def find_faces(raw_im):
    """
    Get the list of the locations of the faces found on the Picture
    """
    face_location_temp = face_recognition.face_locations(raw_im)
    # current format : (top, right, bottom, left)
    # switching to (left, top, right, bottom) used by PIL
    face_location = []
    for face in face_location_temp:
        face_location.append((face[3], face[0], face[1], face[2]))

    return face_location


def get_box4ratio_add(box, ratio, center=None):
    """
    Give the edges of the image to have the correct ratio by adding
    material
    Can be centered on a specific place of the image
    """
    if center is None:
        center = (
            int(box[0] + (box[2] - box[0]) / 2),
            int(box[1] + (box[3] - box[1]) / 2),
        )

    x, y = box[2] - box[0], box[3] - box[1]

    if int(x * ratio[1] - y * ratio[0]) == 0:
        return box
    elif int(x * ratio[1] - y * ratio[0]) > 0:
        new_height = x * (ratio[1] / ratio[0])
        return (
            box[0],
            int(center[1] - new_height / 2),
            box[2],
            int(center[1] + new_height / 2),
        )
    else:
        new_width = y * (ratio[0] / ratio[1])
        return (
            int(center[0] - new_width / 2),
            box[1],
            int(center[0] + new_width / 2),
            box[3],
        )


def get_box4ratio_cut(width, height, ratio, center=None):
    """
    Give the edges of the image to have the correct ratio by cutting
    material
    Can be centered on a specific place of the image
    """
    if center is None:
        center = (int(width / 2), int(height / 2))

    x, y = width, height

    if int(x * ratio[1] - y * ratio[0]) == 0:
        return None
    elif int(x * ratio[1] - y * ratio[0]) > 0:
        new_width = y * (ratio[0] / ratio[1])
        return (
            int(center[0] - new_width / 2),
            0,
            int(center[0] + new_width / 2),
            height,
        )
    else:
        new_height = x * (ratio[1] / ratio[0])
        return (
            0,
            int(center[1] - new_height / 2),
            height,
            int(center[1] + new_height / 2),
        )


def adjust_box(box, size):
    """
    function which try to adjust the box to fit it in a rectangle
    """
    # test if it can fit at all
    if box[2] - box[0] > size[2] - size[0] or box[3] - box[1] > size[3] - size[1]:

        return None

    else:
        if box[0] < size[0]:
            delta = size[0] - box[0]
            box = (box[0] + delta, box[1], box[2] + delta, box[3])
        elif box[2] > size[2]:
            delta = size[2] - box[2]
            box = (box[0] + delta, box[1], box[2] + delta, box[3])

        if box[1] < size[1]:
            delta = size[1] - box[1]
            box = (box[0], box[1] + delta, box[2], box[3] + delta)
        elif box[3] > size[3]:
            delta = size[3] - box[3]
            box = (box[0], box[1] + delta, box[2], box[3] + delta)

        return box


def crop(img, box=None):
    """
    Cut a rectangular region from this image. The box is a
    4-tuple defining the left, upper, right, and lower pixel
    coordinate.
    """
    return img.crop(box)


class Picture:
    """
    Class which can treat pictures with face_recognition and Pillow functions
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
        """
        init the Picture class, with a file_path
        :param file_path: path of the image file
        :param open: if you need to open the file while initializing the class
        :prop im: object representation of the image
        :prop raw: image as a 3D array
        :prop face_location: list of face location (quadruplets)
        :prop nb_face: nb of faces found ? (=len(face_location))
        :prop cut_error: error when cutting the pic
        """
        self.file_path = file_path
        self.im = None
        self.raw = []
        self.face_location = []
        self.nb_face = 0
        self.cut_error = False

        if open:
            self.open()

    def open(self):
        """
        Open the file and store it in the class
        """
        try:
            self.im = Image.open(Path(self.file_path).abspath())
        except OSError:
            raise Exception(
                "The file %s can't be read as an image with Pillow"
                % Path(self.file_path).abspath()
            )

    def save(self, outfile_path="", quality=90, overwrite=False):
        """
        Save the image at the outfile_path location.
        Overwrite the picture if no path is specified.
        Can specify the quality (90 by default)
        """
        if overwrite == True:
            outfile_path = self.file_path

        self.im.save(Path(outfile_path).abspath(), quality=quality)

    def show(self):
        """
        Display the image
        """
        if self.im is None:
            self.open()

        self.im.show()

    def clone(self):
        """
        Get a deepcopy of the Pic object
        """
        return deepcopy(self)

    def img2raw(self):
        """
        Apply img2raw in place
        """
        if self.im == None:
            raise Exception(
                "Need to open the image before transforming it to raw array"
            )

        self.raw = image2raw(self.im)

    def find_faces(self):
        """
        Apply find_faces in place
        """
        if len(self.raw) == 0:
            raise Exception("Need to get raw img array for face_recognition")

        self.face_location = find_faces(self.raw)

    def rotate(self, method):
        """
        Rotate the image in 90 degree steps

        :param method: One of :py:attr:`Picture.FLIP_LEFT_RIGHT`,
          :py:attr:`Picture.FLIP_TOP_BOTTOM`, :py:attr:`Picture.ROTATE_90`,
          :py:attr:`Picture.ROTATE_180`, :py:attr:`Picture.ROTATE_270` or
          :py:attr:`Picture.TRANSPOSE`.
        :returns: Returns a flipped or rotated copy of this image.
        We lose the correspondance img <-> raw so we reaply img2raw
        """
        self.im = self.im.transpose(method)
        self.img2raw()

    def resize(self, size, conserv_ratio=0, resample=1):
        """
        resize the image
        if conserv_ratio = 1, force the conservation of the original ratio of the picture
        We lose the correspondance img <-> raw
        """
        x, y = size
        if conserv_ratio:
            if self.im.width >= self.im.height:
                y = int(self.im.height * (x / self.im.width))
            else:
                x = int(self.im.width * (y / self.im.height))

        self.im = self.im.resize((x, y), resample)
        # we lose the location of faces
        self.face_location = []

    def ratio_cut(self, ratio, center=None):
        """
        Cut the edges of the images to have the correct ratio
        Can be centered on a specific place of the image
        """

        box = get_box4ratio_cut(self.im.width, self.im.height, ratio, center)

        if box is None:
            pass
        else:
            self.crop_on_place(box)

    def crop(self, box=None):
        """
        Cut a rectangular region from this image. The box is a
        4-tuple defining the left, upper, right, and lower pixel
        coordinate.
        """
        return crop(self.im, box)

    def get_updated_face_location(self, box):
        """
        update face_location after a crop (simulate it)
        discard if no more in the picture
        """

        face_locations = []
        nb_face = 0
        for i in range(len(self.face_location)):
            face = self.face_location[i]

            # check if this face is still on the picture
            if (
                face[2] > box[2]
                or face[3] > box[3]
                or face[0] < box[0]
                or face[1] < box[1]
            ):
                pass
            else:
                new_face = (
                    face[0] - box[0],
                    face[1] - box[1],
                    face[2] - box[0],
                    face[3] - box[1],
                )
                face_locations.append(new_face)
                nb_face += 1

        return face_locations

    def crop_on_place(self, box):
        """
        crop the image and update it
        also update the location of faces
        """

        self.im = self.crop(box)
        self.face_location = self.get_updated_face_location(box)

    def face_crop(self, ratio=None, margin=0, whichface=0):
        """
        cut around a face, adding a margin and eventually adjust the box for a
        correct ratio
        """

        # select the correct face
        if len(self.face_location) == 0:
            raise Exception("You need to found at least one face with find_faces first")
        elif len(self.face_location) <= whichface:
            raise Exception(
                "Only %d face found, can't crop on the %d nth"
                % (len(self.face_location), whichface)
            )
        box = self.face_location[whichface]

        # add the margin
        left, top, right, bottom = box
        face_height, face_width = bottom - top, right - left
        top, bottom = int(top - face_height * margin), int(
            bottom + face_height * margin
        )
        left, right = int(left - face_width * margin), int(right + face_width * margin)
        box = left, top, right, bottom

        # corect for the ratio
        if not (ratio is None):
            box = get_box4ratio_add(box, ratio)

        # check if it fits
        box = self.adjust_box(box)
        if box is None:
            raise Exception(
                "The box for the face, once ajusted for the ratio, doesn't fit"
            )

        # finally do the crop
        self.crop_on_place(box)

    def get_faces_as_Pic(self, ratio=None, margin=0):
        pic_per_face = []
        for i in range(len(self.face_location)):
            new_Pic = self.clone()
            new_Pic.face_crop(ratio, margin, whichface=i)
            pic_per_face.append(new_Pic)
        return pic_per_face

    def adjust_box(self, box):
        """
        method which try to adjust the box to fit it in the image
        """

        return adjust_box(box, (0, 0) + self.im.size)
