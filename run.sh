#/bin/bash

restart () {
	echo "🤟 Restarting!"
    docker-compose down
    docker-compose up -d
}

while getopts rb opts; do
   case ${opts} in
	  r) restart;;
	  b) docker-compose up --build;;
   esac
done
