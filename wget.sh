#!/bin/bash
SHELL_FOLDER=$(cd "$(dirname "$0")";pwd)
cat ${SHELL_FOLDER}/url | while read line
do
	wget $line --directory-prefix=${SHELL_FOLDER}
done
