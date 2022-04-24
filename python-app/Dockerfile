
# Use the image of python version 3.8
FROM python:3.8 

# Add all the files in the folder to the /code folder inside the container
ADD . /code

# Go inside the container to prepare the installation and run
WORKDIR /code

# install the requirements.txt
RUN pip install -r requirements.txt

# run the app
CMD python app.py