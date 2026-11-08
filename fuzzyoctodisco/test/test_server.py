from fuzzyoctodisco.main import make_save_path


def test_make_save_path():
    input_path = "/home/dixneuf19/pictures/lana.jpg"
    assert make_save_path(input_path, 19) == "/home/dixneuf19/pictures/lana_out_19.jpg"


def test_find_faces_rotates_a_sideways_picture():
    from fuzzyoctodisco.main import find_faces
    from fuzzyoctodisco.pic import Picture

    picture = Picture("pictures/lena.png")
    picture.open()
    picture.rotate(Picture.ROTATE_270)
    picture.img2raw()
    assert find_faces(picture, nb_faces=1) == 1


def test_find_faces_does_not_rotate_when_only_small_faces():
    from fuzzyoctodisco.main import find_faces
    from fuzzyoctodisco.pic import Picture

    picture = Picture("pictures/lena.png")
    picture.open()
    picture.im = picture.im.resize((128, 128))  # lena's face becomes about 37 px
    picture.img2raw()
    assert find_faces(picture) == 0
    assert picture.has_small_faces
    assert picture.im.size == (128, 128)
