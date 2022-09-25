#!/bin/bash
#
# packager.io postinstall script
#
PATH=/opt/inventree/env/bin:/opt/inventree/:/sbin:/bin:/usr/sbin:/usr/bin:

cd ${APP_HOME}
python3 -m venv env

# default config
export INVENTREE_MEDIA_ROOT=/opt/inventree/data/media
export INVENTREE_STATIC_ROOT=/opt/inventree/data/static
export INVENTREE_PLUGIN_FILE=/opt/inventree/data/plugins.txt
export INVENTREE_CONFIG_FILE=/opt/inventree/data/config.yaml
export INVENTREE_DB_ENGINE=sqlite3
export INVENTREE_DB_NAME=database.sqlite3
export INVENTREE_PLUGINS_ENABLED=true

# import functions
. /opt/inventree/contrib/packager.io/functions

# exec postinstall
debug
detect_os
detect_docker
detect_initcmd

create_initscripts

stop_inventree
update_or_install
start_inventree

final_message
