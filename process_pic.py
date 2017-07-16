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


def load_json_config(path):
    """
    Import a config file written in json
    """
    import json
    return json.loads(Path(path).text())


def process_pic(file_path, nb_faces=1, face_crop=False, margin=0.4):

    # check if the format is supported
    if not (file_path.ext in (".jpg", ".jpeg", ".png", ".gif")):
        print("The type of", filepath, "isn't supported.")
        return

    # create the Picture instance
    im = Picture(file_path)
    try:
        im.open()
    except OSError:
        return

    im.show()


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
    config.update(vars(args))
    c = config  # refactoring
    path = Path(c["path"])
    # Assume that the destination is a file

    file_path = path
    process_pic(file_path)