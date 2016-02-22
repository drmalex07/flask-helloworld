FROM debian:8.2

RUN mkdir -p /var/opt/helloworld/data
ADD data/main.db /var/opt/helloworld/data/main.db
RUN chown www-data:www-data -v -R /var/opt/helloworld/data

CMD ["/bin/true"]

VOLUME /var/opt/helloworld/data/
