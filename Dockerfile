# This is a sample Dockerfile you can modify to deploy your own app based on face_recognition

FROM ghcr.io/dixneuf19/docker-python-face-recognition:main

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY fuzzyoctodisco/ fuzzyoctodisco/ 

EXPOSE 80

CMD ["uvicorn", "fuzzyoctodisco.main:app" , "--host", "0.0.0.0", "--port", "80"]

