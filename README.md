# fuzzy-octo-disco

[![Build Status](https://travis-ci.org/dixneuf19/fuzzy-octo-disco.svg?branch=master)](https://travis-ci.org/dixneuf19/fuzzy-octo-disco)

Small project of face recognition and image manipulation in Python using face_recognition and Pillow library.
It is now used in the [Dank Face Bot](https://github.com/dixneuf19/fuzzy-octo-disco) project, as a separate micro-service.
The main use of this project is to identify faces on picture, by rotating it, and then return croped pictures of this faces.

Try it with

```bash
python example.py
```

Don't forget to install dependecies in a Python *virtualenv* first !

```bash
pip install -r requirements.txt
```

See [my gist](https://gist.github.com/dixneuf19/a398c08f00aac24609c3cc44c29af1f0) for more details on how to setup *virtualenvwrapper* with zsh.

## Choice of architecture

These program need to communicate with other services, as dank-face-bot, which sends pictures, and expects some cropped faces back. But how can we transfer the pictures, an heavy load, between the services ?

Originally, the *Picture* class needed to use a file path to open the file.
First, I thougth about sending the pictures through *gRPC* as bytes. But gRPC isn't made for large transfer, and I would have to change the class.

Therefore, I just send the path of the file and this *find-faces* service get the image how he can. On Kubernetes, this means I'll need a *shared volume*. On docker-compose, I use a shared volume.

We use a NFS shared volume : <https://github.com/mappedinn/kubernetes-nfs-volume-on-gke>

It's deployed with the main [DFB repo](https://github.com/dixneuf19/dank-face-bot).

## Test

Use the `pytest` library. Just run

```bash
pytest
```

Add the `-s` arg to display print.

## Deploy

See the main [DFB repo](https://github.com/dixneuf19/dank-face-bot) for reminders about k8s, Travis and etc...

## GRPC

### Generate the proto

Install `grpcio` and `grpcio-tools` with `pip`. Then

```bash
python -m grpc_tools.protoc -I ./find_faces/grpc_service --python_out=./find_faces/grpc_service --grpc_python_out=./find_faces/grpc_service grpc/find-faces.proto
```

#### Fix path import issue for GRPC

There is an issue with the way `protoc` generate the pb files and `__init__.py`, which create a module.

@see <https://github.com/protocolbuffers/protobuf/issues/1491>

Anyway, a fix for now : 
In `find_faces/grpc_service/find_faces_pb2_grpc.py` change

```python
import find_faces_pb2 as find_faces__pb2
```

to

```python
from . import find_faces_pb2 as find_faces__pb2
```

This isn't a great solution however...

### Test GRPC

A small test file in `find_face/grpc_service/client.py`:

```bash
python -m find_faces.grpc_service.client
```

Use npm `grpcc`.

```bash
grpcc -p find_faces/grpc_service/find-faces.proto -a localhost:50051 -i
```

Then, in the REPL

```javascript
client.findFaces({picture: {path: "./pictures/lena.png"}}, pr)
```