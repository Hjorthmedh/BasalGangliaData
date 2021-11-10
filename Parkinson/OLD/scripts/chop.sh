#!/bin/bash
i=0
name=$(basename $1 .swc)
chop.py $1 -o $name-$(printf '%03d' $((i+1))).swc
for i in $(seq 1 50); do chop.py $name-$(printf '%03d' $i).swc -o $name-$(printf '%03d' $((i+1))).swc; i=$((i+1)); done
