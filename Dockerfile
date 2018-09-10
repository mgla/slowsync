from ubuntu:bionic

ARG RCLONE_DIR=rclone-v1.43.1-linux-amd64
ARG RCLONE_DOWNLOAD=https://downloads.rclone.org/v1.43.1/${RCLONE_DIR}.zip
RUN apt-get update
RUN apt-get install -y wget unzip
RUN wget -q ${RCLONE_DOWNLOAD} -O /tmp/rclone.zip
RUN unzip /tmp/rclone.zip -d /tmp/rclone_tmp
RUN cp /tmp/rclone_tmp/${RCLONE_DIR}/rclone /usr/bin/rclone
RUN chmod +x /usr/bin/rclone
