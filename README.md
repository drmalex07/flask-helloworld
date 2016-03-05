## README

A helloworld application on Flask

### Quickstart

Install locally (for development):

    pip install -r requirements.txt
    python setup.py develop

Copy `config.ini.example` and edit to your needs:

    cp config.ini.example config.ini
    vim config.ini
    ...

Setup `repoze.who` to authenticate against a plain htpasswd-style file.
Create such a file (passwords digested using the rather insecure `crypt` algorithm):

    htpasswd -d -c htpasswd tester

Run Werkzeug server (for development):

    ./run-wsgi.py

### Deploy on containers

This is an example deployment on docker containers. 

The deployment is driven by a `Vagrantfile`, and can be locally configured via `deploy.yml`.

Install Vagrant prerequisites:

    vagrant plugin install vagrant-triggers

#### Setup

Build needed images, setup all containers:

    vagrant up

#### Initialize databases

Initialize database (if needed, i.e. if an empty database file is specified at `deploy.yml`):

    vagrant docker-run app -- paster init-db -v --name main-app

The above is the equivalent of directly running an one-off container based on our `app` image:

    docker run -it --rm --volumes-from helloworld-database local/helloworld:0.1 paster init-db -v --name main-app

#### Teardown

Destroy containers (note that built images are kept):

    vagrant destroy -f

