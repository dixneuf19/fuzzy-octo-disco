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
    # Pretend that we load the following JSON file:
    return json.loads(Path(path).text())


def process_pic(path, nb_faces=1, face_crop=False, margin=0.4):
    file_path = Path(path)
    pass


def merge(dict_1, dict_2):
    """Merge two dictionaries.
    Values that evaluate to true take priority over falsy values.
    `dict_1` takes priority over `dict_2`.
    """
    return dict((str(key), dict_1.get(key) or dict_2.get(key))
                for key in set(dict_2) | set(dict_1))


if __name__ == '__main__':
    args = parser.parse_args()
    if args.json:
        config = load_json_config(args.json)
    else:
        config = {}
    # Shell options takes priority over json config
    config = merge(vars(args), config)
