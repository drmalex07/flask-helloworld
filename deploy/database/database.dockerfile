# vim: set syntax=dockerfile:

FROM debian:8.2

ARG db_file=data/main.db

RUN mkdir -p /var/opt/helloworld/data
ADD ${db_file} /var/opt/helloworld/data/main.db
RUN chown www-data:www-data -v -R /var/opt/helloworld/data

ENV DATABASE_FILE=/var/opt/helloworld/data/main.db

CMD ["/bin/true"]

VOLUME /var/opt/helloworld/data/
