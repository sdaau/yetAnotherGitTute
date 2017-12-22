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
margin = 10
def generate_montage(filenames, output_fn):
  images = [Image.open(filename) for filename in filenames]

  width = margin + max(image.size[0] + margin for image in images)*row_size
  height = margin + max(image.size[1] + margin for image in images)*col_size
  montage = Image.new(mode='RGBA', size=(width, height), color=(20,20,20,255))

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

  montage.save(output_fn)


###################### start:

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




"""
script prints out:

img/scrshot_001.png: ['imgscrshotB/scrshot_001_1.png', 'imgscrshotB/scrshot_001_2.png', 'imgscrshotB/scrshot_001_3.png']
img/scrshot_002.png: ['imgscrshotB/scrshot_002_1.png', 'imgscrshotB/scrshot_002_2.png', 'imgscrshotB/scrshot_002_3.png']
img/scrshot_003.png: ['imgscrshotB/scrshot_003_1.png', 'imgscrshotB/scrshot_003_2.png', 'imgscrshotB/scrshot_003_3.png']
img/scrshot_004.png: ['imgscrshotB/scrshot_004_1.png', 'imgscrshotB/scrshot_004_2.png', 'imgscrshotB/scrshot_004_3.png']
img/scrshot_005.png: ['imgscrshotB/scrshot_005_1.png', 'imgscrshotB/scrshot_005_2.png', 'imgscrshotB/scrshot_005_3.png']
img/scrshot_006.png: ['imgscrshotB/scrshot_006_1.png', 'imgscrshotB/scrshot_006_2.png', 'imgscrshotB/scrshot_006_3.png']
img/scrshot_007.png: ['imgscrshotB/scrshot_007_1.png', 'imgscrshotB/scrshot_007_2.png', 'imgscrshotB/scrshot_007_3.png']
img/scrshot_008.png: ['imgscrshotB/scrshot_008_1.png', 'imgscrshotB/scrshot_008_2.png', 'imgscrshotB/scrshot_008_3.png']
img/scrshot_009.png: ['imgscrshotB/scrshot_009_1.png', 'imgscrshotB/scrshot_009_2.png', 'imgscrshotB/scrshot_009_3.png']
img/scrshot_010.png: ['imgscrshotB/scrshot_010_1.png', 'imgscrshotB/scrshot_010_2.png', 'imgscrshotB/scrshot_010_3.png']
img/scrshot_011.png: ['imgscrshotB/scrshot_011_1.png', 'imgscrshotB/scrshot_011_2.png', 'imgscrshotB/scrshot_011_3.png']
img/scrshot_012.png: ['imgscrshotB/scrshot_012_1.png', 'imgscrshotB/scrshot_012_2.png', 'imgscrshotB/scrshot_012_3.png']
img/scrshot_013.png: ['imgscrshotB/scrshot_013_1.png', 'imgscrshotB/scrshot_013_2.png', 'imgscrshotB/scrshot_013_3.png']
img/scrshot_014.png: ['imgscrshotB/scrshot_014_1.png', 'imgscrshotB/scrshot_014_2.png', 'imgscrshotB/scrshot_014_3.png']
img/scrshot_015.png: ['imgscrshotB/scrshot_015_1.png', 'imgscrshotB/scrshot_015_2.png', 'imgscrshotB/scrshot_015_3.png']
img/scrshot_016.png: ['imgscrshotB/scrshot_016_1.png', 'imgscrshotB/scrshot_016_2.png', 'imgscrshotB/scrshot_016_3.png']
img/scrshot_017.png: ['imgscrshotB/scrshot_017_1.png', 'imgscrshotB/scrshot_017_2.png', 'imgscrshotB/scrshot_017_3.png']
img/scrshot_018.png: ['imgscrshotB/scrshot_018_1.png', 'imgscrshotB/scrshot_018_2.png', 'imgscrshotB/scrshot_018_3.png']
img/scrshot_019.png: ['imgscrshotB/scrshot_019_1.png', 'imgscrshotB/scrshot_019_2.png', 'imgscrshotB/scrshot_019_3.png']
img/scrshot_020.png: ['imgscrshotB/scrshot_020_1.png', 'imgscrshotB/scrshot_020_2.png', 'imgscrshotB/scrshot_020_3.png']
img/scrshot_021.png: ['imgscrshotB/scrshot_021_1.png', 'imgscrshotB/scrshot_021_2.png', 'imgscrshotB/scrshot_021_3.png']
img/scrshot_022.png: ['imgscrshotB/scrshot_022_1.png', 'imgscrshotB/scrshot_022_2.png', 'imgscrshotB/scrshot_022_3.png']
img/scrshot_023.png: ['imgscrshotB/scrshot_023_1.png', 'imgscrshotB/scrshot_023_2.png', 'imgscrshotB/scrshot_023_3.png']
img/scrshot_024.png: ['imgscrshotB/scrshot_024_1.png', 'imgscrshotB/scrshot_024_2.png', 'imgscrshotB/scrshot_024_3.png']
img/scrshot_025.png: ['imgscrshotB/scrshot_025_1.png', 'imgscrshotB/scrshot_025_2.png', 'imgscrshotB/scrshot_025_3.png']
img/scrshot_026.png: ['imgscrshotB/scrshot_026_1.png', 'imgscrshotB/scrshot_026_2.png', 'imgscrshotB/scrshot_026_3.png']
img/scrshot_027.png: ['imgscrshotB/scrshot_027_1.png', 'imgscrshotB/scrshot_027_2.png', 'imgscrshotB/scrshot_027_3.png']

"""
