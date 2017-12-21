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

r1/scrshot_001.png

We should be presented with no other messages, and another prompt - meaning the operation succeeded:

r1/scrshot_002.png

We can now switch to this newly created directory in the terminal, by executing the `bash` command for "change directory", `cd`:

    cd /tmp/main

We should be presented with no other messages, just another prompt (although the prompt might indicate the new current directory):

r1/scrshot_003

Now, let's create a new directory for what will become the "main" `git` repository - let's call it `TheProject.git`. We could run `mkdir /tmp/main/TheProject.git` (that is, by specifying an [absolute path](https://en.wikipedia.org/wiki/Path_(computing)#Absolute_and_relative_paths)) - however, now that we're already in `/tmp/main` as our current working directory, we might as well just run:

    mkdir TheProject.git

r1/scrshot_004

... and then we can change to `TheProject.git` with:

    cd TheProject.git

r1/scrshot_005

Now that we're in the `/tmp/main/TheProject.git` directory, which is otherwise empty, we can finally initialize it as a `git` repository, by running the command `git init`:

    git init

r1/scrshot_006

Note that we get a response to this command in the terminal this time:

    Initialized empty Git repository in /tmp/main/TheProject.git/.git/

However, note also, that our file manager still shows the `TheProject.git` folder as empty - but if we turn on showing of hidden files (on Windows, see [Show hidden files](https://support.microsoft.com/en-us/help/14201/windows-show-hidden-files); on macOS, use [CMD-Shift-. (dot)](https://www.macworld.co.uk/how-to/mac-software/how-show-hidden-files-library-folder-mac-3520878/); on Ubuntu GNU/Linux, Ctrl-H), we'll see something else:

r1/scrshot_007

There is now a `.git` subfolder in the `TheProject.git` folder - hidden by default on Unix filesystems, since its name starts with a `.` (dot). It contains different subfolders, such as `branches`, `hooks`, `objects`, `refs` etc. - we won't go into details, but it is here that the commit history of the project will be saved.

However, in typical working use, we usually do not need to concern ourselves with the details of the contents in the `.git` subfolder - which is why it is by default named in such a way to be hidden, so it "gets out of the way". In the terminal, we can confirm the same by calling the Unix listing command, `ls`:

r1/scrshot_008

Note that the first time we call `ls`, we simply get nothing listed (we get the prompt back again); however if we call `ls -la`, which lists hidden files, we do get the `.git` subfolder listed:

    user@PC:/tmp/main/TheProject.git$ ls
    user@PC:/tmp/main/TheProject.git$ ls -la
    total 12
    drwxrwxr-x 3 user user 4096 Dec 21 03:21 .
    drwxrwxr-x 3 user user 4096 Dec 21 03:07 ..
    drwxrwxr-x 7 user user 4096 Dec 21 03:21 .git

Now that we're aware of this, we can go back to hiding/ignoring the `.git` subfolder for the rest of the tutorial. We're now ready to add our first commit to this repository.

* Note: the naming convention, of naming a `git` repository folder with the extension `[FOLDERNAME].git`, is specific to a so-called "bare" `git` repository, intended for [hosting on a server](https://git-scm.com/book/en/v2/Git-on-the-Server-Getting-Git-on-a-Server). A bare repository typically does not contain a working directory, it simply contains all the files that we see inside the `.git` subfolder; here however, we use that naming convention with a non-bare repository, simply to emulate the server context.

-----

## The "main" repository - first commit

At this point, since our "main" repository is initialized as a Git project, we can also open the directory `/tmp/main/TheProject.git` in the Git GUI client:

r2/scrshot_001

... and we will not get any errors - however, since we have no commits nor content, nothing will be shown in the Git GUI client.

Here, let's first create a file with text content inside the `/tmp/main/TheProject.git` directory. We could do it in a GUI manner - first by right-clicking in the file manager, then choosing Create New / Empty File (or whatever the corresponding action may be in a different file manager), and then opening that empty file in a text editor, writing some text, and saving the file.

However, we can also use the `bash` command line to both create a file, and populate it with text content, in one go - using the [`echo` command](http://www.linfo.org/echo.html) and the [redirection](https://www.gnu.org/software/bash/manual/html_node/Redirections.html) operator `>` ("greater-than" sign/symbol) of `bash`. Let's create a file called `README.md` with a single line of text:

    echo "This is my first line" > README.md

The terminal again responds with no messages and just a prompt, indicating the command completed succesfully:

r2/scrshot_003 (skip 2, bad)

Note that at this point, the file manager does recognize and shows the `README.md` file automatically - while the Git GUI client might have to have its "refresh" button clicked first, but it still shows the new file greyed out. That is due to the file not being "tracked" by git, even if it does now exist in the project directory.

In order to start tracking the history of this file in the `git` project: execute the `git add` command, with the `README.md` filename as argument:

    git add README.md

r2/scrshot_004

Again, the terminal responds with nothing but a prompt, as a sign of succesfully executed command. Also, after being refreshed (after the `git add` command is ran), the Git GUI client now shows the file without it being greyed out - meaning that this file is now tracked in `git` history. Thus, the Git GUI client shows us the status and state of the `git` project - while a file manager typically does not show this status (although, there may be plugins that add that functionality).

At this point, it is proper to check the status of the `git` project, by running `git status`:

r2/scrshot_005

* Note: Since the screenshot is too small to show the entire terminal log, in this code snippet (and others), both the `bash` command, and its output, are shown - to make a difference between them, the prompt (up to its end `$`) is also added. If you're copy/pasting such commands in your terminal, make sure you copy the command line (e.g. `git status`) _excluding_ the prompt prefix (up to, and including, `$ `) as a single line.
* On those code snippets where there is no prompt, each line represents one command (line).

    user@PC:/tmp/main/TheProject.git$ git status
    On branch master

    Initial commit

    Changes to be committed:
      (use "git rm --cached <file>..." to unstage)

      new file:   README.md

With this, `git` informs us of several things. First, in the `/tmp/main/TheProject.git` directory, we're currently "in" the `git` branch "master"; "master" is the default autogenerated name for the default branch in `git` (we'll discuss branching in more detail later on). Then, `git` informs us we're about to perform the initial commit, which will contain one newly added file, `README.md`.

We can proceed with committing this change by using `git commit -m "MESSAGE"` (note that `git` requires a descriptive message for every commit):

    user@PC:/tmp/main/TheProject.git$ git commit -m "this is my initial commit"

    *** Please tell me who you are.

    Run

      git config --global user.email "you@example.com"
      git config --global user.name "Your Name"

    to set your account's default identity.
    Omit --global to set the identity only in this repository.

    fatal: unable to auto-detect email address (got 'user@PC.(none)')

Wait, what's this?! At this moment, `git` will simply not let us commit, because it does not know our identity! Therefore, we must populate the `git` configuration options `user.email` and `user.name`, before we can commit.

Note that we can set `user.email` and `user.name` to whatever we want - they are not bound to the current username as seen by the OS, nor authentication/login credentials on hosting sites like GitHub. Also, as the message points out, we should not use `--global`, so we can set the identity for each `git` project folder separately. Since this repo emulates a "main" server one, let's call this `git` identity `mainsrv`:

    git config user.name "mainsrv"
    git config user.email "mainsrv@example.com"

After the identity for this `git` repo is specified, repeating the `git commit` now succeeds, with a message:

    user@PC:/tmp/main/TheProject.git$ git commit -m "this is my initial commit"
    [master (root-commit) e9fe842] this is my initial commit
     1 file changed, 1 insertion(+)
     create mode 100644 README.md
    user@PC:/tmp/main/TheProject.git$

At this time, we can also refresh the Git GUI client, and observe that it starts listing history of this `git` project - just a single entry for now, identified by the commit message ("this is my initial commit"):

r2/scrshot_006

In the `giggle` Git GUI client, selecting the project folder entry will show no contents in the window, and the history entries for the entire repository - but if we select the file entry for `README.md`, then also its text contents will be shown, as well as a slice of the history relevant to this file:

r2/scrshot_007

At this point, let's see what the `git` status is:

    user@PC:/tmp/main/TheProject.git$ git status
    On branch master
    nothing to commit, working directory clean

As the message notes, all looks good, for the time bieng.


## A bit on Markdown and text editors

Note that the file we added, `README.md`, has an extension `.md` - this, by convention, is a file extension assigned to plain-text files, which are written with [Markdown](https://en.wikipedia.org/wiki/Markdown) formatting/markup.

As a markup language, Markdown is significantly easier to write than, say, HTML or LaTeX; however, also the text formatting effects that can be achieved are few (fewer than HTML or LaTeX). Markdown is typically converted or "rendered" to HTML, so that the formatting becomes visible to the user.

In a context of strictly local use, like in this tutorial, `.md` files are generally not different than normal plain-text `.txt` files - that is, if we open them in a plain-text editor, all we'll see is plain text (written according to Markdown conventions); if we open them in a specialized desktop Markdown editor, like [ReText](https://github.com/retext-project/retext) (among [many others](https://itsfoss.com/best-markdown-editors-linux/)), then might see formatted HTML text (in addition to the plain text source).

If you want to play with Markdown, you can look up sites which offer "live preview", such as:

* [Online Markdown Editor - Dillinger.io](https://dillinger.io/) - offers side-by-side live preview
* [stackoverflow.com](https://stackoverflow.com/) (or any of the [Stack Exchange](https://stackexchange.com/) sites) - simply open any question, scroll down to "Your Answer", and start typing in the text field - and you will get a live preview below the text field; there is also a handy [advanced help »](https://stackoverflow.com/editing-help) in this editor

We mention Markdown here, because most of the `git` online hosting provides, will by default parse `.md` files and show them as formatted HTML if they are chosen for browsing in their respective providers' web interfaces; in addition, `README.md` files are typically rendered even if only their containing directory is chosen for browsing (and not the `README.md` file explicitly). However, note that there may be differences in what kind of Markdown "flavour" each provider chooses to support:

* Bitbucket, for instance, uses the flavor [CommonMark (with a few extensions)](https://confluence.atlassian.com/bitbucketserver/markdown-syntax-guide-776639995.html), and supports no inline HTML whatsoever
* GitHub, for instance, supports the [GitHub Flavored Markdown Spec](https://github.github.com/gfm/), which allows inline HTML (for formatting Markdown itself cannot do)

Again, this support is specifically only for automatic rendering of files in online `git` projects at a particular provider; offline i.e. locally, an `.md` file is just a plain-text file. If you need a text editor for your OS (usually the built-in ones are rather limited), try:

* [Notepad++](https://notepad-plus-plus.org/download/) - Windows only
* [Geany](https://www.geany.org/) - cross-platform
* [Atom](https://atom.io/) - cross-platform


## A bit on Git history log, and commit hashes as labels

We can also use the `git log` command to check the history in this project:

    user@PC:/tmp/main/TheProject.git$ git log --summary
    commit e9fe8424108e74ffa240dcac90ec47ee242b72b0
    Author: mainsrv <mainsrv@example.com>
    Date:   Thu Dec 21 11:12:25 2017 +0100

        this is my initial commit

     create mode 100644 README.md

In this `git log` command, the `--summary` option causes the condensed information of file changes to be shown at bottom (the "`create mode 100644 README.md`"). Otherwise, by default, it will show commits, ordered newest to oldest. It also shows information about the commit, such as: who is the author, when (at which date/time) was the commit performed, as well as the commit message (the "this is my initial commit").

There is one more piece of information, which may be confusing at first, and that is the `git` [commit hash](https://git-scm.com/book/en/v2/Git-Basics-Viewing-the-Commit-History) - in this case, it is `e9fe8424108e74ffa240dcac90ec47ee242b72b0`. So, what do we need this for?

In principle, it would be easier to mark (or identify, or tag, or label) our commits with sequential numbers: for instance, this commit, as the initial commit, could be called revision "1"; then the next commit would become revision "2", then the next revision "3", - and so on. However, with `git` - as we shall see later - in principle, multiple users could start from a common point in history (say, the initial commit); and then, _simultaneously_, create their own versions of history by adding their own commits at random points in time. In that case, each of them would have revisions "2", "3", etc branching from the common revision "1", but which describe totally different commits.

Then, if _both_ of them want to synchronize their changes with the central ("main") repository, it would be impossible to consistently apply the sequential labelling approach: either revision "2" would refer to multiple different commits, thus becoming useless - or the central repository would have to re-label everything upon synchonization, in which case one commit would have different labels in the "main" vs. the user's own copy of repository; which would likewise be useless.

This is why `git` doesn't use sequential numbers for labelling - but instead [calculates](https://stackoverflow.com/questions/35430584/how-is-the-git-hash-calculated) a 160-bit [SHA-1](https://en.wikipedia.org/wiki/SHA-1) hash as a label. The idea behind this is that each and every commit will have a _unique_ label - regardless of when, and in which context, it was made. Since the input for the hash algorithm is the commit's content and timestamps, SHA-1 (almost) guarantees that the hash calculated will be unique (in other words, SHA-1 ensures there is a very, very low probability, that the same hash will be calculated for two different commits in the same repository - which is otherwise known as a "collision", and is the only case where the hash as a commit label becomes useless).

Note there are also special commit labels in `git`, such as `HEAD`, which typically refers to the latest commit in a repository (whatever the SHA-1 hash that commit might already have).


## The "main" repository - a bit on resetting staging, and second commit

Just for the sake of discussion, let's add another commit to the "main" repository. But before that, let's first add a file in the project's directory, which we do *not* intend to track with `git`, let's call it `whatever.txt`:

    echo "whatever" > whatever.txt

r2/scrshot_008

Note that at this point, the file manager recognizes `whatever.txt` as the same file of type as `README.md` - while the Git GUI manager (after a refresh) shows the `README.md` in full contrast, since it is tracked by `git`; while `whatever.txt` is greyed out, as it is not tracked.

Before we proceed, let's add some changes to `README.md` - again, we _could_ use a normal plain-text editor to make and save our changes to this file; however, we will again use the command line instead, this time with the `bash` operator `>>` for appending redirected output:

    echo "Added my second line" >> README.md

r2/scrshot_009

At this point, the file manager won't show anything new by itself - however, the Git GUI client (after a refresh) will show a small plus `+` next to the `README.md` entry - indicating that there have been changes made to this file; however, it still shows the old (or the latest committed) state of `README.md` as text (that is, only the first line of text is shown).

Here, let's check the `git` status:

    user@PC:/tmp/main/TheProject.git$ git status
    On branch master
    Changes not staged for commit:
      (use "git add <file>..." to update what will be committed)
      (use "git checkout -- <file>..." to discard changes in working directory)

      modified:   README.md

    Untracked files:
      (use "git add <file>..." to include in what will be committed)

      whatever.txt

    no changes added to commit (use "git add" and/or "git commit -a")


With this, `git` lets us know that it sees:

* one untracked file, `whatever.txt` - which can start being tracked with `git add`
* one tracked file, `README.md`, with changes in it, that are not yet staged for committing - these changes can be staged for a commit (again) with `git add`

Let's say that at this time, we do not intend to put (track) the `whatever.txt` in the Git repository at all, and we'll just keep it in the same directory; that means the second commit will only consist of changes to `README.md`. Let's stage these changes with `git add`:

    git add README.md

The status now becomes:

    user@PC:/tmp/main/TheProject.git$ git status
    On branch master
    Changes to be committed:
      (use "git reset HEAD <file>..." to unstage)

      modified:   README.md

    Untracked files:
      (use "git add <file>..." to include in what will be committed)

      whatever.txt

Note that at this point, the Git GUI client (after refresh), will not show the small `+` at the `README.md` icon anymore.

We're now ready to commit - but before we do so, let's note something: to record our changes, first we do `git add`, and only after that, can we do `git commit`; one may wonder, why do we need two commands for a single action of recording to history? The short answer is - because we might change our mind, and decide anyway not to include some changes in the commit. To facilitate this, `git` introduces the concept of a "staging area"; in brief:

* There is content/changes in untracked files, and unstaged content/changes in tracked files - these are changes that `git` doesn't *really* "know" about, *yet* (i.e. unstaged changes)
* There is the *staging area* - content/changes in tracked files that `git` "knows about", but are not *yet* part of history (i.e. staged changes)
* There are changes of content in tracked files that *are* part of commits, and as such, part of the "official" history of a given `git` project (i.e. committed changes)

... and thus, the `git` commands can be understood as:

* `git add` moves changes of content from "unknown" - to the "staging area"
* `git commit` moves changes of content from the "staging area" - to an actual *commit* in history

The idea is, once a commit has been made in history, it should be immutable/unchangeable (otherwise, in case of multiple collaborators which could rewrite history anytime at will, the whole concept of file change history loses meaning). The staging area thus allows us to review, and make sure whether we *really* want a given set of changes included in a commit or not.

>> As an **example**: let's say we arrive at a state, where in the staging area, we have two files with changes scheduled for committing: `filemath.c` and `documentation.txt`. In principle, we could do a `git commit` right here; but on the other hand, we might at this point decide that we'd want changes related to math, and changes related to documentation, in separate commits.
>>
>> Thus, we can follow what the `git` message "`use "git reset HEAD <file>..." to unstage`" says, and do `git reset HEAD documentation.txt`, which will unstage the changes in `documentation.txt` (i.e. move these changes from the "staging area" back to "unknown"). So, we can now do `git commit` and only changes related to math (i.e. `filemath.c`) will be recorded as a commit in history; then we can do again `git add documentation.txt`, followed by `git commit`, and only the changes related to `documentation.txt` will be recorded as a commit in history.

Let's give that a try: currently, `README.md` is in the "staging area"; let's unstage it using `git reset`, and then check the status:

    user@PC:/tmp/main/TheProject.git$ git reset HEAD README.md
    Unstaged changes after reset:
    M	README.md

    user@PC:/tmp/main/TheProject.git$ git status
    On branch master
    Changes not staged for commit:
      (use "git add <file>..." to update what will be committed)
      (use "git checkout -- <file>..." to discard changes in working directory)

      modified:   README.md

    Untracked files:
      (use "git add <file>..." to include in what will be committed)

      whatever.txt

    no changes added to commit (use "git add" and/or "git commit -a")

Note that `git reset` simply moved the changes from "staged" to "unstaged" - however, the changes (here, the second line of text), are *still* in the file `README.md`, they are not lost! So, basically, we're back at the state we were in, before we did `git add`.

Now, let's say we decide to commit the changes in `README.md` anyways - then we should simply `git add` those changes again (so they become "staged"), and subsequently do a `git commit`:

    user@PC:/tmp/main/TheProject.git$ git add README.md
    user@PC:/tmp/main/TheProject.git$ git commit -m 'here is the second commit'
    [master f183325] here is the second commit
     1 file changed, 1 insertion(+)
    user@PC:/tmp/main/TheProject.git$

r2/scrshot_010

At this point, note that: what the file manager displays, hasn't really changed; however, the Git GUI client (after refresh), now shows both lines of the text in `README.md`, and also shows two entries in the history graph - as we'd expect. As a wrap up, let's just check the status, and the history log, of this repo from the command line -- note that `git log --oneline` gives a much more reduced and compact view of the history log than what we've seen previously:

    user@PC:/tmp/main/TheProject.git$ git status
    On branch master
    Untracked files:
      (use "git add <file>..." to include in what will be committed)

      whatever.txt

    nothing added to commit but untracked files present (use "git add" to track)
    user@PC:/tmp/main/TheProject.git$ git log --oneline
    f183325 here is the second commit
    e9fe842 this is my initial commit

Note that in `git log --oneline`, we get shortened/truncated SHA-1 hashes as labels for the commits. All seems good so far - we can now proceed to examine, how would other users work with this repository.


-----

## Alice and Bob start - cloning and remotes

Now, let's assume Alice and Bob want to work on the previously created repository. First of all, let us create separate folders for them, again under `/tmp`:

    mkdir /tmp/A
    mkdir /tmp/B

Of course, here it's just a matter of convenience for the tutorial, that all three folders (`main/`, `A/` and `B/`) are under the same parent `/tmp`. In general, these folders could be at completely different locations in the filesystem; or, if the "main" repo is online, they could all be on different computers.

In any case, each user (Alice or Bob), will first `cd` to their own directory, and then perform a `git` operation known as cloning, to retrieve a copy of the "main" repository for themselves - and then they're going to "sign" those copies (via `user.name` and `user.email` config options) respectively (since without identification, `git` won't let them commit, as we saw earlier).

So, Alice could do:

    user@PC:/tmp$ cd /tmp/A
    user@PC:/tmp/A$ git clone /tmp/main/TheProject.git
    Cloning into 'TheProject'...
    done.
    user@PC:/tmp/A$ cd TheProject
    user@PC:/tmp/A/TheProject$ git config user.name alice
    user@PC:/tmp/A/TheProject$ git config user.email alice@example.com


Note that here, `git` automatically deduced from the original repo folder name, `TheProject.git`, that the locally cloned copy should be called `TheProject` (without the `.git` extension).

Likewise, Bob could do:

    user@PC:/tmp$ cd /tmp/B
    user@PC:/tmp/B$ git clone /tmp/main/TheProject.git TheProject_git
    Cloning into 'TheProject_git'...
    done.
    user@PC:/tmp/B$ cd TheProject_git
    user@PC:/tmp/B/TheProject_git$ git config user.name bob
    user@PC:/tmp/B/TheProject_git$ git config user.email bob@example.com

Note that here, Bob explicitly specified to `git` the local repo folder name that the repository should be cloned into (that is, `TheProject_git`), by adding it after the main repo URL/path. In other words - you can, in principle, name the folder containing your local copy of a `git` project anything you want.

r2/scrshot_011

At this point, note that:

* After being cloned, both Bob's and Alice's local copies can be opened in the Git GUI client, - and each clone shows the same state, as the one shown for the "main" repo
* The clone operation did not copy untracked files in the "main" repo (actually, it copies the history commits, and then rebuilds the tracked files accordingly)

We should mention here also the concept of remotes. First, note that now both Alice and Bob can run `git config -l` in their respective repo directories, and obtain a list of all configuration options related to their repos - among others, their `user.` settings; and options related to remotes. For instance, Alice might run:

    user@PC:/tmp/A/TheProject$ git config -l
    ...
    remote.origin.url=/tmp/main/TheProject.git
    remote.origin.fetch=+refs/heads/*:refs/remotes/origin/*
    branch.master.remote=origin
    branch.master.merge=refs/heads/master
    user.name=alice
    user.email=alice@example.com
    user@PC:/tmp/A/TheProject$ git remote -v
    origin	/tmp/main/TheProject.git (fetch)
    origin	/tmp/main/TheProject.git (push)

The term "remotes" usually refers to remote servers, hosting (remote) `git` repositories. Here, both the `git config -l` and `git remote -v` commands, tell us that we have one "remote", with the name `origin`, pointing at the URL `/tmp/main/TheProject.git` - the path of the "main" repo - in Alice's local clone of the repo. At this point, Bob would obtain identical output (except for the differing `user.` settings).

Note that:

* `git` repositories can, in principle, have more than one remote - but that will be skipped in this tutorial
* For local filesystem clones on Linux, we were able to use just the absolute path `/tmp/main/TheProject.git` of the "main" repo as a URL - should this fail, we can prefix `file://` to the absolute path, in which case the terminal output during cloning will be slightly different (and more similar to what you'd see if you cloned from an online repository, hosted say on GitHub):

    $ git clone file:///tmp/main/TheProject.git
    Cloning into 'TheProject'...
    remote: Counting objects: 6, done.
    remote: Compressing objects: 100% (2/2), done.
    Receiving objects: 100% (6/6), done.
    remote: Total 6 (delta 0), reused 0 (delta 0)
    Checking connectivity... done.

* Remote URLs are correspondingly prefixed when we clone online repositories over the network, the most common protocols being `https://`, `ssh://` and `git://`

Finally, if we check the status and history log of the locally cloned copies, we'll see that we have the same commits as in the "main" repo - and that we're in branch `master`, like the "main" repo is; say, for Bob's case (Alice would get identical results):

    user@PC:/tmp/B/TheProject_git$ git log --oneline
    f183325 here is the second commit
    e9fe842 this is my initial commit
    user@PC:/tmp/B/TheProject_git$ git status
    On branch master
    Your branch is up-to-date with 'origin/master'.

    nothing to commit, working directory clean

From this point on, Alice and Bob can make changes in ther locally cloned repos, and commit changes to them - and their local changes can be synchronized back with the "main" repo through a `git` operation known as pushing.


