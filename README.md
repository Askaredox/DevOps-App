# DevOps App

Steps to make a DevOps Application and Automation

# Docker

We'll use docker to test in a local environment, so we need to install the tools to run [Docker](https://www.docker.com/) and [Docker-Compose](https://docs.docker.com/compose/).

## Step 1 - Installing docker

First, update your existing list of packages:

```shell
sudo apt update
```

Install the prerequisite packages

```shell
sudo apt install apt-transport-https ca-certificates curl software-properties-common
```

Then add the GPG key for the official Docker repository to your system:

```shell
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -
```

Add the Docker repo to the APT source:

```shell
sudo add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu focal stable"
```

Install Docker

```shell
sudo apt install docker-ce
```

Docker should now be installed, the daemon started, and the process enabled to start on boot. Check that it’s running:

```shell
sudo systemctl status docker
```

The output should be similar to the following, showing that the service is active and running:

```shell
● docker.service - Docker Application Container Engine
     Loaded: loaded (/lib/systemd/system/docker.service; enabled; vendor preset: enabled)
     Active: active (running) since Sun 2022-04-24 03:48:57 CST; 8h ago
TriggeredBy: ● docker.socket
       Docs: https://docs.docker.com
   Main PID: 1582 (dockerd)
      Tasks: 34
     Memory: 158.0M
     CGroup: /system.slice/docker.service
```

## Step 2 - Use docker without sudo

If you want to avoid typing sudo whenever you run the `docker` command, add your username to the docker group:

```shell
sudo usermod -aG docker ${USER}
```

To apply the new group membership, log out of the server and back in, or type the following:

```shell
su - ${USER}
```

or restart the pc with:

```shell
sudo reboot now
```

## Step 3 - Install docker-compose

We can check the latest version of Docker Compose in its official [Github repository](https://github.com/docker/compose) and check the [version page](https://github.com/docker/compose/releases). At the time of this writing, the latest stable version is [2.4.1](https://github.com/docker/compose/releases/tag/v2.4.1).

The following command will download the version 2.4.1:

```shell
sudo curl -L "https://github.com/docker/compose/releases/download/v2.4.1/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
```

Next, we will set the correct permissions to make the command `docker-compose` executable:

```shell
sudo chmod +x /usr/local/bin/docker-compose
```

To verify that the installation was successful, you can run:

```shell
docker-compose --version
```

You'll see an output like this: 

```shell
Docker Compose version v2.4.1
```

# Coding

Let's do some code to test docker and how will be deployed

## Step 1 - Install virtualenv (Virtual Environment for Python3)

*NOTE: Skip this step if you have already installed pip3 and virtualenv*

Install pip: 

```shell
sudo apt-get install python3-pip
```

Then install virtualenv using pip3:

```shell
sudo pip3 install virtualenv 
```

## Step 2 - Virtual environment creation

Inside the `python-app` folder of this repo is a small app for a REST API, so first we need to make a virtualenv to encapsulate the libraries from the global python environment.

It's important that is in a separate folder and not in the root to separate from the rest of the project containers when we do a docker-compose orchestration. Go to the `python-app` folder or create a new one:

```shell
cd python
```

Create a virtual environment:

```shell
python3 -m virtualenv venv
```

A new folder should have been created called `venv`

First we need to activate the virtual environment:

```shell
source venv/bin/activate
```

## Step 3 - Flask app and requirements.txt

Then let's make some code for a Flask app, in the file `app.py` is a small code to run a Rest api using Flask. 

We need to install the necessary libraries to correcly run the App:

```shell
pip install flask flask-cors
```

If everything is ok, we can run the app locally using python:

```shell
python app.py
```

You should see and output like this:

```shell
 * Serving Flask app 'app' (lazy loading)
 * Environment: production
   WARNING: This is a development server. Do not use it in a production deployment.
   Use a production WSGI server instead.
 * Debug mode: off
 * Running on all addresses (0.0.0.0)
   WARNING: This is a development server. Do not use it in a production deployment.
 * Running on http://127.0.0.1:5000
 * Running on http://192.168.1.5:5000 (Press CTRL+C to quit)
```

Let's try in browser:

![Web test](./images/01_web.png)

Then we need to extract the requirements.txt to install them automatically in the Docker-compose's container. Close the app pressing CTRL+C to quit, then:

```shell
pip freeze > requirements.txt
```

A file should have been created called `requirements.txt` with all the required libraries.

## Step 4 - Docker preparations

Let's create a Docker file to make an image of the python app. You can see a [Dockerfile](./python-app/Dockerfile) in the `python-app` folder with comments explaining each line.

```Dockerfile
# ./python-app/Dockerfile
FROM python:3.8 
ADD . /code
WORKDIR /code
RUN pip install -r requirements.txt
CMD python app.py
```

*NOTE: It's important that the file is called `Dockerfile` exactly.*

Then create docker-compose file **in the ROOT of the project**. You can see a [docker-compose file](./docker-compose.yaml) in the root folder with comments explaining each line.

```docker
services: 
  flask-app:
    build: python-app/. # name of the folder
    container_name: flask-app # name of the container
    ports:
      - "5000:5000" # host port : container port
    volumes:
      - .:/flask/code # save data in a volume
    networks: 
      app_net:
        ipv4_address: 172.19.0.2 # ip address of the container to communicate from other containers
```

*NOTE: It's important that the file is called `docker-compose.yaml` exactly*

## Step 5 - local tests

Let's test the docker compose to run the image of python using this command in the root of the folder

```shell
docker-compose up -d --build
```

- **docker-compose**: the docker compose CLI.
- **up**: run the projects
- **-d**: make the containers run as a background process
- **--build**: build the images using docker

The app should be running as a background process. Let's see in the browser:

![Web test](./images/01_web.png)

You can also see if the image is running with the command:

```shell
docker ps
```

You should see an output like this to see the data of the running containers:

```shell
CONTAINER ID   IMAGE                 COMMAND                  CREATED         STATUS         PORTS                                       NAMES
38bc6b1c4728   devopsapp_flask-app   "/bin/sh -c 'python …"   4 minutes ago   Up 4 minutes   0.0.0.0:5000->5000/tcp, :::5000->5000/tcp   flask-app
```

We can turn off the docker containers using this command:

```shell
docker-compose down
```