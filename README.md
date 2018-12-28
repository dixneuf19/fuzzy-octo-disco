# fuzzy-octo-disco

Small project of face recognition and image manipulation in Python using face_recognition and Pillow library.

Try it with

```bash
python example.py
```

## Choice of architecture

Originally, the *Picture* class needed to use a file path to open the file.

First, I thougth about sending the pictures through *GRPC* as bytes. But GRPC isn't made for large transfer, and I would have to change the class.

Therefore, I just send the path of the file and this *find-faces* service get the image how he can. On Kubernetes, this means I'll need a *shared volume*.

## Test

Use the `pytest` library. Just run

```bash
pytest
```

Add the `-s` arg to display print.

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
grpcc -p find_faces/grpc_services/find_faces.proto -a localhost:50051 -i
```

Then, in the REPL

```javascript
client.findFaces({picture: {path: "./pictures/lena.png"}}, pr)
```