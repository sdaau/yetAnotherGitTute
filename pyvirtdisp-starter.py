#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-

# run with:
# python pyvirtdisp-starter.py

"""
This script starts a Xephyr window via pyvirtualdisplay; in which it instantiates:

* A `nemo` file manager window, showing /tmp
* A `giggle` Git GUI client window, also started at /tmp (which will not be a .git repository, so not the entire window will be shown at start)

Then you can navigate manually to the right locations in these windows.

The Xephyr window should start with quarter size of the available desktop (queried via `xprop -root _NET_WORKAREA`).

Tested on Ubuntu 14.04, MATE desktop.
Note that in Gnome, the file manager would typically also control the desktop - so the file manager that is currently in control of the desktop, cannot be opened in a Xephyr window; which is why MATE's file manager [Caja cannot run in Xephyr/pyvirtualdisplay, even with explicitly set display · Issue #886 · mate-desktop/caja](https://github.com/mate-desktop/caja/issues/886)

That is why, in this case a different file manager is used, to be opened in Xephyr. The `nemo` file manager was used, because it is somewhat simpler than `nautilus`, and it also has an "embedded terminal" addon, unlike `pcmanfm`; to install on Ubuntu 14.04, check http://www.webupd8.org/2014/04/install-nemo-220-with-unity-patches-in.html

As a git GUI client, `giggle` can be easily set to show history, file tree, and open a text file; for other git GUI clients, see https://git-scm.com/downloads/guis/

Python requirements for this script:

* pyvirtualdisplay - for install, see https://github.com/ponty/PyVirtualDisplay#ubuntu-1404
* pyxhook - sudo pip install pyxhook (there is also keyboard - `sudo pip install keyboard`; unfortunately, it needs `sudo` to run on Linux)

"""

from easyprocess import EasyProcess
#~ from pyvirtualdisplay import Display
from pyvirtualdisplay.smartdisplay import SmartDisplay
import time
import os
import pyxhook
import subprocess


# This function is called every time a key is presssed
def kbevent(event):
  global running
  # print key info
  print(event)

  # If the ascii value matches spacebar, terminate the while loop
  if event.Ascii == 27: # (Escape); was - 32: # (Space)
    running = False


if __name__ == "__main__":
  # Create hookmanager
  hookman = pyxhook.HookManager()
  # Define our callback to fire when a key is pressed down
  hookman.KeyDown = kbevent
  # Hook the keyboard
  hookman.HookKeyboard()
  # Start our listener
  hookman.start()

  # get available window dimenstions
  xcommand = "xprop -root _NET_WORKAREA"
  xoutput = subprocess.Popen(["bash", "-c", xcommand], stdout=subprocess.PIPE)
  xresponse = xoutput.communicate()[0].decode("utf-8").strip()
  xresparr = xresponse.split(' = ')[1].split(', ')
  xresparr = list( map(int, xresparr) )
  print("xresponse {}".format(xresparr)) # [0, 24, 1366, 743, 0, 24, 1366, 743, 0, 24, 1366, 743, 0, 24, 1366, 743] - for all four workspaces
  wdeskhalf = xresparr[2]/2;
  hdeskhalf = xresparr[3]/2;
  print("w, h deskhalf {} {}".format(wdeskhalf, hdeskhalf))
  thisdisplay = os.environ['DISPLAY']
  print("display is: "+thisdisplay + " " + os.environ['MATE_DESKTOP_SESSION_ID'] + " " + os.environ['DESKTOP_SESSION'] + " " + os.environ['XDG_CURRENT_DESKTOP'])

  disps = []
  easyprocs = []

  def AddDisplay():
    global disps, easyprocs
    disp = SmartDisplay(visible=1, size=(wdeskhalf, hdeskhalf)).start()
    print("display is: "+os.environ['DISPLAY'] + " " + os.environ['MATE_DESKTOP_SESSION_ID'] + " " + os.environ['DESKTOP_SESSION'] + " " + os.environ['XDG_CURRENT_DESKTOP'])
    disps.append(disp)
    mycmd='nemo --no-desktop /tmp'
    print("mycmd: {}".format(mycmd))
    nemocmdproc = EasyProcess(mycmd).start()
    easyprocs.append(nemocmdproc)
    mycmd='giggle /tmp'
    print("mycmd: {}".format(mycmd))
    gigglecmdproc = EasyProcess(mycmd).start()
    easyprocs.append(gigglecmdproc)

  AddDisplay()
  AddDisplay()

  # Create a loop to keep the application running (for detecting keypresses
  running = True
  while running:
    time.sleep(0.1)

  # here we're out of the loop, stop everything
  #nemocmdproc.stop(); gigglecmdproc.stop(); disp.stop()
  for easyproc in easyprocs: easyproc.stop()
  for disp in disps: disp.stop()
  # Close the listener when we are done
  hookman.cancel()


"""
  #~ Display(visible=1, size=(320, 240)).start()
  #EasyProcess('startx').start()
  #EasyProcess('gnome-calculator').start()
  #~ time.sleep(2)
  #~ mycmd='caja --display='+thisdisplay+' --no-desktop /tmp'
  #~ mycmd='marco'
  #~ mycmd='marco --display='+thisdisplay+'.0'
  #~ print(mycmd)
  #~ EasyProcess(mycmd).start()
  #~ mycmd='caja --display='+thisdisplay+'.0 --no-desktop /tmp'
  #~ mycmd='pcmanfm /tmp'
"""


"""
from easyprocess import EasyProcess
from pyvirtualdisplay import Display
#~ from pyvirtualdisplay.smartdisplay import SmartDisplay # needs pyscreenshot
import logging
logging.basicConfig(level=logging.DEBUG)
import time

_W = 600
_H = 500
# height percents
hp1 = 0.6
hp2 = 1-hp1 # the rest


Display(visible=1, size=(_W , _H)).start()

# EasyProcess.start() # spawns process in background
# EasyProcess.check() # loops process in foreground


try:
  EasyProcess('awesome -c rc.lua').start()
except Exception, detail:
  print  detail

time.sleep(2)

try:
  EasyProcess('bash -c "cd $HOME && scite"').start()
except Exception, detail:
  print  detail

time.sleep(2)

try:
  # 0,x,y,w,h
  EasyProcess(['wmctrl', '-r', 'SciTE', '-e', '0,0,0,'+str(_W)+','+str(int(_H*hp1))]).start()
except Exception, detail:
  print  detail

# gnome-terminal -e 'bash -c "bash --rcfile <(echo source $HOME/.bashrc ; echo PS1=\\\"\$ \\\") -i"'
# first `bash` needed, otherwise cannot do process substitution as file

try:
  EasyProcess(['gnome-terminal', '-e', 'bash -c "bash --rcfile <(echo source $HOME/.bashrc ; echo PS1=\\\"\$\ \\\") -i"']).start() # --maximize is Gnome, nowork
except Exception, detail:
  print  detail

time.sleep(0.5)

try:
  # 0,x,y,w,h
  EasyProcess(['wmctrl', '-r', 'Terminal', '-e', '0,0,'+str(int(_H*hp1))+','+str(_W)+','+str(int(_H*hp2))]).start()
except Exception, detail:
  print  detail
"""

