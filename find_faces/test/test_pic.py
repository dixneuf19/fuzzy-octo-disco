import pytest
import matplotlib.pyplot as plt
from find_faces.pic import *

@pytest.fixture
def pic_object():
    picture = Picture("pictures/lena.png")
    picture.open()
    return picture


@pytest.fixture
def pic_object_raw(pic_object):
    pic_object.img2raw()
    return pic_object

@pytest.fixture
def pic_object_faces(pic_object_raw):
    pic_object_raw.find_faces()
    return pic_object_raw


def test_image2raw(pic_object):
    im_arr = image2raw(pic_object.im)
    assert im_arr.shape == (512, 512, 3)
    pixel = im_arr[19][19]
    assert pixel.tolist() == [225, 130, 109]

def test_find_faces_without_raw(pic_object):
    with pytest.raises(Exception):
        pic_object.find_faces()

def test_find_face(pic_object_raw):
    face_location = find_faces(pic_object_raw.raw)
    assert face_location == [(218, 219, 373, 374)]

def test_face_crop_whithout_find_faces(pic_object_raw):
    with pytest.raises(Exception):
        pic_object.face_crop()
    
def test_face_crop_for_a_surnumerous_face(pic_object_faces):
    with pytest.raises(Exception):
        pic_object_faces.face_crop(whichface=1)

def test_face_crop(pic_object_faces):
    pic_object_faces.face_crop()
    pic_object_faces.img2raw()
    assert pic_object_faces.raw.shape == (155, 155, 3)
    assert pic_object_faces.face_location == [(0, 0, 155, 155)]



