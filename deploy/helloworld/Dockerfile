FROM local/httpd:2.4-mod_wsgi

ARG server_name=helloworld.internal
ENV SERVER_NAME=${server_name}

ENV HELLOWORLD_VERSION=0.1
ENV HELLOWORLD_CONFIG_FILE=/etc/opt/helloworld/config.ini
ENV CONFIG_FILE=${HELLOWORLD_CONFIG_FILE}

RUN mkdir -p /etc/opt/helloworld /var/opt/helloworld /var/opt/helloworld/data
ADD dist/helloworld-${HELLOWORLD_VERSION}.tar.gz /opt/
RUN ln -s /opt/helloworld-${HELLOWORLD_VERSION} /opt/helloworld

WORKDIR /opt/helloworld
RUN pip install -r requirements.txt
RUN python setup.py install
RUN cp -rv -l /opt/helloworld/public /var/opt/helloworld/public

RUN chown -v root:www-data -R /var/opt/helloworld/public
RUN chown -v www-data:www-data -R /var/opt/helloworld/data/

ADD deploy/helloworld/config.ini /etc/opt/helloworld
RUN sed \
  -i 's/session.secret =\s*.*$/session.secret = '"$(head -c16 /dev/urandom| base64)"'/' \
  /etc/opt/helloworld/config.ini

ADD deploy/helloworld/vhost.conf /etc/apache2/sites-available/helloworld.conf
ADD deploy/helloworld/wsgi.py /opt/helloworld/wsgi.py
RUN a2ensite helloworld

VOLUME /var/opt/helloworld/data/main.db
