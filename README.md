# Yet another Git tutorial

This is a brief tutorial on the SCM ([Source Control or Source Code Management](https://en.wikipedia.org/wiki/Source_control_management)) - aka VCS (Version Control System) - software [`git`](https://en.wikipedia.org/wiki/Git). It will focus on an offline (local) demonstration of basic operations, as well as conflicts and resolving them.

Crudely speaking, SCM/VCS allows one to track history of changes of files in a directory - the user creates, modifies or deletes files inside this directory; and the user can choose, at any time, to record the current state of the files in history by _committing_ them, the recorded state being known as a _commit_.

As more commits are added to the history, an SCM/VCS allows that the exact state of a previous commit can be restored in the working directory - which is particularly useful in software coding; say, in cases when a bug has been introduced by a more recent change (which should otherwise introduce a new feature). Such a directory, with contents with tracked history, is typically referred to as a _project_ or a _repository_ (that is, "repo").

Before we get going, note that:

* Git/`git` is the name of the SCM/VCS system and software, with a homepage at https://git-scm.com/
* GitHub is the name of a company, which offers hosting services and tools for `git` projects, with a homepage at https://github.com/ (one among many others, such as SourceForge https://sourceforge.net/ GitLab https://gitlab.com/ Bitbucket https://bitbucket.org/ etc).

-----

This tutorial has been tested on git version 1.9.1 on Ubuntu 14.04, a GNU/Linux operating system (OS). As such, it should be easy to follow on similar OS, that follow the [Unix filesystem](https://en.wikipedia.org/wiki/Unix_filesystem) convention, provided that `git` is installed:

* On Linux systems, use your package manager to install; say, on Ubuntu, you can just type `git` in a terminal, and it will remind you to `sudo apt-get install git` if not already installed
* MacOS/OSX systems also follow the Unix filesystem convention, and similarly, you can open [Terminal.app](https://www.macworld.co.uk/feature/mac-software/how-use-terminal-on-mac-3608274/) and just type `git`, and you will be prompted to install [Command Line Developer Tools](https://www.macissues.com/2014/05/26/what-are-the-command-line-developer-tools-in-os-x/) that also contain `git`
    * Note that both MacOS/OSX and Ubuntu, provide a command line intepreter (a.k.a. _shell_) called [`bash`](https://en.wikipedia.org/wiki/Bash_(Unix_shell))
* For Windows, you can install [Git for Windows](https://git-scm.com/download/win), which will install a "Git Bash" program, which will then also provide the same `bash` shell (and an emulation of an Unix filesystem) with a `git` command, as under GNU/Linux or MacOS/OSX

-----

This tutorial will operate in the temporary `/tmp` directory of the filesystem; and will be illustrated by screenshots, taken on Ubuntu 14.04 (see the Python script [`pyvirtdisp-starter.py`](pyvirtdisp-starter.py) in this repo for more) - where each related `git` directory will have its own terminal (here, `gnome-terminal`), own file manager (here, `pcmanfm`), and own Git GUI client (here, `giggle`; for more, see [Git - GUI Clients](https://git-scm.com/downloads/guis)).

The tutorial will start with creating a "main" `git` project directory, which will simulate online repositories, such as those found on GitHub or other services. Then, it will illustrate how two users, [Alice and Bob](https://en.wikipedia.org/wiki/Alice_and_Bob), work in their respective copies of the "main" repositories, and update (or synchronize) the "main" repository with their own changes.

-----

## The "main" repository - initializing

First, fire up a terminal, and let's create a directory under `/tmp` called `main` - type (or copy/paste) the following line at the terminal prompt (usually ending with dollar sign `$`), and press ENTER (Note that `mkdir` is a `bash` command):

    mkdir /tmp/main

scrshot_001.png

We should be presented with no other messages, and another prompt - meaning the operation succeeded:

scrshot_002.png

We can now switch to this newly created directory in the terminal, by executing the `bash` command for "change directory", `cd`:

    cd /tmp/main

We should be presented with no other messages, just another prompt (although the prompt might indicate the new current directory):

scrshot_003

Now, let's create a new directory for what will become the "main" `git` repository - let's call it `TheProject.git`. We could run `mkdir /tmp/main/TheProject.git` (that is, by specifying an [absolute path](https://en.wikipedia.org/wiki/Path_(computing)#Absolute_and_relative_paths)) - however, now that we're already in `/tmp/main` as our current working directory, we might as well just run:

    mkdir TheProject.git

scrshot_004

... and then we can change to `TheProject.git` with:

    cd TheProject.git

scrshot_005

Now that we're in the `/tmp/main/TheProject.git` directory, which is otherwise empty, we can finally initialize it as a `git` repository, by running the command `git init`:

    git init

scrshot_006

Note that we get a response to this command in the terminal this time:

    Initialized empty Git repository in /tmp/main/TheProject.git/.git/

However, note also, that our file manager still shows the `TheProject.git` folder as empty - but if we turn on showing of hidden files (on Windows, see [Show hidden files](https://support.microsoft.com/en-us/help/14201/windows-show-hidden-files); on macOS, use [CMD-Shift-. (dot)](https://www.macworld.co.uk/how-to/mac-software/how-show-hidden-files-library-folder-mac-3520878/); on Ubuntu GNU/Linux, Ctrl-H), we'll see something else:

scrshot_007

There is now a `.git` subfolder in the `TheProject.git` folder - hidden by default on Unix filesystems, since its name starts with a `.` (dot). It contains different subfolders, such as `branches`, `hooks`, `objects`, `refs` etc. - we won't go into details, but it is here that the commit history of the project will be saved.

However, in typical working use, we usually do not need to concern ourselves with the details of the contents in the `.git` subfolder - which is why it is by default named in such a way to be hidden, so it "gets out of the way". In the terminal, we can confirm the same by calling the Unix listing command, `ls`:

scrshot_008

Note that the first time we call `ls`, we simply get nothing listed (we get the prompt back again); however if we call `ls -la`, which lists hidden files, we do get the `.git` subfolder listed:

    user@PC:/tmp/main/TheProject.git$ ls
    user@PC:/tmp/main/TheProject.git$ ls -la
    total 12
    drwxrwxr-x 3 user user 4096 Dec 21 03:21 .
    drwxrwxr-x 3 user user 4096 Dec 21 03:07 ..
    drwxrwxr-x 7 user user 4096 Dec 21 03:21 .git

Now that we're aware of this, we can go back to hiding/ignoring the `.git` subfolder for the rest of the tutorial. We're now ready to add our first commit to this repository.



