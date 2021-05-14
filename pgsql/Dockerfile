# Compile mod tile with its products from the git repo
FROM fedora:33 AS base
RUN dnf install -y git redhat-rpm-config iniparser-devel cairo-devel autoconf automake boost-devel freetype-devel gcc-c++ httpd httpd-devel libicu-devel libtool make mapnik-devel proj-devel unzip wget

RUN git clone https://github.com/openstreetmap/mod_tile.git && cd mod_tile && \
	./autogen.sh && ./configure && make -j4 && make install && make install-mod_tile
RUN mkdir -p leaflet && cd leaflet && wget http://cdn.leafletjs.com/leaflet/v1.7.1/leaflet.zip && unzip leaflet.zip

# Deploy renderd and apache
FROM fedora:33
RUN dnf install -y httpd mapnik python3-mapnik
# renderd binaries
COPY --from=base /mod_tile/render* /usr/local/bin/
# mod_tile Apache module
COPY --from=base /usr/lib64/httpd/modules/mod_tile.so /usr/lib64/httpd/modules/
# Renderd conf
COPY --from=base /mod_tile/examples/config/renderd/renderd.conf.dist /etc/renderd.conf
# Mod tile apache conf
COPY --from=base /mod_tile/examples/config/apache2/renderd.conf.dist /etc/httpd/conf.d/mod_tile.conf
#Mapnik style
#COPY --from=base /mod_tile/examples/example-map/mapnik.xml /var/www/html/
# Base page, needs editing
COPY --from=base /mod_tile/examples/example-map/index.html /var/www/html/
# Leaflet css, js and images
COPY --from=base /leaflet/leaflet.css /var/www/html/
COPY --from=base /leaflet/* /var/www/html/

# Update configs
RUN sed -i 's/lib\/mapnik\/3.0/lib64\/mapnik/g' /etc/renderd.conf && \
	sed -i 's/example-map\/mapnik.xml/html\/mapnik.xml/g' /etc/renderd.conf && \
	chmod 755 /usr/lib64/httpd/modules/mod_tile.so && \
	curl https://raw.githubusercontent.com/LeoXDXp/mti-lab/main/pgsql/osm-vhost.conf -o /etc/httpd/conf.d/osm-vhost.conf && \
	curl https://raw.githubusercontent.com/LeoXDXp/mti-lab/main/pgsql/mapnik.xml -o /var/www/html/mapnik.xml && \
	sed -i 's/nothereobviously//g' /var/www/html/mapnik.xml && \
	sed -i 's/awsremotehost//g' /var/www/html/mapnik.xml
RUN 
#RUN useradd -U renderd
#USER renderd

CMD (httpd &) && renderd -f
