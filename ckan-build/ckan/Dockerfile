# See CKAN docs on installation from Docker Compose on usage
FROM ubuntu:focal-20210119
MAINTAINER Open Knowledge

# Set timezone
ENV TZ=UTC
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

# Setting the locale
ENV LC_ALL=en_US.UTF-8       
RUN apt-get update
RUN apt-get install --no-install-recommends -y locales
RUN sed -i "/$LC_ALL/s/^# //g" /etc/locale.gen
RUN dpkg-reconfigure --frontend=noninteractive locales 
RUN update-locale LANG=${LC_ALL}

# Install required system packages
RUN apt-get -q -y update \
    && DEBIAN_FRONTEND=noninteractive apt-get -q -y upgrade \
    && apt-get -q -y install \
        python3.8 \
        python3-dev \
        python3-pip \
        python3-venv \
        python3-wheel \
        libpq-dev \
        libxml2-dev \
        libxslt-dev \
        libproj-dev \
        libgeos-dev \
        libspatialindex-dev \
        libudunits2-dev \
        libssl-dev \
        libgdal-dev \
        libffi-dev \
        postgresql-client \
        build-essential \
        git-core \
        vim \
        wget \
        curl \
        apt-utils \
        apt-transport-https \
        debconf-utils \
        gcc \
        build-essential \
        g++ \
        unixodbc \
        unixodbc-dev \
        xmlsec1 \
        uwsgi \
    && apt-get -q clean \
    && rm -rf /var/lib/apt/lists/*

RUN curl https://packages.microsoft.com/keys/microsoft.asc | apt-key add -
RUN curl https://packages.microsoft.com/config/ubuntu/19.04/prod.list > /etc/apt/sources.list.d/mssql-release.list

RUN apt-get -y update \
    && ACCEPT_EULA=Y apt-get install -y msodbcsql17

# Define environment variables
ENV CKAN_HOME /usr/lib/ckan
ENV CKAN_VENV $CKAN_HOME/venv
ENV CKAN_CONFIG /etc/ckan
ENV CKAN_STORAGE_PATH=/var/lib/ckan_storage
ENV CKAN_INI /etc/ckan/production.ini

# Build-time variables specified by docker-compose.yml / .env
ARG CKAN_SITE_URL

# Create ckan user
RUN useradd -r -u 900 -m -c "ckan" -d $CKAN_HOME -s /bin/false ckan

# Setup virtual environment for CKAN
RUN mkdir -p $CKAN_VENV $CKAN_CONFIG $CKAN_STORAGE_PATH && \
    python3 -m venv $CKAN_VENV && \
    ln -s $CKAN_VENV/bin/pip3 /usr/local/bin/ckan-pip3 &&\
    ln -s $CKAN_VENV/bin/ckan /usr/local/bin/ckan

# Virtual environment binaries/scripts to be used first
ENV PATH=${CKAN_VENV}/bin:${PATH}  

# Setup CKAN
WORKDIR $CKAN_VENV/src/
RUN git clone https://github.com/ckan/ckan.git
WORKDIR $CKAN_VENV/src/ckan
RUN git reset --hard 
RUN git checkout master
WORKDIR $CKAN_VENV/src/
RUN ckan-pip3 install -U pip && \
    ckan-pip3 install --upgrade --no-cache-dir -r $CKAN_VENV/src/ckan/requirement-setuptools.txt && \
    ckan-pip3 install zope.interface>=4.3.2 && \
    sed -i "/$zope.interface==4.3.2/d" $CKAN_VENV/src/ckan/requirements.txt && \
    ckan-pip3 install --upgrade --no-cache-dir -r $CKAN_VENV/src/ckan/requirements.txt && \
    ckan-pip3 install -e $CKAN_VENV/src/ckan/ && \
    ckan generate config $CKAN_CONFIG/production.ini && \
    ckan-pip3 install pyopenssl --upgrade && \
    ln -s $CKAN_VENV/src/ckan/ckan/config/who.ini $CKAN_CONFIG/who.ini && \
    cp -v $CKAN_VENV/src/ckan/contrib/docker/ckan-entrypoint.sh /ckan-entrypoint.sh && \
    chmod +x /ckan-entrypoint.sh && \
    chown -R ckan:ckan $CKAN_HOME $CKAN_VENV $CKAN_CONFIG $CKAN_STORAGE_PATH

USER ckan
EXPOSE 5000

CMD ["ckan","-c","/etc/ckan/production.ini", "run", "--host", "0.0.0.0"]
