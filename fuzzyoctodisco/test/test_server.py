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
