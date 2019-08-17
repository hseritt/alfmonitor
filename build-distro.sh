#!/usr/bin/env bash

# Version to build distro:
VERSION="0.0.3"
DISTRO_DIR="distro"
DISTRO_DEST_DIR=$DISTRO_DIR/$VERSION

# Clear distro version directory
echo "Clearing $DISTRO_DEST_DIR ..."
rm -rf $DISTRO_DEST_DIR

echo "Creating distro directory ..."
mkdir $DISTRO_DEST_DIR

echo "Clearing all *.pyc files ..."
find . -name \*.pyc -delete

echo "Compiling Python files ..."
python -m compileall monitor.py engine.py

echo "Creating logs directory ..."
mkdir $DISTRO_DEST_DIR/logs

echo "Creating scripts directory ..."
mkdir $DISTRO_DEST_DIR/scripts

echo "Distributing compiled modules ..."
cp __pycache__/engine.cpython-36.pyc $DISTRO_DEST_DIR/scripts/engine.pyc
cp __pycache__/monitor.cpython-36.pyc $DISTRO_DEST_DIR/scripts/monitor.pyc

echo "Generating secret_key ..."
python django_genkey.py

# Copy essential directories
# alfmonitor project dir
echo "Copying directories ..."
cp -rf alfmonitor $DISTRO_DEST_DIR/.
cp -f alfmonitor/settings-dist.py $DISTRO_DEST_DIR/alfmonitor/settings.py
rm -rf $DISTRO_DEST_DIR/alfmonitor/settings-dist.py

# agents app
cp -rf agents $DISTRO_DEST_DIR/.

# console app
cp -rf console $DISTRO_DEST_DIR/.

# licenses
cp -rf licenses $DISTRO_DEST_DIR/.

echo "Copying setup scripts ..."
# scripts
cp scripts/add_agents.py $DISTRO_DEST_DIR/scripts/.
cp scripts/add_groups.py $DISTRO_DEST_DIR/scripts/.
cp scripts/modadminpwd.py $DISTRO_DEST_DIR/scripts/.
cp scripts/updatedb.py $DISTRO_DEST_DIR/scripts/.

# static
echo "Copying static files ..."
cp -rf static $DISTRO_DEST_DIR/.

# Copy scripts
echo "Copying scripts ..."
cp alfmonitor.sh $DISTRO_DEST_DIR/scripts/.
cp manage.py $DISTRO_DEST_DIR/scripts/.
cp starthttp.sh $DISTRO_DEST_DIR/scripts/.
cp requirements.txt $DISTRO_DEST_DIR/.
cp dist-setup.sh $DISTRO_DEST_DIR/setup.sh

cp README.txt $DISTRO_DEST_DIR/.

cd $DISTRO_DIR
tar czf alfmonitor-$VERSION.tgz $VERSION
mv alfmonitor-$VERSION.tgz ../versions/$VERSION/.
cd ..

echo "Creating source distro ..."

echo "Done."
