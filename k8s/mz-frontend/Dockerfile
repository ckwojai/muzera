FROM python:3.9
RUN apt-get update && apt-get install -y \
  libsndfile-dev \
   ffmpeg \
#   git \
#   mercurial \
#   subversion \
  && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY app/requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY app .
CMD "gunicorn" "--bind" "0.0.0.0:5000" "wsgi:app"
# CMD ["python3", "app.py"