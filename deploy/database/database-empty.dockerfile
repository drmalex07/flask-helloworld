# vim: set syntax=dockerfile:

FROM debian:8.2

RUN mkdir -p /var/opt/helloworld/data
RUN touch /var/opt/helloworld/data/main.db
RUN chown www-data:www-data -v -R /var/opt/helloworld/data

ENV DATABASE_FILE=/var/opt/helloworld/data/main.db

CMD ["/bin/true"]

VOLUME /var/opt/helloworld/data/
