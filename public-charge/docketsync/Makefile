COMMAND=bash

DATESTAMP:=`date --date="1 day ago" +'%Y-%m-%d'`

DOCKER_COMMAND=docker run -it --rm --init \
    --name docketsync-${TIMESTAMP} \
    --user=`id -u`:`id -g` \
    --volume ${CURDIR}:${WORKDIR} \
    --workdir ${WORKDIR} \
    --env REGULATIONS_GOV_API_KEY \
    ${DOCKER_IMAGE}

DOCKER_IMAGE=d4d/docketsync

DOCKETSYNC_ARGS=\
    --save-db comments_${DATESTAMP}.db \
    --save-csv comments_${DATESTAMP}.csv \
    --posted-date ${POSTED_DATE}

POSTED_DATE:=`date --date="1 day ago" +'%m/%d/%y'`

TIMESTAMP=`date +'%H%M%S'`

WORKDIR=/opt/docketsync


build:
	chmod 755 docketsync docketsync-run
	docker build -t ${DOCKER_IMAGE} .

shell:
	${DOCKER_COMMAND} ${COMMAND}

sync:
	${DOCKER_COMMAND} ./docketsync ${DOCKETSYNC_ARGS}
