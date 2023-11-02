FROM python:3.8-slim-buster

EXPOSE 5000

WORKDIR /usr/app/src

ADD requirements.txt ./

RUN python -m pip install -r requirements.txt

COPY api.py  bike_index.py gpt.py main.py ./

COPY manufacturers.csv ./

RUN mkdir ./logs

RUN touch ./logs/BikeIndexApp.log

CMD [ "python", "./main.py"]