from find_faces.server import make_save_path


def test_make_save_path():
    input_path = "/home/dixneuf19/pictures/lana.jpg"
    assert make_save_path(input_path, 19) == "/home/dixneuf19/pictures/lana_out_19.jpg"
