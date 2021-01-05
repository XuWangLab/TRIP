#!/bin/bash

cat url | while read line
do
	wget $line
done
