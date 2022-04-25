# Use the node image from Docker
FROM node:12

# create the folder app in the container
RUN mkdir /app

# move to the created container
WORKDIR /app

# copy the all files to the container's folder
COPY . /app

# install the requirements files
RUN npm i

# copy all to the file
CMD node app.js
