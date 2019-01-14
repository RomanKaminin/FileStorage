FROM python:3.6-slim

# It`s setting for use superuser after start application.


# Install some necessary things.
RUN apt-get update
RUN apt-get install -y gettext libgettextpo-dev

# Install our requirements.
WORKDIR /root/src/
ADD ./requirements /root/src
ADD ./libs/django-filetransfers /root/src
RUN pip3 install -U pip
RUN pip3 install -Ur requirements
RUN pip install django-filetransfers
ADD . /root/src
