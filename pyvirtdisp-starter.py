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

* This script assumes that python2.7/dist-packages/pyvirtualdisplay/xephyr.py has been modified, so Xephyr is started with `-ac` (to allow X forwarding via ssh, see https://askubuntu.com/q/116936), and `-resizeable` (to allow to resize the window)
* This script needs the `toggle-decorations` executable, which should be built from the `toggle-decorations.c` file in this directory (see inside that file, for instructions on how to build with gcc)

Python requirements for this script:

* pyvirtualdisplay - for install, see https://github.com/ponty/PyVirtualDisplay#ubuntu-1404
* pyxhook - sudo pip install pyxhook (there is also keyboard - `sudo pip install keyboard`; unfortunately, it needs `sudo` to run on Linux)
* pexpect - sudo pip install pexpect

"""

from easyprocess import EasyProcess
#~ from pyvirtualdisplay import Display
from pyvirtualdisplay.smartdisplay import SmartDisplay
import time
import sys, os
import pyxhook
import subprocess
import pexpect
import getpass
import gtk.gdk

#~ import Xlib
#~ import Xlib.display

THIS_SCRIPT_DIR = os.path.dirname( os.path.abspath(os.path.realpath(__file__)) )
# just to make sure, change to this directory:
os.chdir(THIS_SCRIPT_DIR)
print("Running from dir: {}".format(os.getcwd()))

# This function is called every time a key is presssed
def kbevent(event):
  global running
  # print key info
  #~ print(event)

  # If the ascii value matches spacebar, terminate the while loop
  if event.Ascii == 27: # (Escape); was - 32: # (Space)
    running = False
########## end kbevent


# height/width percents
hp1 = 0.6
hp2 = 1.0-hp1 # the rest
wp1 = 0.6
wp2 = 1.0-wp1 # the rest

disps = []
easyprocs = []
sshconns = []


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
  #os.environ['NEMO_ACTION_VERBOSE'] = "1"

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
    disps.append((disp, os.environ['DISPLAY']))
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
    # however, we must have mate-session (or gnome-session) ran before that;
    # else the wmctrl "cannot get client list properties"; mate-panel is not enough, but marco is (and it keeps small fonts - but adds titlebars)
    mycmd='ssh -XfC -c blowfish {}@localhost marco --replace --no-composite'.format(curuser) #  -F ssh.config
    #mycmd='ssh -XfC -c blowfish {}@localhost tinywm'.format(curuser) #  -F ssh.config # tinywm is so tiny, lists of windows are not managed
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
    mycmd='giggle /tmp'
    print("mycmd: {}".format(mycmd))
    gigglecmdproc = EasyProcess(mycmd).start()
    easyprocs.append(gigglecmdproc)
    #
    #~ mycmd='ssh -XfC -c blowfish {}@localhost nemo /tmp'.format(curuser) #  -F ssh.config #  --no-desktop seems to have no effect here...
    #~ print("mycmd: {}".format(mycmd))
    #~ ssh_cmd2 = pexpect.spawn(mycmd)
    #~ ssh_cmd2.expect('password: ')
    #~ time.sleep(0.1)
    #~ ssh_cmd2.sendline(sshpwd) # don't wait after this for EOF?
    #~ ssh_cmd2.expect(pexpect.EOF)
    #~ sshconns.append(ssh_cmd2)
    #
    mycmd='pcmanfm /tmp'
    print("mycmd: {}".format(mycmd))
    pcmancmdproc = EasyProcess(mycmd).start()
    easyprocs.append(pcmancmdproc)
    #
    mycmd=['gnome-terminal', '--working-directory=/tmp', '-e', r'bash -c "bash --rcfile <( echo source $HOME/.bashrc ; echo PS1=\\\"user@PC:\\\\[\\\\033[0\;33\;1m\\\\]\\\w\\\[\\\033[00m\\\]\\\\$ \\\" ) -i"']
    print("mycmd: {}".format(mycmd))
    termcmdproc = EasyProcess(mycmd).start()
    easyprocs.append(termcmdproc)
    # #
    # time.sleep(1) # wait for window to instantiate, else it is not listed
    # rootw = gtk.gdk.get_default_root_window()
    # # this lists only for DISPLAY=:0:
    # ## for id in rootw.property_get('_NET_CLIENT_LIST')[2]:
    # ##   w = gtk.gdk.window_foreign_new(id)
    # ##   if w:
    # ##     print("{} {}".format(id, w.property_get('WM_NAME')[2]))
    # wcurrootdat = rootw.property_get("_NET_ACTIVE_WINDOW") # ('WINDOW', 32, [102760449]) - refers to 0x06200001 Xephyr on :1005.0 etc window ; 102760449 = 0x6200001
    # wcurrootid = wcurrootdat[2][0]
    # wr = gtk.gdk.window_foreign_new( wcurrootid )
    # # w.set_decorations here changes the titlebar od the Xephyr window!
    # thisdisp = gtk.gdk.Display(os.environ['DISPLAY'])
    # print("wr {} {} // {} d {}".format(wcurrootdat, wr.get_decorations(), wr.get_children(), thisdisp )) # <flags 0 of type GdkWMDecoration> // [] empty here even w/ wait; at next toggle, flags GDK_DECOR_ALL
    # winlist = EasyProcess('wmctrl -l').call().stdout # prints according to current DISPLAY
    # print("winlist: {}".format(winlist))
    # dispscr = thisdisp.get_default_screen()
    # disprootw = dispscr.get_root_window()
    # # ok, listing the right children under current DISPLAY with this:
    # for id in disprootw.property_get('_NET_CLIENT_LIST')[2]:
    #   w = gtk.gdk.window_foreign_new_for_display(thisdisp, id)
    #   if w:
    #     print("d {} {} {}".format(id, w.property_get('WM_NAME')[2], w.get_decorations()))
    # # for line in iter(winlist.splitlines()):
    # #   hexidstr = line.split()[0] # split() no args, split on whitespace
    # #   hexid = int(hexidstr, 0) # "You must specify 0 as the base in order to invoke this prefix-guessing behavior"
    # #   print("hex: {} {}".format(hexidstr, hexid))
    # #   #~ w = gtk.gdk.window_foreign_new( hexid ) # cannot use this here, only for default DISPLAY
    # #   w = gtk.gdk.window_foreign_new_for_display( thisdisp, hexid ) # this sorta works? but getting segfault later?
    # #   print("w {} {}".format(w, w.get_decorations())) # <flags GDK_DECOR_ALL of type GdkWMDecoration>
    # #   w.set_decorations( (w.get_decorations()+1)%2 ) # toggle between 0 and 1
    # #   print("w {} {}".format(w, w.get_decorations())) #
    # #~ gtk.gdk.window_process_all_updates() # this causes segfault ?!
    # #~ gtk.gdk.flush() # this may actually effectuate no title bars, because at start, all of them show undecorated!

  AddDisplay()
  # "You have to do this between each new Display." https://stackoverflow.com/q/30168169/
  # (else the second window does not instantiate, and the programs for it go in the first window)
  # time.sleep(1)
  os.environ["DISPLAY"] = origdisplay # now that we mess with stuff, we get segfault here?!
  AddDisplay()

  # instantiate first, then mess with decorations
  time.sleep(1)
  print("---")
  #gtk.gdk.DisplayManager.list_displays() #descriptor 'list_displays' of 'gtk.gdk.DisplayManager' object needs an argument
  gDMo = gtk.gdk.display_manager_get()
  print(gDMo) #"{} {}".format(gDMo, dir(gDMo)))
  gDMo.list_displays() # nothing here
  print("---")
  gtk.gdk.window_process_all_updates()
  gtk.gdk.flush() # doesn't do anything here..

  for disp in disps:
    thisdisp = gtk.gdk.Display(disp[1])
    dispscr = thisdisp.get_default_screen()
    print("d {} {} {} {} {}".format(disp[1], thisdisp, thisdisp.get_n_screens(), dispscr, dispscr.get_n_monitors()))
    # disprootw = dispscr.get_root_window() # here segfault, assertion 'GDK_IS_SCREEN (screen)' failed - but only on second loop!
  #   # # ok, listing the right children under current DISPLAY with this:
  #   # for id in disprootw.property_get('_NET_CLIENT_LIST')[2]:
  #   for w in dispscr.get_toplevel_windows():
  #    # w = gtk.gdk.window_foreign_new_for_display(thisdisp, id)
  #     if w:
  #       id = w.xid # exists, but is the same for different displays ?! and WM_NAME is wrong, too!
  #       print("  {} {} {} {}".format(disp[1], id, w.property_get('WM_NAME')[2], w.get_decorations()))
  #   time.sleep(1)

  for disp in disps:
    os.environ["DISPLAY"] = disp[1]
    winlist = EasyProcess('wmctrl -l').call().stdout # prints according to current DISPLAY
    print("winlist: {}".format(winlist))
    # first, try remove the decoration/titlebar from all windows
    for line in iter(winlist.splitlines()):
      hexidstr = line.split()[0] # split() no args, split on whitespace
      hexid = int(hexidstr, 0) # "You must specify 0 as the base in order to invoke this prefix-guessing behavior"
      print("hex: {} {}".format(hexidstr, hexid))
      EasyProcess('./toggle-decorations '+hexidstr).call()
    # to call with hex id, use wmctrl -i -r 0x00...
    # the nemo is/may be maximized, so we have to unmaximize it first
    EasyProcess('wmctrl -r tmp -b remove,maximized_horz').call()
    EasyProcess('wmctrl -r tmp -b remove,maximized_vert').call()
    EasyProcess( 'wmctrl -r tmp -e 0,0,0,{},{}'.format(int(wdeskhalf*wp1), int(hdeskhalf*hp1)) ).call()
    # Giggle/Terminal is not maximised, so we can manipulate it immediately:
    EasyProcess([ 'wmctrl', '-r', 'Terminal', '-e', '0,0,{},{},{}'.format(int(hdeskhalf*hp1), int(wdeskhalf*wp1), int(hdeskhalf*hp2)) ]).call()
    # Note: the calc is correct, but in this setup, giggle will not scale down in width
    #  below its own minimal width, so it will be wider than wdeskhalf*wp2;
    #  then even if pushed correctly to wdeskhalf*wp1, it will stick with right edge to right edge of screen,
    #  so it will look not exactly aligned, and would have to be moved manually
    #  (Alt+LeftClick works, when Xephyr window 'grabs mouse and keyboard')
    EasyProcess([ 'wmctrl', '-r', 'Giggle', '-e', '0,{},0,{},{}'.format(int(wdeskhalf*wp1), int(wdeskhalf*wp2), hdeskhalf) ]).call()

  #~ display = Xlib.display.Display()

  # Create a loop to keep the application running (for detecting keypresses
  running = True
  while running:
    time.sleep(0.1)

  # here we're out of the loop, stop everything
  #nemocmdproc.stop(); gigglecmdproc.stop(); disp.stop()
  for easyproc in easyprocs: easyproc.stop()
  for disp in disps: disp[0].stop()
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

    #~ mycmd='gnome-session'
    #~ print("mycmd: {}".format(mycmd))
    #~ gsesscmdproc = EasyProcess(mycmd).start()
    #~ easyprocs.append(gsesscmdproc)

    #~ mycmd='gnome-terminal'
    #~ print("mycmd: {}".format(mycmd))
    #~ termcmdproc = EasyProcess(mycmd).start()
    #~ easyprocs.append(termcmdproc)

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

