#-*- coding: utf-8 -*-
from find_faces.pic import Picture
from path import Path
import copy


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
        print("No faces found")

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
                print("Tried all rotations, but no faces found.")
                return 0

        # Expecting only one_face, found more
    if nb_faces == 1 != im.nb_face:
        print("Found", im.nb_face, "faces, expecting only one face.")
        return 0

    return im.nb_face


def save(im, out_path, out_tag, max_size, file_path, extension):
    out_path, out_tag = Path(out_path), Path(out_tag)
    out_path = out_path + out_tag + "_" + file_path.namebase + extension
    quality = 90
    im.save(out_path, quality=quality)
    while out_path.size > int(max_size) and quality >= 40:
        quality -= 5
        print("The file is too heavy, trying to save with quality :", quality)
        im.save(out_path, quality=quality)

    if out_path.size > int(max_size):
        print("Can't manage to reduce the size under", max_size, "bytes.")
        out_path.remove()
    else:
        print("The file is succesfully saved at", out_path.abspath())


def process_pic_for_bot(file_path,
                resolution,
                out_tag,
                out_path="",
                face_crop=False,
                nb_faces=1,
                margin=0.4,
                rotate=True,
                max_size=10000,
                extension=".jpg",
                skip_compression=False):

    if not (file_path.ext.lower() in (".jpg", ".jpeg", ".png", ".gif")):
        print("The type of", file_path, "isn't supported.")
        return
    print("------------------------------------------------------------------")
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

    faces_result = []

    if im.nb_face > 0:

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
            face.save(out_path + out_tag + str(i) + "_" +
                          file_path.namebase + extension)        
            faces_result.append(out_path + out_tag + str(i) + "_" +
                          file_path.namebase + extension)
    
    return faces_result

    

    

def process_pic(file_path,
                resolution,
                out_tag,
                out_path="",
                face_crop=False,
                nb_faces=1,
                margin=0.4,
                rotate=True,
                max_size=10000,
                extension=".jpg",
                skip_compression=False):

    # check if the format is supported
    if not (file_path.ext.lower() in (".jpg", ".jpeg", ".png", ".gif")):
        print("The type of", file_path, "isn't supported.")
        return
    print("------------------------------------------------------------------")
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


def run_bot(path):


    config = load_json_config('config.json')
    
        

    c = config  #  shorter name
    path = Path(path)
    if path.isfile():
        # Assume that the destination is a file
        return process_pic_for_bot(path, None, c["out_tag"], c["out_path"],
                    c["face_crop"], c["nb_faces"], c["margin"], c["rotate"],
                    c["max_size"], c["extension"])
    elif path.isdir():

        for file in path.files():
            if file.isfile():
                if file.ext in (".jpg", ".jepg", ".png", ".gif"):
                    return process_pic(file, c["resolution"], c["out_tag"],
                                c["out_path"], c["face_crop"], c["nb_faces"],
                                c["margin"], c["rotate"], c["max_size"],
                                c["extension"], c["skip_compression"])
    else:
        print("This path doesn't exist")
