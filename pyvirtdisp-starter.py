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

However, `nemo` when opened as first in a DISPLAY, it blocks, and takes over the desktop - so all other `nemo` processes, started afterward, will run under it (so they don't block when run, but exit immediately after their windows are shown) - regardless of their individual DISPLAY setting (and if all the instances are started with `--no-desktop`)! And same goes for newer nemo (nemo 3.2.2) and nautilus! `pcmanfm` can get around this, though...

As a git GUI client, `giggle` can be easily set to show history, file tree, and open a text file; for other git GUI clients, see https://git-scm.com/downloads/guis/

* Note: this script assumes that python2.7/dist-packages/pyvirtualdisplay/xephyr.py has been modified, so Xephyr is started with `-ac` (to allow X forwarding via ssh, see https://askubuntu.com/q/116936), and `-resizeable` (to allow to resize the window)

Python requirements for this script:

* pyvirtualdisplay - for install, see https://github.com/ponty/PyVirtualDisplay#ubuntu-1404
* pyxhook - sudo pip install pyxhook (there is also keyboard - `sudo pip install keyboard`; unfortunately, it needs `sudo` to run on Linux)
* pexpect - sudo pip install pexpect

"""

from easyprocess import EasyProcess
#~ from pyvirtualdisplay import Display
from pyvirtualdisplay.smartdisplay import SmartDisplay
import time
import os
import pyxhook
import subprocess
import pexpect
import getpass

# This function is called every time a key is presssed
def kbevent(event):
  global running
  # print key info
  #~ print(event)

  # If the ascii value matches spacebar, terminate the while loop
  if event.Ascii == 27: # (Escape); was - 32: # (Space)
    running = False


if __name__ == "__main__":
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
  origdisplay = os.environ['DISPLAY'] # expecting :0.0 here
  print("** display is: "+origdisplay + " " + os.environ['MATE_DESKTOP_SESSION_ID'] + " " + os.environ['DESKTOP_SESSION'] + " " + os.environ['XDG_CURRENT_DESKTOP'])
  os.environ['NEMO_ACTION_VERBOSE'] = "1"

  # to reuse ssh connections; this:
#  MYSSHCONFFILESTR="""
#host *
#    controlmaster auto
#    controlpath /tmp/ssh-%r@%h:%p
#"""
#  with open("ssh.config", "w") as text_file:
#    text_file.write(MYSSHCONFFILESTR)
  # ... unfortunately, if we reuse, then we cannot control the DISPLAY of the X11 forwarding, which need to be separate; so instead of reusing connection via ssh.config, just feed the password we'll obtain (sshpwd below)
  # pxssh can't really be set to use this config file;
  # try make an ssh connection with pexpect (check pexpect examples/ssh_tunnel.py)
  curuser = getpass.getuser()
  print("For the ssh connection to this machine as current user: {}@localhost".format(curuser))
  sshpwd = getpass.getpass('Enter password: ')

  # even if this does run, if we reuse connections, then we don't have the right DISPLAY
  # starter_ssh_cmd = "ssh -F ssh.config -XC -c blowfish {}@localhost".format(curuser)
  # try:
  #   ssh_starter = pexpect.spawn(starter_ssh_cmd)
  #   ssh_starter.expect('password: ')
  #   print('(sleeping a bit after expecting password: ...)')
  #   time.sleep(0.1)
  #   ssh_starter.sendline(sshpwd)
  #   print('(after sendline  ...)')
  #   #time.sleep(60) # Cygwin is slow to update process status.
  #   time.sleep(5) # also on linux, tends to wait here a lot more than the timeout
  #   ssh_starter.expect(pexpect.EOF)
  # except Exception as e:
  #   print("Got Exception: " + str(e))

  disps = []
  easyprocs = []
  sshconns = []

  # Create hookmanager # only after the keyboard passwording stuff is done!
  hookman = pyxhook.HookManager()
  # Define our callback to fire when a key is pressed down
  hookman.KeyDown = kbevent
  # Hook the keyboard
  hookman.HookKeyboard()
  # Start our listener
  hookman.start()

  def AddDisplay():
    global disps, easyprocs
    disp = SmartDisplay(visible=1, size=(wdeskhalf, hdeskhalf)).start()
    print("** AddDisplay is: "+os.environ['DISPLAY'] + " " + os.environ['MATE_DESKTOP_SESSION_ID'] + " " + os.environ['DESKTOP_SESSION'] + " " + os.environ['XDG_CURRENT_DESKTOP'])
    disps.append(disp)
    #
    #mycmd='bash -c "echo AAA >> /tmp/test.log"' # shell redir has to be called like this!
    #
    # unfortunately, we cannot just call `nemo` here like the usual:
    #~ mycmd='nemo --no-desktop --display='+os.environ['DISPLAY']+' /tmp'
    #~ print("mycmd: {}".format(mycmd))
    #~ nemocmdproc = EasyProcess(mycmd).start()
    #~ easyprocs.append(nemocmdproc)
    # - it will take over the first Xephyr window as desktop manager, and all subsequent `nemo`s will open there;
    # however, we can use SSH X11 forwarding, which seems to fix that:
    mycmd='ssh -XfC -c blowfish {}@localhost nemo'.format(curuser) #  -F ssh.config
    print("mycmd: {}".format(mycmd))
    #gscmdproc = EasyProcess(mycmd).start()
    #easyprocs.append(gscmdproc)
    ssh_cmd = pexpect.spawn(mycmd)
    ssh_cmd.expect('password: ')
    time.sleep(0.1)
    ssh_cmd.sendline(sshpwd) # don't wait after this for EOF?
    ssh_cmd.expect(pexpect.EOF)
    sshconns.append(ssh_cmd)
    #
    #~ mycmd='gnome-session'
    #~ print("mycmd: {}".format(mycmd))
    #~ gsesscmdproc = EasyProcess(mycmd).start()
    #~ easyprocs.append(gsesscmdproc)
    mycmd='giggle /tmp'
    print("mycmd: {}".format(mycmd))
    gigglecmdproc = EasyProcess(mycmd).start()
    easyprocs.append(gigglecmdproc)
    #~ mycmd='gnome-terminal'
    #~ print("mycmd: {}".format(mycmd))
    #~ termcmdproc = EasyProcess(mycmd).start()
    #~ easyprocs.append(termcmdproc)

  AddDisplay()
  # "You have to do this between each new Display." https://stackoverflow.com/q/30168169/
  # (else the second window does not instantiate, and the programs for it go in the first window)
  os.environ["DISPLAY"] = origdisplay
  AddDisplay()

  # Create a loop to keep the application running (for detecting keypresses
  running = True
  while running:
    time.sleep(0.1)

  # here we're out of the loop, stop everything
  #nemocmdproc.stop(); gigglecmdproc.stop(); disp.stop()
  for easyproc in easyprocs: easyproc.stop()
  for disp in disps: disp.stop()
  # also:
  #~ ssh_starter.close(force=True)
  for sshcmd in sshconns: sshcmd.close(force=True)
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

