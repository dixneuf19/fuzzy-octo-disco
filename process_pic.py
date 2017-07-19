#-*- coding: utf-8 -*-
from pic import Picture
from path import Path
import argparse
parser = argparse.ArgumentParser(
    description=
    "Process the picture or the directory, given the json config file")
parser.add_argument("path", help="Path for the picture or the directory")
parser.add_argument(
    "-n",
    "--nb_faces",
    type=int,
    help=
    "0 | 1 | n to don't search for any face | search and expect exactly one face | search for multiple face"
)
parser.add_argument(
    "--margin",
    "-m",
    type=float,
    help="Specify the margin around the face if the face_crop is activate")
parser.add_argument("--json", "-j", help="Path to a config file")
parser.add_argument(
    "--rotate", default=True, help="Try to rotate the picture to find faces")


def load_json_config(path):
    """
    Import a config file written in json
    """
    import json
    return json.loads(Path(path).text())
def find_faces(im, nb_faces, rotate):
    im.find_face()

    # if no faces found at all
    if im.nb_face == 0:
        print("No faces found in", file_path)

        # let's try to rotate the picture
        if rotate:
            print("Try to rotate the picture")
            i = 0
            while i < 3 and im.nb_face == 0:
                im.rotate(im.ROTATE_90)
                im.find_face()
                i += 1

            # No faces found
            if im.nb_face == 0:
                print("Tried all rotations, but no faces found in", file_path)
                return 0

        # Expecting only one_face, found more
    if nb_faces == 1 != im.nb_face:
        print("Found", im.nb_face, "faces, expecting only one face.")
        return 0

    return im.nb_face

def face_crop

def process_pic(file_path,
                resolution=None,
                nb_faces=1,
                margin=0.4,
                rotate=True):

    # check if the format is supported
    if not (file_path.ext in (".jpg", ".jpeg", ".png", ".gif")):
        print("The type of", filepath, "isn't supported.")
        return

    # create the Picture instance
    im = Picture(file_path)
    # try to open it
    try:
        im.open()
    except OSError:
        return

    # find faces, exit if it doesn't respect the nb_faces argument
    if nb_faces >= 1:
        nb_faces_found = find_faces(im, nb_faces, rotate)

        if nb_faces_found == 0:
            return

        # if everything went alright
        print("Found", im.nb_face, "face(s).")

    im.show()


if __name__ == '__main__':
    args = parser.parse_args()
    if args.json:
        config = load_json_config(args.json)
        x, y = config["resolution"].split("x")
        config["resolution"] = (int(x), int(y))
    else:
        config = {}
    # Shell options takes priority over json config
    args = vars(args)
    for key, value in args.items():
        if not value is None:
            config[key] = value

    c = config  # shorter name
    path = Path(c["path"])
    # Assume that the destination is a file

    file_path = path
    process_pic(file_path, c["resolution"], c["nb_faces"], c["margin"],
                c["rotate"])
