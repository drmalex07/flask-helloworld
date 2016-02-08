## README

A helloworld application on Flask

### Setup with repoze.who middleware

In this example we setup repoze.who to authenticate against a plain htpasswd-style file.
Create such a file (passwords digested using the rather insecure `crypt` algorithm):

    htpasswd -d -c htpasswd tester


