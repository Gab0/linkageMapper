FROM python:3.7.3-alpine

ENV LANG C.UTF-8
RUN echo "http://dl-cdn.alpinelinux.org/alpine/latest-stable/main" > /etc/apk/repositories
RUN echo "http://dl-cdn.alpinelinux.org/alpine/latest-stable/community" >> /etc/apk/repositories
RUN echo "http://dl-8.alpinelinux.org/alpine/edge/community" >> /etc/apk/repositories
RUN apk add --no-cache --allow-untrusted --repository http://dl-3.alpinelinux.org/alpine/edge/testing hdf5 hdf5-dev


RUN apk add --no-cache \
    xauth \
    xvfb \
    xvfb-run gcc gfortran build-base wget freetype-dev libpng-dev openblas-dev glib cairo cairo-dev \
    jpeg-dev zlib-dev 

RUN apk add --no-cache gobject-introspection-dev

RUN ls .
COPY . /app
RUN pip install --no-binary :all: ./app

