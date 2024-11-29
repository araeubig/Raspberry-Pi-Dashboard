#!/bin/bash

echo "Deleting existing dashboard folder."

rm -rf Raspberry-Pi-Dashboard

echo "Folder deleted and cloning git."

git clone https://github.com/araeubig/Raspberry-Pi-Dashboard

echo "Last dashbord version cloned. Peparing folder..."

(cd Raspberry-Pi-Dashboard; chmod +x *.sh)

sudo ./run.sh

