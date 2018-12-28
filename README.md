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
python -m grpc_tools.protoc -I ./grpc --python_out=./grpc --grpc_python_out=./grpc grpc/find-faces.proto
```

### Test GRPC

Use npm `grpcc`.

```bash
grpcc -p grpc/insult-jmk.proto -a localhost:50051 -i
```

Then, in the REPL

```javascript
client.getInsult({picture: {path: "./some/path/random"}, printReply)
```