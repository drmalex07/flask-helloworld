## README

A httpd-based docker image for the WSGI application. 

This image assumes that the source distribution of the Python package
is allready present at `dist/helloworld-{VERSION}.tar.gz`. 
If not, built with:

    python setup.py sdist
