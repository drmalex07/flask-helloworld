# vim: set syntax=dockerfile: 

FROM local/httpd:2.4-mod_wsgi

ARG version
ARG server_name=helloworld.internal

ENV SERVER_NAME=${server_name}

# Note: The current config.ini expects a webserver-writable data directory
# at /var/opt/helloworld/data. So, we must take care to mount a data volume container 
# that will provide it!

ENV HELLOWORLD_VERSION=${version:-0.0.1}
ENV HELLOWORLD_CONFIG_FILE=/etc/opt/helloworld/config.ini
ENV CONFIG_FILE=${HELLOWORLD_CONFIG_FILE}

RUN mkdir -p /etc/opt/helloworld /var/opt/helloworld
ADD dist/helloworld-${HELLOWORLD_VERSION}.tar.gz /opt/
RUN ln -s /opt/helloworld-${HELLOWORLD_VERSION} /opt/helloworld

WORKDIR /opt/helloworld
RUN pip install -r requirements.txt && python setup.py install
RUN cp -rv -l /opt/helloworld/public /var/opt/helloworld/public

ADD deploy/app/wsgi.py /opt/helloworld/wsgi.py

RUN chown -v www-data:www-data -R /var/opt/helloworld

ADD deploy/app/config.ini /etc/opt/helloworld/config.ini

ADD deploy/app/vhost.conf /etc/apache2/sites-available/helloworld.conf
RUN a2ensite helloworld

