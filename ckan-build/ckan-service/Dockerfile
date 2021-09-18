FROM ckanbase.azurecr.io/ckan-base-2.9.3:base

# Define environment variables
ENV CKAN_HOME /usr/lib/ckan
ENV CKAN_VENV $CKAN_HOME/venv
ENV CKAN_CONFIG /etc/ckan
ENV CKAN_STORAGE_PATH=/var/lib/ckan
ENV SRC_DIR=$CKAN_VENV/src
ENV PATH=${CKAN_VENV}/bin:${PATH}
ENV CKAN_INI=$CKAN_CONFIG/production.ini
ENV CKAN__PLUGINS="image_view text_view recline_view envvars scheming_datasets developerpage"


WORKDIR $CKAN_HOME
USER root
RUN chown -R ckan:ckan $CKAN_HOME $CKAN_VENV $CKAN_CONFIG $CKAN_STORAGE_PATH
COPY ckan-build/ckan-service/scripts ${CKAN_HOME}/scripts
COPY ckan-build/ckan-service/patches ${SRC_DIR}/patches
COPY src $SRC_DIR/extensions
RUN chown -R ckan:ckan $SRC_DIR
RUN chmod +x -R ${CKAN_HOME}/scripts

USER ckan
WORKDIR $CKAN_VENV/src/ckan 

# Apply patches (if any)
RUN for d in ${SRC_DIR}/patches/*; do \
        for f in `ls $d/*.patch | sort -g`; do \
			cd $SRC_DIR/`basename "$d"` && echo "$0: Applying patch $f to $SRC_DIR/`basename $d`"; patch -p1 < "$f" ; \
        done ; \
    done

WORKDIR $CKAN_HOME

# Generate CKAN Config
RUN ckan generate config $CKAN_CONFIG/production.ini

ENTRYPOINT [ ]
CMD ["/bin/sh", "scripts/start_ckan.sh"]