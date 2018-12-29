from concurrent import futures
from logzero import logger
from path import Path
import grpc
import time


from find_faces.grpc_service import find_faces_pb2
from find_faces.grpc_service import find_faces_pb2_grpc
from find_faces.pic import Picture

_ONE_DAY_IN_SECONDS = 60 * 60 * 24

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
        logger.info("Found %d faces, expecting only one face." % len(picture.face_location))
        return 0

    return len(picture.face_location)


class FindFacesServicer(find_faces_pb2_grpc.FindFacesServicer):
    def FindFaces(self, request, context):
        logger.info("Received a request: \n%s" % request)

        if request.picture is None or request.picture.path == "":
            logger.warn("You need at least picture object with a path")
            return find_faces_pb2.FindFacesResponse(status="NO_PATH_ERROR")

        picture_path = Path(request.picture.path)

        if not(picture_path.exists()):
            logger.warn("The path '%s' doesnt exists." % picture_path)
            return find_faces_pb2.FindFacesResponse(status="INVALID_PATH_ERROR")

        if not (picture_path.ext.lower() in (".jpg", ".jpeg", ".png", ".gif")):
            logger.warn("The type of %s isn't supported" % picture_path)
            return find_faces_pb2.FindFacesResponse(status="INVALID_FILE_EXTENSION_ERROR")
        
        # Finally we are good to go
        picture = Picture(picture_path.abspath())
        try:
            picture.open()
        except OSError:
            logger.warn("Error when opening the file %s" % picture_path.abspath())
            return find_faces_pb2.FindFacesResponse(status="OPEN_FILE_ERROR")
        
        try:
            picture.img2raw()
            find_faces(picture)
        except Exception as error:
            logger.debug(error)
            logger.warn("Error when searching the faces")
            return find_faces_pb2.FindFacesResponse(status="IMAGE_PROCESSING_ERROR")
        
        if len(picture.face_location) == 0:
            logger.info("No face found on this picture")
            return find_faces_pb2.FindFacesResponse(status="NO_FACE_FOUND")
        
        logger.info("Found %d face(s)." % len(picture.face_location))
        faces_paths = []
        for i in range(len(picture.face_location)):
            try:
                face = picture.clone()
                face.face_crop(whichface=i)
                out_path = make_save_path(request.picture.path, index=i)
                face.save(out_path)
                faces_paths.append(out_path)
            except Exception as error:
                logger.debug(error)
                logger.warn("failed to clone, crop or save face %d" % i)
                pass
        
        if len(faces_paths) == 0:
            logger.warn("Failed to handle ALL faces")
            return find_faces_pb2.FindFacesResponse(status="FAILED_ALL_FACES")
        
        faces_pictures = [find_faces_pb2.Picture(path=faces_paths[i], index=i) for i in range(len(faces_paths))]    
        return find_faces_pb2.FindFacesResponse(status="SUCCESS", nb_faces=len(faces_pictures), faces=faces_pictures)    


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    find_faces_pb2_grpc.add_FindFacesServicer_to_server(
        FindFacesServicer(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    logger.info("started the server")
    try:
        while True:
            time.sleep(_ONE_DAY_IN_SECONDS)
    except KeyboardInterrupt:
        server.stop(0)