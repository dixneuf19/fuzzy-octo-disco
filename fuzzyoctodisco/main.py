import os

from loguru import logger
from path import Path

from fuzzyoctodisco.pic import Picture

FACE_CROP_MARGIN = float(os.environ.get("FACE_CROP_MARGIN", default=0))


def make_save_path(original_path, index=0):
    original_path = Path(original_path)
    out_name = original_path.stem + "_out_%d" % index + original_path.ext
    full_path = original_path.dirname() / out_name
    return full_path.abspath()


def find_faces(picture, nb_faces=2, rotate=True):
    picture.find_faces()

    # if no faces found at all
    if len(picture.face_location) == 0:
        logger.info("No faces found")

        # let's try to rotate the picture
        if rotate:
            logger.info("Try to rotate the picture")
            i = 0
            while i < 3 and len(picture.face_location) == 0:
                picture.rotate(picture.ROTATE_90)
                picture.find_faces()
                i += 1

            # No faces found
            if len(picture.face_location) == 0:
                logger.info("Tried all rotations, but no faces found.")
                return 0

        #  Expecting only one_face, found more
    if nb_faces == 1 != len(picture.face_location):
        logger.info(
            "Found %d faces, expecting only one face." % len(picture.face_location)
        )
        return 0

    return len(picture.face_location)


from fastapi import FastAPI

app = FastAPI()


def error_response(error_code: str, error_msg: str):
    logger.warning(error_msg)
    return {"status": error_code, "message": error_msg}


@app.get("/faces")
def faces(pic_path: str):

    picture_path = Path(pic_path)

    # TODO add protection against attack with arbitrary path

    if not (picture_path.exists()):
        return error_response(
            "INVALID_PATH_ERROR", f"The path '{picture_path}' doesnt exists"
        )

    if not (picture_path.ext.lower() in (".jpg", ".jpeg", ".png", ".gif")):
        return error_response(
            "INVALID_FILE_EXTENSION_ERROR",
            f"The type of {picture_path} isn't supported",
        )

    # Finally we are good to go
    picture = Picture(picture_path.abspath())
    try:
        picture.open()
    except OSError:
        return error_response(
            "OPEN_FILE_ERROR", f"Error when opening the file {picture_path.abspath()}"
        )

    try:
        picture.img2raw()
        find_faces(picture)
    except Exception as error:
        logger.debug(error)
        return error_response(
            "IMAGE_PROCESSING_ERROR", "Error when searching the faces"
        )

    if len(picture.face_location) == 0:
        logger.info("No face found on this picture")
        return {"status": "NO_FACE_FOUND", "message": "No face found on this picture"}

    logger.info(f"Found {len(picture.face_location)} face(s).")
    faces_paths = []
    for i in range(len(picture.face_location)):
        try:
            face = picture.clone()
            face.face_crop(margin=FACE_CROP_MARGIN, whichface=i)
            out_path = make_save_path(pic_path, index=i)
            face.save(out_path)
            faces_paths.append(out_path)
        except Exception as error:
            logger.debug(error)
            logger.warn("failed to clone, crop or save face %d" % i)
            pass

    if len(faces_paths) == 0:
        return error_response("FAILED_ALL_FACES", "Failed to handle ALL faces")

    faces_pictures = [faces_paths[i] for i in range(len(faces_paths))]
    return {
        "status": "SUCCESS",
        "nbFaces": len(faces_pictures),
        "paths": faces_pictures,
    }
