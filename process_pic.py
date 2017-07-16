from pic import Picture
from path import Path
import argparse, json
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


def process(dir_path, nb_faces=1, margin=0.4):
    dir = Path(dir_path)
    print(dir)


if __name__ == '__main__':
    args = parser.parse_args()
    print(args)
