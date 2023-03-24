#!/bin/sh
# Convert all arguments (assumed to be SVG) to a TIFF.
# Requires Inkscape and ImageMagick 6.8 (doesn't work with 6.6.9).
# From matsen: https://gist.github.com/matsen/4263955


for i in *.svg; do
  BN=$(basename $i .svg)
  inkscape --without-gui --export-filename="output/$BN.png" --export-dpi 300 $i
  magick -compress LZW output/$BN.png output/$BN.tiff
#   mogrify -alpha off $BN.tiff
  rm output/$BN.png
done
