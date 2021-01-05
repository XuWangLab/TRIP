#!/bin/bash
tail -n +2 *.txt | cut -f 7 | tr ";" "\t" | tee url.0 | cut -f 1 > url.1
cat url.0 | cut -s -f 2 > url.2
cat url.1 > url
cat url.2 >> url
rm url.1
rm url.2
rm url.0
