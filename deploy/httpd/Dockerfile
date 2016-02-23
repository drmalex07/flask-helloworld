FROM debian:8.2

RUN apt-get update && apt-get install -y \
  ca-certificates \
  python python-dev python-setuptools python-pip \
  apache2 libapache2-mod-wsgi

RUN apt-get clean
RUN rm -rf /tmp/* /var/tmp/*

ENV APACHE_RUN_USER=www-data
ENV APACHE_RUN_GROUP=www-data
ENV APACHE_PID_FILE=/var/run/apache2/apache2.pid
ENV APACHE_RUN_DIR=/var/run/apache2
ENV APACHE_LOCK_DIR=/var/lock/apache2
ENV APACHE_LOG_DIR=/var/log/apache2
ENV LANG=C

RUN a2enmod ssl

CMD ["/usr/sbin/apache2", "-DFOREGROUND", "-kstart"]

EXPOSE 80
EXPOSE 443

VOLUME /var/log/apache2
