#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-

# run from current directory with:
# python montage-screenshots.py

"""
The problem: assuming screenshot .pngs like this in INDIR:

├── scrshot_001_1.png
├── scrshot_001_2.png
├── scrshot_001_3.png
├── scrshot_002_1.png
├── scrshot_002_2.png
├── scrshot_002_3.png
...

... make a montage of each set of _1, _2 and _3 .png (bound by a basename, say scrshot_001) in a square 2x2 grid, such that:

* _1.png is top center
* _2.png is bottom left
* _3.png is bottom right

... and then save the corresponding montage as OUTDIR/scrshot_001.png
"""

import sys, os
import glob
import re

INDIR="imgscrshotB"
OUTDIR="img"

# based on SO: 17555345
import Image
row_size = 2 # how many elems in row
col_size = 2
margin = 5
def generate_montage(filenames, output_fn):
  images = [Image.open(filename) for filename in filenames]

  width = margin + max(image.size[0] + margin for image in images)*row_size
  height = margin + max(image.size[1] + margin for image in images)*col_size
  montage = Image.new(mode='RGBA', size=(width, height), color=(180,180,180,255))

  #~ max_x = 0
  #~ max_y = 0
  offset_x = 0
  offset_y = 0

  for i,image in enumerate(images):
    if i == 0:
      offset_x = int(round(width/2.0 - image.size[0]/2.0))
      offset_y = margin
    elif i == 1:
      offset_x = margin
      offset_y = height - margin - image.size[1]
    elif i == 2:
      offset_x = width - margin - image.size[0]
      offset_y = height - margin - image.size[1]

    montage.paste(image, (offset_x, offset_y))

    #~ max_x = max(max_x, offset_x + image.size[0])
    #~ max_y = max(max_y, offset_y + image.size[1])

    #~ if i % row_size == row_size-1:
      #~ offset_y = max_y + margin
      #~ offset_x = 0
    #~ else:
      #~ offset_x += margin + image.size[0]

  #~ montage = montage.crop((0, 0, max_x, max_y))
  montage.save(output_fn)




# glob all the .png files in indir (assumming ALL are like _1, _2, _3)
all_indir_pngs = glob.glob('{}/*.png'.format(INDIR))
# sort in-place
all_indir_pngs.sort()

uniq_prim_names = []
for fullname in all_indir_pngs:
  # fullname is like: imgscrshotB/scrshot_001_1.png
  name = fullname.replace("{}{}".format(INDIR, os.sep), "") # get rid of imgscrshotB/ at start
  name = re.sub('_\d\.png$', '', name)
  if name not in uniq_prim_names: uniq_prim_names.append(name)
  #~ print(name)

# iterate through uniq_prim_names, grab sets of three images related to uniqbasename, generate out filename - then create montage, and save as out filename

for i, ubname in enumerate(uniq_prim_names):
  myubnameset = []
  # unoptimized: go through all_indir_pngs, check which of the filenames match ubname, and put those in myubnameset
  for fullname in all_indir_pngs:
    if ubname in fullname:
      myubnameset.append(fullname)
  outname = os.path.join( OUTDIR, "{}.png".format(ubname) )
  print( "{}: {}".format(outname, myubnameset) )
  generate_montage(myubnameset, outname)
