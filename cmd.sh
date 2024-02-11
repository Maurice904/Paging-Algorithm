#!/bin/bash
file="esc.csv"
echo "frame,dist_read,disk_write,rate" > $file
for i in {1..600}
do
   echo "running frame = ${i}"
   cmd=`python memsim.py ./samples/swim/swim.trace ${i} esc quiet`
   echo $cmd >> $file
done