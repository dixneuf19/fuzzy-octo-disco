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
parser.add_argument(
    "--skip_compression", action='store_true', help="skip compression")
parser.add_argument(
    "--resolution",
    "-r",
    help=
    "ratio and resolution for the resize of the picture, for example 240x300")
parser.add_argument(
    "--face_crop",
    action="store_true",
    help="crop around the faces found on picture")
parser.add_argument("--out_path", help="path for the output file(s)")
parser.add_argument("--out_tag", help="tag for the output file(s)")
parser.add_argument(
    "--max_size", help="max size in bytes for the output file(s)")
parser.add_argument(
    "--ext",
    help="choose the extension of the output file(s) : .jpg, .gif, .png")


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
    if path.isfile():
    # Assume that the destination is a file
        process_pic(path, c["resolution"], c["out_tag"], c["out_path"],
                    c["face_crop"], c["nb_faces"], c["margin"], c["rotate"],
                    c["max_size"], c["extension"])
    elif path.isdir():
    print("Working on ", file_path)
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

    # crop around the face

    if im.nb_face > 0 and face_crop:

        for i in range(im.nb_face):
            print("Working on face", str(i + 1))
            face = copy.deepcopy(im)
            end_flag = False
            while not end_flag:
                face.face_crop(resolution, margin, whichface=i)
                if face.cut_error:
                    margin -= 0.05
                    if margin < 0:
                        return

                    print(
                        "The crop can't fit, now trying with a smaller margin of",
                        margin)
                    face.cut_error = 0
                else:
                    end_flag = True
            if skip_compression:
                face.save(out_path + out_tag + str(i) + "_" +
                          file_path.namebase + extension)
                return "Succes"
            face.resize(resolution)
            save(face, out_path, out_tag + str(i), max_size, file_path,
                 extension)
    else:
        if skip_compression:
            im.save(out_path + out_tag + str(i) + "_" + file_path.namebase +
                    extension)
            return "Succes"
        im.ratio_cut(resolution)
        im.resize(resolution)
        save(im, out_path, out_tag, max_size, file_path, extension)


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
    if path.isfile():
        # Assume that the destination is a file
        process_pic(path, c["resolution"], c["out_tag"], c["out_path"],
                    c["face_crop"], c["nb_faces"], c["margin"], c["rotate"],
                    c["max_size"], c["extension"])
    elif path.isdir():

        for file in path.files():
            if file.isfile():
                if file.ext in (".jpg", ".jepg", ".png", ".gif"):
                    process_pic(file, c["resolution"], c["out_tag"],
                                c["out_path"], c["face_crop"], c["nb_faces"],
                                c["margin"], c["rotate"], c["max_size"],
                                c["extension"], c["skip_compression"])
    else:
        print("This path doesn't exist")