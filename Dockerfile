# The first instruction is what image we want to base our container on
# We Use an official Python runtime as a parent image
FROM python:3.8.10

# The enviroment variable ensures that the python output is set straight
# to the terminal with out buffering it first
ENV PYTHONUNBUFFERED 1

# create root directory for our project in the container
RUN mkdir /rest-api-scraper

# Set the working directory to /rest-api-scraper
WORKDIR /rest-api-scraper

# Copy the current directory contents into the container at /rest-api-scraper
ADD . /rest-api-scraper/

# Install any needed packages specified in requirements.txt
RUN pip install -r requirements.txt

RUN python backend/manage.py makemigrations && python backend/manage.py migrate
CMD python backend/manage.py runserver 0.0.0.0:8000