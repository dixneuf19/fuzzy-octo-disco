# This is a sample Dockerfile you can modify to deploy your own app based on face_recognition

FROM ghcr.io/dixneuf19/docker-python-face-recognition:main@sha256:0672f1af5e661c30884adebfec9db8cffebdbe6767dd9cb43959e12d4f2b69d2

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY fuzzyoctodisco/ fuzzyoctodisco/ 

EXPOSE 80

CMD ["uvicorn", "fuzzyoctodisco.main:app" , "--host", "0.0.0.0", "--port", "80"]

