from concurrent import futures
from logzero import logger
import grpc
import time

import find_faces_pb2
import find_faces_pb2_grpc

_ONE_DAY_IN_SECONDS = 60 * 60 * 24

class FindFacesServicer(find_faces_pb2_grpc.FindFacesServicer):
    def FindFaces(self, request, context):
        logger.info("Received a request: \n%s" % request)

        if request.picture is None or request.picture.path == "":
            logger.warn("You need at least picture object with a path")
            return find_faces_pb2.FindFacesResponse(status="NO_PATH_ERROR")

        
        return find_faces_pb2.FindFacesResponse()


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


if __name__ == '__main__':
    serve()