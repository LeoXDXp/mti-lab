# mti-lab
Building a small lab for the sysadmin course at mti.cl

The main idea is to deploy the django app from a monolithic structure into a semi scalable one, 
going through the pain points of these process

## Contanerized-DB with OSM
* Make sure the osmdb folder exists and run the initial container
´´´
podman run --rm -d --name osm-db -e POSTGRES_PASSWORD=mti2o20_db! -v $(pwd)/osmdb/:/var/lib/postgresql/data/:Z -v $(pwd)/chile-latest.osm.pbf:/data.osm.pbf:Z -p 5432:5432 postgis/postgis
´´´

* Connect to the database
´´´
psql -h 127.0.0.1 -U postgres -p 5433
create database gis;
create user gis superuser;
alter user gis with password '202o_mt1ñ';
grant ALL on DATABASE gis to gis ;
´´´

* Access the container, install osm2pgsql, load the data, edit postgres.conf for (performance)[https://www.linuxbabe.com/ubuntu/openstreetmap-tile-server-ubuntu-18-04-osm]
´´´
podman exec -ti osm-db bash
apt update -y
apt install -y osm2pgsql vim
osm2pgsql -d gis -U postgres -c -C20480 /data.osm.pbf
vim /var/lib/postgresql/data/postgresql.conf
´´´

* Grant all permission on tables and sequences to gis
´´´
psql -h 127.0.0.1 -U postgres -p 5433 -d gis
grant ALL on SCHEMA public to gis ;
´´´

## Django Setup
* Set DJANGO_SECRET_KEY to anything random-ish
´´´
export DJANGO_SECRET_KEY=kljsd76ASD_
export GIS_PWORD=202o_mt1ñ
´´´

* Install
´´´
dnf install -y python3-django python3-psycopg2
´´´
