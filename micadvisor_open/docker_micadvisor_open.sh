docker run \
    --volume=/:/rootfs:ro \
    --volume=/var/run:/var/run:rw \
    --volume=/sys:/sys:ro \
    --volume=/home/dingtong/open-falcon/micadvisor_open/log/cadvisor/:/home/work/uploadCadviosrData/log \
    --volume=/home/data/docker/:/var/lib/docker:ro \
    --volume=/home/data/docker/containers:/home/docker/containers:ro \
    --publish=18080:18080 \
    --env Interval=60 \
    --detach=true \
    --name=micadvisor \
    --net=host \
    --restart=always \
    micadvisor:latest

