#########################################
# Scrapy docker development environment #
# Based on Ubuntu Image                 #
#########################################

FROM ubuntu
MAINTAINER Nicholas Elia <nichelia.com>

# Last updated
ENV REFRESHED_AT 2017-6-17

RUN echo deb http://archive.ubuntu.com/ubuntu precise universe >> /etc/apt/sources.list
RUN apt-get update -y

# Install system dependencies
RUN apt-get install -y autoconf \
                       build-essential \
                       curl \
                       git \
                       vim-tiny

# Python dependencies
RUN apt-get install -y python \
                       python-dev \
                       python-distribute \
                       python-pip \
                       ipython

# Scrapy dependencies
RUN apt-get install -y libffi-dev \
                       libssl-dev \
                       libtool \
                       libxml2 \
                       libxml2-dev \
                       libxslt1.1 \
                       libxslt1-dev

# Pillow (Python Imaging Library) dependencies
RUN apt-get install -y libtiff5 \
                       libtiff5-dev \
                       libfreetype6-dev \
                       liblcms2-2 \
                       liblcms2-dev \
                       libwebp5 \
                       libwebp-dev \
                       zlib1g \
                       zlib1g-dev \
                       libjpeg8-dev \
                       tcl8.6-dev \
                       tk8.6-dev

# Add the dependencies to the container and install the python dependencies
ADD requirements.txt /tmp/requirements.txt
RUN pip install -r /tmp/requirements.txt && rm /tmp/requirements.txt

COPY scrapyd.conf /etc/scrapyd/
VOLUME /etc/scrapyd/ /var/lib/scrapyd/

# Expose web GUI
EXPOSE 6800

CMD [ "scrapyd", "--pidfile=" ]