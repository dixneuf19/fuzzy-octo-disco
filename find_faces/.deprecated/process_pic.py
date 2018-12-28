# -*- coding: utf-8 -*-
from find_faces.pic import Picture
from path import Path
from logzero import logger
import copy
import json


def load_json_config(path):
    """
    Import a config file written in json
    """
    return json.loads(Path(path).text())


def find_faces(im, nb_faces=2, rotate=True):
    im.find_face()

    # if no faces found at all
    if len(im.face_location) == 0:
        logger.info("No faces found")

        # let's try to rotate the picture
        if rotate:
            logger.info("Try to rotate the picture")
            i = 0
            while i < 3 and len(im.face_location) == 0:
                im.rotate(im.ROTATE_90)
                im.find_face()
                i += 1

            # No faces found
            if len(im.face_location) == 0:
                logger.info("Tried all rotations, but no faces found.")
                return 0

        #  Expecting only one_face, found more
    if nb_faces == 1 != len(im.face_location):
        logger.info("Found %d faces, expecting only one face." % len(im.face_location))
        return 0

    return len(im.face_location)


def save(im, out_path, out_tag, max_size, file_path, extension):
    out_path, out_tag = Path(out_path), Path(out_tag)
    out_path = out_path + out_tag + "_" + file_path.namebase + extension
    quality = 90
    im.save(out_path, quality=quality)
    while out_path.size > int(max_size) and quality >= 40:
        quality -= 5
        logger.info("The file is too heavy, trying to save with quality : %f" % quality)
        im.save(out_path, quality=quality)

    if out_path.size > int(max_size):
        logger.info("Can't manage to reduce the size under %d bytes." % max_size)
        out_path.remove()
    else:
        logger.info("The file is succesfully saved at %s" % out_path.abspath())


def process_pic_for_bot(
    file_path,
    resolution,
    out_tag,
    out_path="",
    face_crop=False,
    nb_faces=1,
    margin=0.4,
    rotate=True,
    max_size=10000,
    extension=".jpg",
    skip_compression=False,
):

    if not (file_path.ext.lower() in (".jpg", ".jpeg", ".png", ".gif")):
        logger.info("The type of %s isn't supported" % file_path)
        return
    logger.info("------------------------------------------------------------------")
    logger.info("Working on %s" % file_path)

    # create the Picture instance
    im = Picture(file_path)
    #  try to open it
    try:
        im.open()
    except OSError:
        return

    # find faces, exit if it doesn't respect the nb_faces argument
    if nb_faces >= 1:
        nb_faces_found = find_faces(im, nb_faces, rotate)

        if nb_faces_found == 0:
            return
        #  if everything went alright
        logger.info("Found %d face(s)." % len(im.face_location))

    #  crop around the face

    faces_result = []

    if len(im.face_location) > 0:

        for i in range(len(im.face_location)):

            logger.info("Working on face %d" % i + 1)

            face = copy.deepcopy(im)
            end_flag = False
            while not end_flag:
                face.face_crop(resolution, margin, whichface=i)
                if face.cut_error:
                    margin -= 0.05
                    if margin < 0:
                        return

                    logger.info(
                        "The crop can't fit, now trying with a smaller margin of %f"
                        % margin
                    )
                    face.cut_error = 0
                else:
                    end_flag = True
            face.save(
                out_path + out_tag + str(i) + "_" + file_path.namebase + extension
            )
            faces_result.append(
                out_path + out_tag + str(i) + "_" + file_path.namebase + extension
            )

    return faces_result


def process_pic(
    file_path,
    resolution,
    out_tag,
    out_path="",
    face_crop=False,
    nb_faces=1,
    margin=0.4,
    rotate=True,
    max_size=10000,
    extension=".jpg",
    skip_compression=False,
):

    # check if the format is supported
    if not (file_path.ext.lower() in (".jpg", ".jpeg", ".png", ".gif")):
        logger.info("The type of %s isn't supported" % file_path)
        return
    logger.info("------------------------------------------------------------------")
    logger.info("Working on %s" % file_path)
    # create the Picture instance
    im = Picture(file_path)
    #  try to open it
    try:
        im.open()
    except OSError:
        return

    # find faces, exit if it doesn't respect the nb_faces argument
    if nb_faces >= 1:
        nb_faces_found = find_faces(im, nb_faces, rotate)

        if nb_faces_found == 0:
            return
        #  if everything went alright
        logger.info("Found %d face(s)." % len(im.face_location))

    #  crop around the face

    if len(im.face_location) > 0 and face_crop:

        for i in range(len(im.face_location)):
            logger.info("Working on face %d" % i + 1)

            face = copy.deepcopy(im)
            end_flag = False
            while not end_flag:
                face.face_crop(resolution, margin, whichface=i)
                if face.cut_error:
                    margin -= 0.05
                    if margin < 0:
                        return

                    logger.info(
                        "The crop can't fit, now trying with a smaller margin of %f"
                        % margin
                    )
                    face.cut_error = 0
                else:
                    end_flag = True
            if skip_compression:
                face.save(
                    out_path + out_tag + str(i) + "_" + file_path.namebase + extension
                )
                return "Succes"
            face.resize(resolution)
            save(face, out_path, out_tag + str(i), max_size, file_path, extension)
    else:
        if skip_compression:
            im.save(out_path + out_tag + str(i) + "_" + file_path.namebase + extension)
            return "Succes"
        width, height = resolution
        im.ratio_cut(width, height, resolution)
        im.resize(resolution)
        save(im, out_path, out_tag, max_size, file_path, extension)


def run_bot(path):

    config = load_json_config("config.json")

    c = config  #  shorter name
    path = Path(path)
    if path.isfile():
        # Assume that the destination is a file
        return process_pic_for_bot(
            path,
            None,
            c["out_tag"],
            c["out_path"],
            c["face_crop"],
            c["nb_faces"],
            c["margin"],
            c["rotate"],
            c["max_size"],
            c["extension"],
        )
    elif path.isdir():

        for file in path.files():
            if file.isfile():
                if file.ext in (".jpg", ".jepg", ".png", ".gif"):
                    return process_pic(
                        file,
                        c["resolution"],
                        c["out_tag"],
                        c["out_path"],
                        c["face_crop"],
                        c["nb_faces"],
                        c["margin"],
                        c["rotate"],
                        c["max_size"],
                        c["extension"],
                        c["skip_compression"],
                    )
    else:
        logger.info("This path doesn't exist")
