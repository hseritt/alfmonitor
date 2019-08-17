#!/usr/bin/env bash

./build-distro.sh

# Version to build distro:
VERSION="0.0.3"
DISTRO_DIR="distro"
DISTRO_DEST_DIR=$DISTRO_DIR/$VERSION

cd $DISTRO_DEST_DIR
./setup.sh --noinput
./alfmonitor.sh start
