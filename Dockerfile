FROM ubuntu:22.04

EXPOSE 5000

RUN apt-get update
RUN apt-get dist-upgrade -y
RUN apt-get install software-properties-common -y 
RUN add-apt-repository ppa:deadsnakes/ppa
RUN apt-get install python3.10 -y

RUN apt-get update
RUN apt-get install python3-pip -y

RUN apt-get update
RUN apt-get install -y libgl1-mesa-glx -y

WORKDIR /app
COPY . /app

RUN python3.11 -m pip install --upgrade pip; pip install -r requirements.txt

# CMD ["gunicorn", "wsgi:app", "-b", "0.0.0.0:5000"]

CMD ["python3", "app.py"]