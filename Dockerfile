FROM python:3.11-slim-bullseye

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt
RUN python -m nltk.downloader punkt

COPY . .

EXPOSE 5000
CMD [ "gunicorn", "--bind=0.0.0.0:5000", "--workers=1", "--threads=4", "app:app"]
