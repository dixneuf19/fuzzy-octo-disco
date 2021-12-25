# This is a sample Dockerfile you can modify to deploy your own app based on face_recognition

FROM python:3.8-slim-bullseye

RUN apt-get update && apt-get install -y \
    build-essential \
    cmake \
    gfortran \
    git \
    wget \
    curl \
    graphicsmagick \
    libgraphicsmagick1-dev \
    libatlas-base-dev \
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
RUN pip install -r requirements.txt

COPY fuzzyoctodisco/ fuzzyoctodisco/ 

EXPOSE 80

CMD ["uvicorn", "fuzzyoctodisco.main:app" , "--host", "0.0.0.0", "--port", "80"]

