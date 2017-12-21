#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-

# run with:
# python pyvirtdisp-starter.py

"""
This script starts a Xephyr window via pyvirtualdisplay; in which it instantiates:

* A `pcmanfm` file manager window, showing /tmp
* A `gnome-terminal` window, showing /tmp
* A `giggle` Git GUI client window, also started at /tmp (which will not be a .git repository, so not the entire window will be shown at start)

Then you can navigate manually to the right locations in these windows.

The Xephyr window should start with quarter size of the available desktop (queried via `xprop -root _NET_WORKAREA`).

When the windows are instantiated, you should be able to use Ctrl+Alt+Space to take a screenshot of all the windows, which will be numbered (numbers are reset at each run of the application), which will be stored in the `imgscrshot/` subfolder of this directory (will be created if it does not exist).

Tested on Ubuntu 14.04, MATE desktop.

Note that in Gnome, the file manager would typically also control the desktop - so the file manager that is currently in control of the desktop, cannot be opened in a Xephyr window; which is why MATE's file manager [Caja cannot run in Xephyr/pyvirtualdisplay, even with explicitly set display · Issue #886 · mate-desktop/caja](https://github.com/mate-desktop/caja/issues/886)

That is why, in this case a different file manager is used, to be opened in Xephyr. The `nemo` file manager was used, because it is somewhat simpler than `nautilus`, and it also has an "embedded terminal" addon, unlike `pcmanfm`; to install on Ubuntu 14.04, check http://www.webupd8.org/2014/04/install-nemo-220-with-unity-patches-in.html

However, `nemo` when opened as first in a DISPLAY, it blocks, and takes over the desktop - so all other `nemo` processes, started afterward, will run under it (so they don't block when run, but exit immediately after their windows are shown) - regardless of their individual DISPLAY setting (and if all the instances are started with `--no-desktop`)! And same goes for newer nemo (nemo 3.2.2) and nautilus! `pcmanfm` can get around this, though... so finally, here `pcmanfm` with separate `gnome-terminal` is used.

As a git GUI client, `giggle` can be easily set to show history, file tree, and open a text file; for other git GUI clients, see https://git-scm.com/downloads/guis/

Requirements/dependencies for this script:

* This script assumes that python2.7/dist-packages/pyvirtualdisplay/xephyr.py has been modified, so Xephyr is started with `-ac` (to allow X forwarding via ssh, see https://askubuntu.com/q/116936), and `-resizeable` (to allow to resize the window), and with hacks for position available on newer Xephyr - please check/apply the patch file `pyvirtualdisplay.patch`, available in this directory
* This script needs the `toggle-decorations` executable, which should be built from the `toggle-decorations.c` file in this directory (see inside that file, for instructions on how to build with gcc)
* This script runs `ssh` to do X11 forwarding, so `sudo apt-get install openssh-client` is a dependency
* This script uses `gnome-screenshot` to get screenshots

Python requirements for this script:

* pyvirtualdisplay - for install, see https://github.com/ponty/PyVirtualDisplay#ubuntu-1404
    * however, instead of `xserver-xephyr`, which in Ubuntu 14.04 is v. 2:1.15.1, install `xserver-xephyr-lts-xenial`, also available in vanilla repos for Ubuntu 14.04, which is v. 2:1.18.3, and includes support for '"-screen WxH+X+Y" option for window placement' (https://bugs.freedesktop.org/show_bug.cgi?id=12221 ; see also https://lists.freedesktop.org/archives/xorg/2007-September/028666.html)

* pyxhook - sudo pip install pyxhook (there is also keyboard - `sudo pip install keyboard`; unfortunately, it needs `sudo` to run on Linux)
* pexpect - sudo pip install pexpect

Note: some windows may fail to instantiate, if you have them hanging in the process list; e.g.
  $ ps axf | grep -v grep | grep pcmanfm
  31851 pts/2    Sl+    0:00  |           \_ pcmanfm /tmp  # parented to a pyvirtdisp-starter
  32084 pts/2    Sl     0:01 pcmanfm /tmp  # "hanging" process
... in which case they should be manually removed, e.g. `kill -9 32084`

Note: with this approach, it is not possible to copy/paste, sometimes even between applications in the same Xephyr window (you may want to start `glipper` in each Xephyr window, which will then allow for copy/paste in the same Xephyr window, but not between the Xephyr window and the desktop). To exchange message between terminals in Xephyr and the desktop, you can run `w` to get a list of terminals, and then `echo "My Message" > /dev/pts/12` to a specific terminal, or `echo "My Message" | sudo wall -n` to all terminals. Alternately, from the main desktop you can run `DISPLAY=:1001.0 gnome-terminal` and open another terminal in a given Xephyr window, and then exchange data through that (via `cat` or `nano`).

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


THIS_SCRIPT_DIR = os.path.dirname( os.path.abspath(os.path.realpath(__file__)) )
# just to make sure, change to this directory:
os.chdir(THIS_SCRIPT_DIR)
print("Running from dir: {}".format(os.getcwd()))

IMGDIR="imgscrshot"
IMGDIRFULL=os.path.join(THIS_SCRIPT_DIR, IMGDIR)
if not os.path.exists(IMGDIRFULL):
  print("Creating dir {}".format(IMGDIRFULL))
  os.makedirs(IMGDIRFULL)


# global lists:
disps = []
easyprocs = []
sshconns = []

ISCTRL=False
ISALT=False
# This function is called every time a key is presssed
def kbeventKeyDown(event):
  global running, ISCTRL, ISALT
  # print key info
  #~ print(event)

  # If the ascii value matches spacebar, terminate the while loop
  if event.Ascii == 27: # (Escape); was - 32: # (Space)
    if ISCTRL and ISALT: # so, react on Ctrl-Alt-Escape:
      ISCTRL=False
      ISALT=False
      running = False
  elif event.Ascii == 227 or event.Ascii == 228: # (Control_L, Control_R);
    ISCTRL = True
  elif event.Ascii == 233 or event.Ascii == 234: # (Alt_L, Alt_R);
    ISALT = True
  #elif event.Ascii == 83: # (S = shift+s); # may block with modifier keys?
  elif event.Ascii == 32: # (space);
    if ISCTRL and ISALT: # so, react on Ctrl-Alt-Space:
      TakeScreenshots()
      # since this reacts only on keydown, reset these two as well:
      ISCTRL=False
      ISALT=False
########## end kbeventKeyDown
def kbeventKeyUp(event):
  global ISCTRL, ISALT
  if event.Ascii == 227 or event.Ascii == 228: # (Control_L, Control_R);
    ISCTRL = False
  elif event.Ascii == 233 or event.Ascii == 234: # (Alt_L, Alt_R);
    ISALT = False
########## end kbeventKeyUp

NUMSCREENSHOTS=0

def TakeScreenshots():
  global NUMSCREENSHOTS, disps
  NUMSCREENSHOTS += 1
  scrshbasename = "scrshot_{:03}".format(NUMSCREENSHOTS)
  rep = []
  for ix, disptup in enumerate(disps):
    scrshname = os.path.join( IMGDIR, "{}_{}.png".format(scrshbasename, (ix+1)) )
    # disp = disptup[0] # get the SmartDisplay
    # # unfortunately, disp.waitgrab grabs screenshot of entire desktop, instead of what's inside; and after first screenshot, getting `Fatal IO error 11 ... on X server :0.0`, and process breaks...
    # #os.environ["DISPLAY"] = disptup[1] # no dice, still IO error
    # #disp.redirect_display(on=False) # True -> set $DISPLAY to virtual screen (False -> set $DISPLAY to original screen, i.e. unset DISPLAY), in abstractdisplay.py # no dice, still IO error
    # os.environ["DISPLAY"] = ":0.0" # no dice, still IO error
    # time.sleep(0.1)
    # img = disp.waitgrab()
    # img.save(scrshname,"PNG")
    ####
    # the above does not work, but `gnome-screenshot` can take screenshots from a different display, so use that..
    schcmd = "gnome-screenshot --display={} -f {}".format(disptup[1], scrshname)
    EasyProcess(schcmd).call()
    rep.append(scrshname)
    time.sleep(0.1)
  print("SCREENSHOT: {} !".format(" ".join(rep)))
########## end TakeScreenshots


# height/width percents
hp1 = 0.6
hp2 = 1.0-hp1 # the rest
wp1 = 0.6
wp2 = 1.0-wp1 # the rest


if __name__ == "__main__":
  # get available window dimenstions
  xcommand = "xprop -root _NET_WORKAREA"
  xoutput = subprocess.Popen(["bash", "-c", xcommand], stdout=subprocess.PIPE)
  xresponse = xoutput.communicate()[0].decode("utf-8").strip()
  xresparr = xresponse.split(' = ')[1].split(', ')
  xresparr = list( map(int, xresparr) )
  print("xresponse {}".format(xresparr)) # [0, 24, 1366, 743, 0, 24, 1366, 743, 0, 24, 1366, 743, 0, 24, 1366, 743] - for all four workspaces
  wdeskhalf = int(xresparr[2]/2);
  hdeskhalf = int(xresparr[3]/2);
  print("w, h deskhalf {} {}".format(wdeskhalf, hdeskhalf))
  origdisplay = os.environ['DISPLAY'] # expecting :0.0 here
  print("** display is: "+origdisplay + " " + os.environ['MATE_DESKTOP_SESSION_ID'] + " " + os.environ['DESKTOP_SESSION'] + " " + os.environ['XDG_CURRENT_DESKTOP'])
  #os.environ['NEMO_ACTION_VERBOSE'] = "1"

  # ... unfortunately, if we reuse ssh connection, then we cannot control the DISPLAY of the X11 forwarding, which need to be separate; so instead of reusing connection via ssh.config, just feed the password we'll obtain (sshpwd below)
  # pxssh can't really be set to use a config file;
  # try make an ssh connection with pexpect (check pexpect examples/ssh_tunnel.py)
  curuser = getpass.getuser()
  print("For the ssh connection to this machine as current user: {}@localhost".format(curuser))
  sshpwd = getpass.getpass('Enter password: ')

  # Create hookmanager # only after the keyboard passwording stuff is done!
  hookman = pyxhook.HookManager()
  # Define our callback to fire when a key is pressed down
  hookman.KeyDown = kbeventKeyDown
  hookman.KeyUp = kbeventKeyUp
  # Hook the keyboard
  hookman.HookKeyboard()
  # Start our listener
  hookman.start()

  def get_bit(byteval,idx): # SO: 2591483
    return int((byteval&(1<<idx))!=0);

  def AddDisplay():
    global disps, easyprocs, sshconns
    numdispwins = len(disps)
    if numdispwins > 0: numdispwins += 1 # this hack, so we have first top left, second bottom left, third bottom right
    mypos = ( (numdispwins%2)*wdeskhalf, get_bit(numdispwins,1)*hdeskhalf )
    disp = SmartDisplay(visible=1, size=(wdeskhalf, hdeskhalf), position=mypos).start()
    print("** AddDisplay is: "+os.environ['DISPLAY'] + " " + os.environ['MATE_DESKTOP_SESSION_ID'] + " " + os.environ['DESKTOP_SESSION'] + " " + os.environ['XDG_CURRENT_DESKTOP'])
    disps.append((disp, os.environ['DISPLAY']))
    #
    #mycmd='bash -c "echo AAA >> /tmp/test.log"' # shell redir has to be called like this!
    #
    # unfortunately, we cannot just call `nemo` here like the usual:
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
    time.sleep(0.25)
    ssh_cmd.expect(pexpect.EOF)
    sshconns.append(ssh_cmd)
    time.sleep(0.1)
    #
    mycmd='giggle /tmp'
    print("mycmd: {}".format(mycmd))
    gigglecmdproc = EasyProcess(mycmd).start()
    easyprocs.append(gigglecmdproc)
    time.sleep(0.1)
    #
    mycmd='pcmanfm /tmp'
    print("mycmd: {}".format(mycmd))
    pcmancmdproc = EasyProcess(mycmd).start()
    easyprocs.append(pcmancmdproc)
    time.sleep(0.1)
    #
    mycmd=['gnome-terminal', '--working-directory=/tmp', '-e', r'bash -c "bash --rcfile <( echo source $HOME/.bashrc ; echo PS1=\\\"user@PC:\\\\[\\\\033[0\;33\;1m\\\\]\\\w\\\[\\\033[00m\\\]\\\\$ \\\" ) -i"']
    print("mycmd: {}".format(mycmd))
    termcmdproc = EasyProcess(mycmd).start()
    easyprocs.append(termcmdproc)

  AddDisplay()
  time.sleep(0.2)
  # "You have to do this between each new Display." https://stackoverflow.com/q/30168169/
  # (else the second window does not instantiate, and the programs for it go in the first window)
  os.environ["DISPLAY"] = origdisplay # now that we mess with stuff, we (might) get segfault here?!
  AddDisplay()
  time.sleep(0.2)
  os.environ["DISPLAY"] = origdisplay
  AddDisplay()

  # instantiate first, then mess with decorations
  time.sleep(1)
  print("---")
  gtk.gdk.window_process_all_updates()
  gtk.gdk.flush() # doesn't do anything here..

  for disp in disps:
    thisdisp = gtk.gdk.Display(disp[1])
    dispscr = thisdisp.get_default_screen()
    print("d {} {} {} {} {}".format(disp[1], thisdisp, thisdisp.get_n_screens(), dispscr, dispscr.get_n_monitors()))

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
    #  also, for some reason, the terminal is smaller in height than needed (maybe due to removed decorations?), so there's a bit of a gap
    EasyProcess([ 'wmctrl', '-r', 'Terminal', '-e', '0,0,{},{},{}'.format(int(hdeskhalf*hp1), int(wdeskhalf*wp1), int(hdeskhalf*hp2)) ]).call()
    # Note: the calc is correct, but in this setup, giggle will not scale down in width
    #  below its own minimal width, so it will be wider than wdeskhalf*wp2;
    #  then even if pushed correctly to wdeskhalf*wp1, it will stick with right edge to right edge of screen,
    #  so it will look not exactly aligned, and would have to be moved manually
    #  (Alt+LeftClick works, when Xephyr window 'grabs mouse and keyboard')
    EasyProcess([ 'wmctrl', '-r', 'Giggle', '-e', '0,{},0,{},{}'.format(int(wdeskhalf*wp1), int(wdeskhalf*wp2), hdeskhalf) ]).call()

  # Create a loop to keep the application running (for detecting keypresses)
  running = True
  while running:
    time.sleep(0.5)

  # here we're out of the loop, stop everything
  #nemocmdproc.stop(); gigglecmdproc.stop(); disp.stop()
  for sshcmd in sshconns: sshcmd.close(force=True)
  for easyproc in easyprocs: easyproc.stop()
  for disp in disps:
    print("disp: {}".format(disp))
    disp[0].stop() # can cause, on the last entry: `Fatal IO error 11 (Resource temporarily unavailable) on X server :1013.`; in stop() method, `EasyProcess.stop(self)` kills last window, and by the time it gets to `if self.use_xauth:`, we get the `Fatal IO error 11..` - have no idea how to solve this atm, but it does not interfere with operation much, so can be ignored for the time being...
  # Close the listener when we are done
  hookman.cancel()

