#!/bin/bash
#
if [ $# -lt 3 ]
then
   echo
   echo "Usage: minfo -m <meta-type> <epub-file>"
   echo
else
   fileloc=`unzip -l "$3" | grep -Po '\b[^\s-]*\.opf\b'`
   metafound=`zipgrep  '<dc:'$2'>(.*)</dc:'$2'>' "$3" $fileloc`
   echo `expr "$metafound" : '.*<dc:'$2'>\(.*\)</dc:'$2'>.*'`
fi