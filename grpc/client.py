from logzero import logger
import grpc
import time

import find_faces_pb2
import find_faces_pb2_grpc


with grpc.insecure_channel('localhost:50051') as channel:
    stub = find_faces_pb2_grpc.FindFacesStub(channel)

    picture = find_faces_pb2.Picture(path="")
    input = find_faces_pb2.FindFacesRequest(picture=picture)

    faces = stub.FindFaces(input)

    logger.info(faces)