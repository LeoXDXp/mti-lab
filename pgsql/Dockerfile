FROM fedora AS base
RUN dnf install -y https://download.postgresql.org/pub/repos/yum/reporpms/F-32-x86_64/pgdg-fedora-repo-latest.noarch.rpm && \
	dnf install -y git postgresql11-server libpq-devel redhat-rpm-config bison flex && \
	dnf groupinstall -y "Development Tools"
RUN git clone https://github.com/apache/incubator-age.git && cd incubator-age && mkdir incubator-age && make

FROM fedora
RUN dnf update -y && dnf install -y https://download.postgresql.org/pub/repos/yum/reporpms/F-32-x86_64/pgdg-fedora-repo-latest.noarch.rpm && \
	dnf install -y postgresql11-server postgis postgis-utils bison flex
COPY --from=base /

# Run initdb only if /var/lib/pgsql/data/ is empty
RUN if [ ! -d "/var/lib/pgsql/data/" ]; then /usr/pgsql-11/bin/postgresql-11-setup initdb fi

# Enable the db service
RUN systemcl enable postgresql-11

# Expose the DB port
EXPOSE 5432

# If using SELinux, this boolean needs to be activated
# setsebool -P container_manage_cgroup 1

# If not using k8s, might want to manually declare the volumes 
#VOLUME  ["/etc/postgresql", "/var/log/postgresql", "/var/lib/postgresql"]

USER postgres
#CMD ["/usr/pgsql-11/bin/postgres", "-D", "/var/lib/pgsql/11/main", "-c", "config_file=/etc/postgresql/9.3/main/postgresql.conf"]
