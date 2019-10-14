# This is a sample Dockerfile you can modify to deploy your own app based on face_recognition

FROM python:3.6-slim-stretch

RUN apt-get -y update && apt-get install -y --fix-missing \
    build-essential \
    cmake \
    gfortran \
    git \
    wget \
    curl \
    graphicsmagick \
    libgraphicsmagick1-dev \
    libatlas-dev \
    libavcodec-dev \
    libavformat-dev \
    libgtk2.0-dev \
    libjpeg-dev \
    liblapack-dev \
    libswscale-dev \
    pkg-config \
    python3-dev \
    python3-numpy \
    software-properties-common \
    zip \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip3 install -r requirements.txt

# The rest of this file just runs an example script.

COPY main.py main.py
COPY find_faces/ find_faces/ 
COPY config.json config.json

CMD [ "python", "./main.py" ]
