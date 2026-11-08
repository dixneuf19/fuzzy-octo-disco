import pytest

from fuzzyoctodisco.pic import *


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


def test_open_wrong_file():
    with pytest.raises(Exception, match="can't be read as an image with Pillow"):
        picture = Picture("find_faces/test/test_pic.py")
        picture.open()


def test_image2raw(pic_object):
    im_arr = image2raw(pic_object.im)
    assert im_arr.shape == (512, 512, 3)
    pixel = im_arr[19][19]
    assert pixel.tolist() == [225, 130, 109]


def test_find_faces_without_raw(pic_object):
    with pytest.raises(Exception):
        pic_object.find_faces()


def iou(a, b):
    left, top = max(a[0], b[0]), max(a[1], b[1])
    right, bottom = min(a[2], b[2]), min(a[3], b[3])
    inter = max(0, right - left) * max(0, bottom - top)
    area = lambda box: (box[2] - box[0]) * (box[3] - box[1])
    return inter / (area(a) + area(b) - inter)


def test_find_face(pic_object_raw):
    face_location = find_faces(pic_object_raw.raw)
    assert len(face_location) == 1
    # Lena's face, as boxed by the previous dlib HOG detector
    assert iou(face_location[0], (218, 219, 373, 374)) > 0.5


def test_find_face_grayscale_and_rgba(pic_object):
    for mode in ("L", "RGBA"):
        assert len(find_faces(image2raw(pic_object.im.convert(mode)))) == 1


def test_find_face_on_sideways_picture_needs_rotation(pic_object):
    pic_object.rotate(Picture.ROTATE_90)
    pic_object.img2raw()
    assert find_faces(pic_object.raw) == []


def test_face_crop_whithout_find_faces(pic_object_raw):
    with pytest.raises(Exception):
        pic_object.face_crop()


def test_face_crop_for_a_surnumerous_face(pic_object_faces):
    with pytest.raises(Exception):
        pic_object_faces.face_crop(whichface=1)


def test_face_crop(pic_object_faces):
    left, top, right, bottom = pic_object_faces.face_location[0]
    width, height = right - left, bottom - top
    pic_object_faces.face_crop()
    pic_object_faces.img2raw()
    assert pic_object_faces.raw.shape == (height, width, 3)
    assert pic_object_faces.face_location == [(0, 0, width, height)]


def test_rotate_90(pic_object):
    pic_object.rotate(Picture.ROTATE_90)
    im_arr = image2raw(pic_object.im)
    assert im_arr.shape == (512, 512, 3)
    pixel = im_arr[512 - (19 + 1)][19]
    assert pixel.tolist() == [225, 130, 109]


def test_clone(pic_object_raw):
    clone = pic_object_raw.clone()
    clone.img2raw()
    assert clone.raw.tolist() == pic_object_raw.raw.tolist()


def test_pic_per_face(pic_object_faces):
    pics = pic_object_faces.get_faces_as_Pic()
    assert len(pics) == 1
    pic = pics[0]
    pic.img2raw()
    pic_object_faces.face_crop()
    pic_object_faces.img2raw()
    assert pic.raw.tolist() == pic_object_faces.raw.tolist()
