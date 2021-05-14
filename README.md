# mti-lab
Building a small lab for the sysadmin course at mti.cl

The main idea is to deploy the django app from a monolithic structure into a semi scalable one, 
going through the pain points of these process

## Contanerized-DB with OSM
* Make sure the osmdb folder exists and run the initial container
* Image must use a version of Debian that has osm2pgsql > 0.96
* Mount the volumes for data, the pbf file(s) and the carto git
´´´
podman run --rm -d --name osm-db -e POSTGRES_PASSWORD=mti2o20_db! -v $(pwd)/osmdb/:/var/lib/postgresql/data/:Z -v $(pwd)/chile-latest.osm.pbf:/data.osm.pbf:Z -v $(pwd)/openstreetmap-carto/:/carto:Z -p 5433:5432 postgis/postgis:13-master
´´´

* Connect to the database
´´´
psql -h 127.0.0.1 -U postgres -p 5433
create database gis;
create user gis superuser;
alter user gis with password '202o_mt1ñ';
grant ALL on DATABASE gis to gis;
\c gis
create extension hstore;
´´´

* Access the container, install osm2pgsql, load the data, no need to edit postgres.conf as it comes ready with the ideal setup
´´´
podman exec -ti osm-db bash
apt update -y
apt install -y osm2pgsql vim
osm2pgsql -G -d gis --hstore -U postgres -c -C20480 --style /carto/openstreetmap-carto.style --tag-transform-script /carto/openstreetmap-carto.lua /data.osm.pbf
su - postgres; cd carto; psql -d gis -f /carto/indexes.sql
´´´

* Grant all permission on tables and sequences to gis
´´´
psql -h 127.0.0.1 -U postgres -p 5433 -d gis
grant ALL on SCHEMA public to gis ;
´´´

* Create a local folder to store tiles
´´´
mkdir -p $(pwd)/tiles/
´´´

* After that, run normally as
´´´
podman run --rm -d --name osm-db -v $(pwd)/osmdb/:/var/lib/postgresql/data/:Z -p 5433:5432 postgis/postgis:13-master
´´´

## OSM Logic and View: Mapnik, Renderd and Apache
* Use host ip
´´´
podman build -t mti/mod_tile --build-arg theremotedb="192.168.0.15" --build-arg thepass="202o_mt1ñ" -f Dockerfile
podman run -ti --rm --name renderd-httpd-osm -v $(pwd)/tiles/:/var/cache/renderd/tiles:Z -p 8080:8080 mti/mod_tile
´´´

## Django Setup (Optional)
* Set DJANGO_SECRET_KEY to anything random-ish
´´´
export DJANGO_SECRET_KEY=kljsd76ASD_
export GIS_PWORD=202o_mt1ñ
´´´

* Install
´´´
dnf install -y python3-django python3-psycopg2
´´´
