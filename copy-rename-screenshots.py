#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-

# run from current directory with:
# python copy-rename-screenshots.py

"""
The problem: assuming file structure like this in INDIR:

├── r1
│   ├── scrshot_001_1.png
│   ├── scrshot_001_2.png
│   ├── scrshot_001_3.png
│   ├── scrshot_002_1.png
│   ├── scrshot_002_2.png
│   ├── scrshot_002_3.png
...
└── r2
    ├── scrshot_001_1.png
    ├── scrshot_001_2.png
    ├── scrshot_001_3.png
    ├── scrshot_002_1.png
    ├── scrshot_002_2.png
    ├── scrshot_002_3.png
...

... where the order is implied in sorting of r1, r2 subfolders:

* Find and print only the primary numeration in respective subfolders (i.e. r1/scrshot_001, r1/scrshot_002, ... r2/scrshot_001, r2/scrshot_002, ...)
* Recount, and print the new primary numeration for copy (i.e. OUTDIR/scrshot_001, OUTDIR/scrshot_002, ... OUTDIR/scrshot_00X, OUTDIR/scrshot_00Y, ...)
* Make a copy of all files from INDIR/{r1, r2...} to OUTDIR - with the new numeration
"""

import sys, os
import glob
import re
import shutil

INDIR="imgscrshot"
OUTDIR="imgscrshotB"

# create OUTDIR if it does not exist:
if not os.path.exists(OUTDIR):
  print("Creating directory {}".format(OUTDIR))
  os.makedirs(OUTDIR)

# glob all the .png files in indir - assuming r1, r2 folders will autosort?
all_indir_pngs = glob.glob('{}/*/*.png'.format(INDIR))
#print(all_indir_pngs)
# unfortunately, they do not autosort - files are essentially random, and r2 is before r1
# https://stackoverflow.com/questions/6773584/how-is-pythons-glob-glob-ordered "probably not sorted at all"

# sort in-place (SO: 36139 "case-sensitive sorting, don't take locale into account")
# just .sort() seems to do the right thing in sorting the filenames
all_indir_pngs.sort()

uniq_prim_names = []
for fullname in all_indir_pngs:
  # fullname is like: imgscrshot/r1/scrshot_001_1.png
  name = fullname.replace("{}{}".format(INDIR, os.sep), "") # get rid of imgscrshot/ at start
  name = re.sub('_\d\.png$', '', name)
  if name not in uniq_prim_names: uniq_prim_names.append(name)
  #print(name)

prim_names_new = []
for i, name in enumerate(uniq_prim_names):
  # name is like: r1/scrshot_001
  # extract the basename - from the / to the _:
  basename = re.findall('/(.*?)_', name)[0]
  newname = "{}_{:03}".format(basename, (i+1))
  prim_names_new.append(newname)
  print( "{} -> {}".format( name, newname ) )

print("---------")

for fullname in all_indir_pngs:
  uniqind=-1
  for ui, uniqname in enumerate(uniq_prim_names):
    if uniqname in fullname:
      uniqind = ui
      break
  fnnodir = fullname.replace("{}{}".format(INDIR, os.sep), "") # get rid of imgscrshot/ at start
  outname = fnnodir.replace(uniq_prim_names[uniqind], prim_names_new[uniqind])
  #~ print( "{} -> {} {} {}".format(fullname, uniqind, uniq_prim_names[uniqind], prim_names_new[uniqind]) )
  outnamefull = os.path.join(OUTDIR, outname)
  print( "{} -> {}".format(fullname, outnamefull) )
  shutil.copy(fullname, outnamefull)



"""
script prints out:

r1/scrshot_001 -> scrshot_001
r1/scrshot_002 -> scrshot_002
r1/scrshot_003 -> scrshot_003
r1/scrshot_004 -> scrshot_004
r1/scrshot_005 -> scrshot_005
r1/scrshot_006 -> scrshot_006
r1/scrshot_007 -> scrshot_007
r1/scrshot_008 -> scrshot_008
r2/scrshot_001 -> scrshot_009
r2/scrshot_002 -> scrshot_010
r2/scrshot_003 -> scrshot_011
r2/scrshot_004 -> scrshot_012
r2/scrshot_005 -> scrshot_013
r2/scrshot_006 -> scrshot_014
r2/scrshot_007 -> scrshot_015
r2/scrshot_008 -> scrshot_016
r2/scrshot_009 -> scrshot_017
r2/scrshot_010 -> scrshot_018
r2/scrshot_011 -> scrshot_019
r2/scrshot_012 -> scrshot_020
r2/scrshot_013 -> scrshot_021
r2/scrshot_014 -> scrshot_022
r2/scrshot_015 -> scrshot_023
r2/scrshot_016 -> scrshot_024
r2/scrshot_017 -> scrshot_025
r2/scrshot_018 -> scrshot_026
r2/scrshot_019 -> scrshot_027
---------
imgscrshot/r1/scrshot_001_1.png -> imgscrshotB/scrshot_001_1.png
imgscrshot/r1/scrshot_001_2.png -> imgscrshotB/scrshot_001_2.png
imgscrshot/r1/scrshot_001_3.png -> imgscrshotB/scrshot_001_3.png
imgscrshot/r1/scrshot_002_1.png -> imgscrshotB/scrshot_002_1.png
imgscrshot/r1/scrshot_002_2.png -> imgscrshotB/scrshot_002_2.png
imgscrshot/r1/scrshot_002_3.png -> imgscrshotB/scrshot_002_3.png
imgscrshot/r1/scrshot_003_1.png -> imgscrshotB/scrshot_003_1.png
imgscrshot/r1/scrshot_003_2.png -> imgscrshotB/scrshot_003_2.png
imgscrshot/r1/scrshot_003_3.png -> imgscrshotB/scrshot_003_3.png
imgscrshot/r1/scrshot_004_1.png -> imgscrshotB/scrshot_004_1.png
imgscrshot/r1/scrshot_004_2.png -> imgscrshotB/scrshot_004_2.png
imgscrshot/r1/scrshot_004_3.png -> imgscrshotB/scrshot_004_3.png
imgscrshot/r1/scrshot_005_1.png -> imgscrshotB/scrshot_005_1.png
imgscrshot/r1/scrshot_005_2.png -> imgscrshotB/scrshot_005_2.png
imgscrshot/r1/scrshot_005_3.png -> imgscrshotB/scrshot_005_3.png
imgscrshot/r1/scrshot_006_1.png -> imgscrshotB/scrshot_006_1.png
imgscrshot/r1/scrshot_006_2.png -> imgscrshotB/scrshot_006_2.png
imgscrshot/r1/scrshot_006_3.png -> imgscrshotB/scrshot_006_3.png
imgscrshot/r1/scrshot_007_1.png -> imgscrshotB/scrshot_007_1.png
imgscrshot/r1/scrshot_007_2.png -> imgscrshotB/scrshot_007_2.png
imgscrshot/r1/scrshot_007_3.png -> imgscrshotB/scrshot_007_3.png
imgscrshot/r1/scrshot_008_1.png -> imgscrshotB/scrshot_008_1.png
imgscrshot/r1/scrshot_008_2.png -> imgscrshotB/scrshot_008_2.png
imgscrshot/r1/scrshot_008_3.png -> imgscrshotB/scrshot_008_3.png
imgscrshot/r2/scrshot_001_1.png -> imgscrshotB/scrshot_009_1.png
imgscrshot/r2/scrshot_001_2.png -> imgscrshotB/scrshot_009_2.png
imgscrshot/r2/scrshot_001_3.png -> imgscrshotB/scrshot_009_3.png
imgscrshot/r2/scrshot_002_1.png -> imgscrshotB/scrshot_010_1.png
imgscrshot/r2/scrshot_002_2.png -> imgscrshotB/scrshot_010_2.png
imgscrshot/r2/scrshot_002_3.png -> imgscrshotB/scrshot_010_3.png
imgscrshot/r2/scrshot_003_1.png -> imgscrshotB/scrshot_011_1.png
imgscrshot/r2/scrshot_003_2.png -> imgscrshotB/scrshot_011_2.png
imgscrshot/r2/scrshot_003_3.png -> imgscrshotB/scrshot_011_3.png
imgscrshot/r2/scrshot_004_1.png -> imgscrshotB/scrshot_012_1.png
imgscrshot/r2/scrshot_004_2.png -> imgscrshotB/scrshot_012_2.png
imgscrshot/r2/scrshot_004_3.png -> imgscrshotB/scrshot_012_3.png
imgscrshot/r2/scrshot_005_1.png -> imgscrshotB/scrshot_013_1.png
imgscrshot/r2/scrshot_005_2.png -> imgscrshotB/scrshot_013_2.png
imgscrshot/r2/scrshot_005_3.png -> imgscrshotB/scrshot_013_3.png
imgscrshot/r2/scrshot_006_1.png -> imgscrshotB/scrshot_014_1.png
imgscrshot/r2/scrshot_006_2.png -> imgscrshotB/scrshot_014_2.png
imgscrshot/r2/scrshot_006_3.png -> imgscrshotB/scrshot_014_3.png
imgscrshot/r2/scrshot_007_1.png -> imgscrshotB/scrshot_015_1.png
imgscrshot/r2/scrshot_007_2.png -> imgscrshotB/scrshot_015_2.png
imgscrshot/r2/scrshot_007_3.png -> imgscrshotB/scrshot_015_3.png
imgscrshot/r2/scrshot_008_1.png -> imgscrshotB/scrshot_016_1.png
imgscrshot/r2/scrshot_008_2.png -> imgscrshotB/scrshot_016_2.png
imgscrshot/r2/scrshot_008_3.png -> imgscrshotB/scrshot_016_3.png
imgscrshot/r2/scrshot_009_1.png -> imgscrshotB/scrshot_017_1.png
imgscrshot/r2/scrshot_009_2.png -> imgscrshotB/scrshot_017_2.png
imgscrshot/r2/scrshot_009_3.png -> imgscrshotB/scrshot_017_3.png
imgscrshot/r2/scrshot_010_1.png -> imgscrshotB/scrshot_018_1.png
imgscrshot/r2/scrshot_010_2.png -> imgscrshotB/scrshot_018_2.png
imgscrshot/r2/scrshot_010_3.png -> imgscrshotB/scrshot_018_3.png
imgscrshot/r2/scrshot_011_1.png -> imgscrshotB/scrshot_019_1.png
imgscrshot/r2/scrshot_011_2.png -> imgscrshotB/scrshot_019_2.png
imgscrshot/r2/scrshot_011_3.png -> imgscrshotB/scrshot_019_3.png
imgscrshot/r2/scrshot_012_1.png -> imgscrshotB/scrshot_020_1.png
imgscrshot/r2/scrshot_012_2.png -> imgscrshotB/scrshot_020_2.png
imgscrshot/r2/scrshot_012_3.png -> imgscrshotB/scrshot_020_3.png
imgscrshot/r2/scrshot_013_1.png -> imgscrshotB/scrshot_021_1.png
imgscrshot/r2/scrshot_013_2.png -> imgscrshotB/scrshot_021_2.png
imgscrshot/r2/scrshot_013_3.png -> imgscrshotB/scrshot_021_3.png
imgscrshot/r2/scrshot_014_1.png -> imgscrshotB/scrshot_022_1.png
imgscrshot/r2/scrshot_014_2.png -> imgscrshotB/scrshot_022_2.png
imgscrshot/r2/scrshot_014_3.png -> imgscrshotB/scrshot_022_3.png
imgscrshot/r2/scrshot_015_1.png -> imgscrshotB/scrshot_023_1.png
imgscrshot/r2/scrshot_015_2.png -> imgscrshotB/scrshot_023_2.png
imgscrshot/r2/scrshot_015_3.png -> imgscrshotB/scrshot_023_3.png
imgscrshot/r2/scrshot_016_1.png -> imgscrshotB/scrshot_024_1.png
imgscrshot/r2/scrshot_016_2.png -> imgscrshotB/scrshot_024_2.png
imgscrshot/r2/scrshot_016_3.png -> imgscrshotB/scrshot_024_3.png
imgscrshot/r2/scrshot_017_1.png -> imgscrshotB/scrshot_025_1.png
imgscrshot/r2/scrshot_017_2.png -> imgscrshotB/scrshot_025_2.png
imgscrshot/r2/scrshot_017_3.png -> imgscrshotB/scrshot_025_3.png
imgscrshot/r2/scrshot_018_1.png -> imgscrshotB/scrshot_026_1.png
imgscrshot/r2/scrshot_018_2.png -> imgscrshotB/scrshot_026_2.png
imgscrshot/r2/scrshot_018_3.png -> imgscrshotB/scrshot_026_3.png
imgscrshot/r2/scrshot_019_1.png -> imgscrshotB/scrshot_027_1.png
imgscrshot/r2/scrshot_019_2.png -> imgscrshotB/scrshot_027_2.png
imgscrshot/r2/scrshot_019_3.png -> imgscrshotB/scrshot_027_3.png
"""
