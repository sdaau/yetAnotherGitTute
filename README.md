# Yet another Git tutorial

This is a brief tutorial on the SCM ([Source Control or Source Code Management](https://en.wikipedia.org/wiki/Source_control_management)) - aka VCS (Version Control System) - software [`git`](https://en.wikipedia.org/wiki/Git). It will focus on an offline (local) demonstration of basic operations, as well as conflicts and resolving them.

Table of contents:

* [The "main" repository - initializing](#the-main-repository---initializing)
* [The "main" repository - first commit](#the-main-repository---first-commit)
* [A bit on Markdown and text editors](#a-bit-on-markdown-and-text-editors)
* [A bit on Git history log, and commit hashes as labels](#a-bit-on-git-history-log-and-commit-hashes-as-labels)
* [The "main" repository - a bit on resetting staging, and second commit](#the-main-repository---a-bit-on-resetting-staging-and-second-commit)
* [Alice and Bob start - cloning and remotes](#alice-and-bob-start---cloning-and-remotes)
* [Alice starts hacking - push](#alice-starts-hacking---push)
* [Bob starts hacking - push and pull and automerge abort and rebase](#bob-starts-hacking---push-and-pull-and-automerge-abort-and-rebase)
* [Alice keeps hacking - file content-level conflict, and mergetool resolution](#alice-keeps-hacking---file-content-level-conflict-and-mergetool-resolution)
* [Reset and checkout of "main" repo - moving through commit history](#reset-and-checkout-of-main-repo---moving-through-commit-history)
* [Multiple users with own branches](#multiple-users-with-own-branches)
* [Alice branches out](#alice-branches-out)
* [Bob branches out](#bob-branches-out)
* [Merging branches back to master - branch upstream tracking, octopus merge](#merging-branches-back-to-master---branch-upstream-tracking-octopus-merge)


Crudely speaking, SCM/VCS allows one to track history of changes of files in a directory - the user creates, modifies or deletes files inside this directory; and the user can choose, at any time, to record the current state of the files in history by _committing_ them, the recorded state being known as a _commit_.

As more commits are added to the history, an SCM/VCS allows that the exact state of a previous commit can be restored in the working directory - which is particularly useful in software coding; say, in cases when a bug has been introduced by a more recent change (which should otherwise introduce a new feature). Such a directory, with contents with tracked history, is typically referred to as a _project_ or a _repository_ (that is, "repo").

Before we get going, note that:

* Git/`git` is the name of the SCM/VCS system and software, with a homepage at https://git-scm.com/
* GitHub is the name of a company, which offers hosting services and tools for `git` projects, with a homepage at https://github.com/ (one among many others, such as SourceForge https://sourceforge.net/ GitLab https://gitlab.com/ Bitbucket https://bitbucket.org/ etc).

-----

This tutorial has been tested on git version 1.9.1 on Ubuntu 14.04, a GNU/Linux operating system (OS). As such, it should be easy to follow on similar OS, that follow the [Unix filesystem](https://en.wikipedia.org/wiki/Unix_filesystem) convention, provided that `git` is installed:

* On Linux systems, use your package manager to install; say, on Ubuntu, you can just type `git` in a terminal, and it will remind you to `sudo apt-get install git` if not already installed
* macOS/OSX systems also follow the Unix filesystem convention, and similarly, you can open [Terminal.app](https://www.macworld.co.uk/feature/mac-software/how-use-terminal-on-mac-3608274/) and just type `git`, and you will be prompted to install [Command Line Developer Tools](https://www.macissues.com/2014/05/26/what-are-the-command-line-developer-tools-in-os-x/) that also contain `git`
    * Note that both macOS/OSX and Ubuntu, provide a command line intepreter (a.k.a. _shell_) called [`bash`](https://en.wikipedia.org/wiki/Bash_(Unix_shell))
* For Windows, you can install [Git for Windows](https://git-scm.com/download/win), which will install a "Git Bash" program, which will then also provide the same `bash` shell (and an emulation of an Unix filesystem) with a `git` command, as under GNU/Linux or macOS/OSX

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

scrshot_003.png

Now, let's create a new directory for what will become the "main" `git` repository - let's call it `TheProject.git`. We could run `mkdir /tmp/main/TheProject.git` (that is, by specifying an [absolute path](https://en.wikipedia.org/wiki/Path_(computing)#Absolute_and_relative_paths)) - however, now that we're already in `/tmp/main` as our current working directory, we might as well just run:

    mkdir TheProject.git

scrshot_004.png

... and then we can change to `TheProject.git` with:

    cd TheProject.git

scrshot_005.png

Now that we're in the `/tmp/main/TheProject.git` directory, which is otherwise empty, we can finally initialize it as a `git` repository, by running the command `git init`:

    git init

scrshot_006.png

Note that we get a response to this command in the terminal this time:

    Initialized empty Git repository in /tmp/main/TheProject.git/.git/

However, note also, that our file manager still shows the `TheProject.git` folder as empty - but if we turn on showing of hidden files (on Windows, see [Show hidden files](https://support.microsoft.com/en-us/help/14201/windows-show-hidden-files); on macOS, use [CMD-Shift-. (dot)](https://www.macworld.co.uk/how-to/mac-software/how-show-hidden-files-library-folder-mac-3520878/); on Ubuntu GNU/Linux, Ctrl-H), we'll see something else:

scrshot_007.png

There is now a `.git` subfolder in the `TheProject.git` folder - hidden by default on Unix filesystems, since its name starts with a `.` (dot). It contains different subfolders, such as `branches`, `hooks`, `objects`, `refs` etc. - we won't go into details, but it is here that the commit history of the project will be saved.

However, in typical working use, we usually do not need to concern ourselves with the details of the contents in the `.git` subfolder - which is why it is by default named in such a way to be hidden, so it "gets out of the way". In the terminal, we can confirm the same by calling the Unix listing command, `ls`:

scrshot_008.png

Note that the first time we call `ls`, we simply get nothing listed (we get the prompt back again); however if we call `ls -la`, which lists hidden files, we do get the `.git` subfolder listed:

    user@PC:/tmp/main/TheProject.git$ ls
    user@PC:/tmp/main/TheProject.git$ ls -la
    total 12
    drwxrwxr-x 3 user user 4096 Dec 21 03:21 .
    drwxrwxr-x 3 user user 4096 Dec 21 03:07 ..
    drwxrwxr-x 7 user user 4096 Dec 21 03:21 .git

Now that we're aware of this, we can go back to hiding/ignoring the `.git` subfolder for the rest of the tutorial. The rest of the files in the project folder, that are normally visible, are known as "work tree" or "working directory". We're now ready to add our first commit to this repository.

* Note: the naming convention, of naming a `git` repository folder with the extension `[FOLDERNAME].git`, is specific to a so-called "bare" `git` repository, intended for [hosting on a server](https://git-scm.com/book/en/v2/Git-on-the-Server-Getting-Git-on-a-Server). A bare repository typically does not contain a working directory, it simply contains all the files that we see inside the `.git` subfolder; here however, we use that naming convention with a non-bare repository, simply to emulate the server context.

-----

## The "main" repository - first commit

At this point, since our "main" repository is initialized as a Git project, we can also open the directory `/tmp/main/TheProject.git` in the Git GUI client:

scrshot_009.png

... and we will not get any errors - however, since we have no commits nor content, nothing will be shown in the Git GUI client.

Here, let's first create a file with text content inside the `/tmp/main/TheProject.git` directory. We could do it in a GUI manner - first by right-clicking in the file manager, then choosing Create New / Empty File (or whatever the corresponding action may be in a different file manager), and then opening that empty file in a text editor, writing some text, and saving the file.

However, we can also use the `bash` command line to both create a file, and populate it with text content, in one go - using the [`echo` command](http://www.linfo.org/echo.html) and the [redirection](https://www.gnu.org/software/bash/manual/html_node/Redirections.html) operator `>` ("greater-than" sign/symbol) of `bash`. Let's create a file called `README.md` with a single line of text:

    echo "This is my first line" > README.md

The terminal again responds with no messages and just a prompt, indicating the command completed succesfully:

scrshot_011.png (skip scrshot_010, bad)

Note that at this point, the file manager does recognize and shows the `README.md` file automatically - while the Git GUI client might have to have its "refresh" button clicked first, but it still shows the new file greyed out. That is due to the file not being "tracked" by git, even if it does now exist in the project directory.

In order to start tracking the history of this file in the `git` project: execute the `git add` command, with the `README.md` filename as argument:

    git add README.md

scrshot_012.png

Again, the terminal responds with nothing but a prompt, as a sign of succesfully executed command. Also, after being refreshed (after the `git add` command is ran), the Git GUI client now shows the file without it being greyed out - meaning that this file is now tracked in `git` history. Thus, the Git GUI client shows us the status and state of the `git` project - while a file manager typically does not show this status (although, there may be plugins that add that functionality).

At this point, it is proper to check the status of the `git` project, by running `git status`:

scrshot_013.png

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

scrshot_014.png

In the `giggle` Git GUI client, selecting the project folder entry will show no contents in the window, and the history entries for the entire repository - but if we select the file entry for `README.md`, then also its text contents will be shown, as well as a slice of the history relevant to this file:

scrshot_015.png

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

scrshot_016.png

Note that at this point, the file manager recognizes `whatever.txt` as the same file of type as `README.md` - while the Git GUI manager (after a refresh) shows the `README.md` in full contrast, since it is tracked by `git`; while `whatever.txt` is greyed out, as it is not tracked.

Before we proceed, let's add some changes to `README.md` - again, we _could_ use a normal plain-text editor to make and save our changes to this file; however, we will again use the command line instead, this time with the `bash` operator `>>` for appending redirected output:

    echo "Added my second line" >> README.md

scrshot_017.png

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

We're now ready to commit - but before we do so, let's note something: to record our changes, first we do `git add`, and only after that, can we do `git commit`; one may wonder, why do we need two commands for a single action of recording to history? The short answer is - because we might change our mind, and decide anyway not to include some changes in the commit. To facilitate this, `git` introduces the concept of a "staging area" a.k.a ["index"](https://stackoverflow.com/questions/12138207/is-the-git-staging-area-just-an-index); in brief:

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

scrshot_018.png

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

scrshot_019.png

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

From this point on, Alice and Bob can make changes in ther locally cloned repos, and commit changes to them - and their local changes can later be synchronized back with the "main" repo, through a `git` operation known as pushing.


## Alice starts hacking - push

Here, let's assume Alice wants to create a new file, let's call it `afile.txt`, and add some text to it; that can be easily achieved with `echo`ing and redirection, as previously. Also, we saw previously, that once a file is created with the right content, it should be added to staging area with `git add`, and then committed with `git commit` and a message:

    user@PC:/tmp/A/TheProject$ echo "Initial line by Alice" >> afile.txt
    user@PC:/tmp/A/TheProject$ git add afile.txt
    user@PC:/tmp/A/TheProject$ git commit -m "afile.txt new file added"
    [master 8709a34] afile.txt new file added
     1 file changed, 1 insertion(+)
     create mode 100644 afile.txt

scrshot_020.png

Here, we can observe, that the file manager shows the new `afile.txt`; and the Git GUI client (after refresh) also shows this file, and the new commit in the history - however, we have to select the root directory of the `git` project (`/tmp/A/TheProject`) in order to see the whole history (otherwise, selecting the individual file nodes will show only those commits in history that are related to the respective file).

Let's now check the status - it is implied we did a `cd /tmp/A/TheProject` previously:

    user@PC:/tmp/A/TheProject$ git status
    On branch master
    Your branch is ahead of 'origin/master' by 1 commit.
      (use "git push" to publish your local commits)

    nothing to commit, working directory clean

The `git` program lets us now that we're now "ahead" of the remote repository we cloned from "by 1 commit". In order to synchronise Alice's local changes with the "main" remote repo, we need to issue `git push`:

    user@PC:/tmp/A/TheProject$ git push
    warning: push.default is unset; its implicit value is changing in
    Git 2.0 from 'matching' to 'simple'. To squelch this message
    and maintain the current behavior after the default changes, use:

      git config --global push.default matching

    To squelch this message and adopt the new behavior now, use:

      git config --global push.default simple

    When push.default is set to 'matching', git will push local branches
    to the remote branches that already exist with the same name.

    In Git 2.0, Git will default to the more conservative 'simple'
    behavior, which only pushes the current branch to the corresponding
    remote branch that 'git pull' uses to update the current branch.

    See 'git help config' and search for 'push.default' for further information.
    (the 'simple' mode was introduced in Git 1.7.11. Use the similar mode
    'current' instead of 'simple' if you sometimes use older versions of Git)

    Counting objects: 4, done.
    Delta compression using up to 4 threads.
    Compressing objects: 100% (2/2), done.
    Writing objects: 100% (3/3), 299 bytes | 0 bytes/s, done.
    Total 3 (delta 0), reused 0 (delta 0)
    remote: error: refusing to update checked out branch: refs/heads/master
    remote: error: By default, updating the current branch in a non-bare repository
    remote: error: is denied, because it will make the index and work tree inconsistent
    remote: error: with what you pushed, and will require 'git reset --hard' to match
    remote: error: the work tree to HEAD.
    remote: error:
    remote: error: You can set 'receive.denyCurrentBranch' configuration variable to
    remote: error: 'ignore' or 'warn' in the remote repository to allow pushing into
    remote: error: its current branch; however, this is not recommended unless you
    remote: error: arranged to update its work tree to match what you pushed in some
    remote: error: other way.
    remote: error:
    remote: error: To squelch this message and still keep the default behaviour, set
    remote: error: 'receive.denyCurrentBranch' configuration variable to 'refuse'.
    To /tmp/main/TheProject.git
     ! [remote rejected] master -> master (branch is currently checked out)
    error: failed to push some refs to '/tmp/main/TheProject.git'

Now the `git` program lets us know of several problems:

* `git push` in itself is not enough; the proper syntax for it is `git push which-remote what-branch`. Since here we have only one branch (`master`) and one remote (`origin`), it was easy to be misled, and to assume `git` would assume these as the default arguments for the push operation. However, this version of `git` (1.9) is a version where significant changes in behavior are planned for future versions, and therefore `git` refuses to make that assumption for us. Explicitly, we would have to say `git push origin master` (that is, "push the changes in local `master` branch, to the remote repo with URL specified by `origin`).
* The remote repo refuses to update, because it is a non-bare repository (one with both a `.git` subfolder for history, and actual files), and pushing to a non-bare repository "will make the index and work tree inconsistent".

So, first, instead of turning the "main" repo into a 'bare' one, let's go to the "main" repo (implying `cd /tmp/main/TheProject.git`) and set `receive.denyCurrentBranch` to `ignore`, so we emulate how an actual remote repository would behave:

    user@PC:/tmp/main/TheProject.git$ git config receive.denyCurrentBranch ignore

With this, our commits will still be pushed to the `.git` subfolder of the "main" repo, however, the work tree will remain in the old version as we left it, and so will not reflect these changes.

Now, we can go back to Alice's repo (implying `cd /tmp/A/TheProject`), and try to push again. First, let's try the command `git push --all`, which is sometimes described online as "push all local branches to the remote":

    user@PC:/tmp/A/TheProject$ git push --all
    Counting objects: 4, done.
    Delta compression using up to 4 threads.
    Compressing objects: 100% (2/2), done.
    Writing objects: 100% (3/3), 299 bytes | 0 bytes/s, done.
    Total 3 (delta 0), reused 0 (delta 0)
    To /tmp/main/TheProject.git
       f183325..8709a34  master -> master

This is the usual output of a succesfully completed `push` command, and thus our `git push --all` succeeded for now.

scrshot_021.png

Note that at this point, we can go back to the Git GUI client of the "main" repo, and even without refreshing, click the root node of the repository, and we will see Alice's commit show up in the history -- even if the file `afile.txt` itself is not in the work tree (and so is not shown in the Git GUI client either).


## Bob starts hacking - push and pull and automerge abort and rebase

Let's assume that while Alice was doing her hacking in the previous subsection, Bob was also doing his own hacks. Bob, however, decided to add some content to the `README.md` file, instead of creating a new file. Since last we left him, Bob had just cloned the repository, he proceeds immediately with changing this file.

As previously we had solved the issue of the "main" repo not being 'bare', here we can proceed with adding a line to the `README.md` using `bash` `echo` and redirection; then adding the changes to staging area with `git add`; committing the changes with `git commit`; and finally pushing the changes to "main" repo with `git push` - and we _might_ expect that all this will complete without problems:

    user@PC:/tmp/B/TheProject_git$ echo "bob adding a line here" >> README.md
    user@PC:/tmp/B/TheProject_git$ git add README.md
    user@PC:/tmp/B/TheProject_git$ git commit -m 'bob edited README.md'
    [master 689d651] bob edited README.md
     1 file changed, 1 insertion(+)
    user@PC:/tmp/B/TheProject_git$ git push --all
    To /tmp/main/TheProject.git
     ! [rejected]        master -> master (fetch first)
    error: failed to push some refs to '/tmp/main/TheProject.git'
    hint: Updates were rejected because the remote contains work that you do
    hint: not have locally. This is usually caused by another repository pushing
    hint: to the same ref. You may want to first integrate the remote changes
    hint: (e.g., 'git pull ...') before pushing again.
    hint: See the 'Note about fast-forwards' in 'git push --help' for details.

Well, not so fast. The problem is now, that while Bob was hacking, Alice had already pushed a commit to the `master` branch - which Bob does not have. And, since `git` isn't certain in how to handle this situation, it asks Bob to first get the new commits (those that Bob doesn't have) from the "main" repo, and resolve potential conflicts locally, - before Bob is allowed to push his own commits.

In this case, we'd use the command `git pull` (alternately, `git pull origin master` or `git pull --all`) to retrieve the latest (missing) commits from the "main" repo. However, if we enter:

    user@PC:/tmp/B/TheProject_git$ git pull --all

... we will immediately get a text file opened in a terminal text editor (like `nano`), saying:

    Merge branch 'master' of /tmp/main/TheProject

    # Please enter a commit message to explain why this merge is necessary,
    # especially if it merges an updated upstream into a topic branch.

What is happening here, is that `git` tried to automatically "merge" the states of the (remote) "main" repo, and the local repo of Bob; it managed to rectify the situation, but that means now it has to make an additional commit, and the message for that commit is now shown in a text editor so the user can edit it; once it is edited and saved and text editor exited (in `nano`, hit Ctrl-X to start exiting, then you will be prompted if you want to save the file, to which you can say Y or N, and then `nano` will exit, and the merge will be committed).

However, here we don't really have a need for a merge per se, since we know Alice in her commit edited different file than Bob. So, at this moment, we could try adding a number- or hash-sign `#` in front of the "Merge branch 'master' .. " message, so it is interpreted as a comment instead of a message - then `git` will notice there is no commit message, which is not allowed, and it will abort the commit; and so the full terminal log becomes:

    user@PC:/tmp/B/TheProject_git$ git pull --all
    Fetching origin
    remote: Counting objects: 4, done.
    remote: Compressing objects: 100% (2/2), done.
    remote: Total 3 (delta 0), reused 0 (delta 0)
    Unpacking objects: 100% (3/3), done.
    From /tmp/main/TheProject
       f183325..8709a34  master     -> origin/master
    error: Empty commit message.
    Not committing merge; use 'git commit' to complete the merge.

Let's check the current status:

    user@PC:/tmp/B/TheProject_git$ git status
    On branch master
    Your branch and 'origin/master' have diverged,
    and have 1 and 1 different commit each, respectively.
      (use "git pull" to merge the remote branch into yours)

    All conflicts fixed but you are still merging.
      (use "git commit" to conclude merge)

    Changes to be committed:

      new file:   afile.txt

Ideally, what we should have done in a case like this (had Bob been aware that a problem of this kind is ahead), is `git pull --rebase`, with which [your remote changes (C) will be applied before the local changes (D)](https://stackoverflow.com/questions/25430600/difference-between-git-pull-rebase-and-git-pull-ff-only). Let's try to undo the merge with [`git merge --abort`](https://stackoverflow.com/questions/11646107/you-have-not-concluded-your-merge-merge-head-exists):

    user@PC:/tmp/B/TheProject_git$ git merge --abort
    user@PC:/tmp/B/TheProject_git$ git status
    On branch master
    Your branch and 'origin/master' have diverged,
    and have 1 and 1 different commit each, respectively.
      (use "git pull" to merge the remote branch into yours)

    nothing to commit, working directory clean

Now we can try `git pull --rebase`:

    user@PC:/tmp/B/TheProject_git$ git pull --rebase
    First, rewinding head to replay your work on top of it...
    Applying: bob edited README.md
    user@PC:/tmp/B/TheProject_git$ git status
    On branch master
    Your branch is ahead of 'origin/master' by 1 commit.
      (use "git push" to publish your local commits)

    nothing to commit, working directory clean
    user@PC:/tmp/B/TheProject_git$ git log --oneline
    e69e8ec bob edited README.md
    8709a34 afile.txt new file added
    f183325 here is the second commit
    e9fe842 this is my initial commit

Ah, that's more like it - indeed, in this case (result of steps as outlined in the tutorial), there was really no need for an extra merge commit, as there was no real conflict, and now the history log looks fine. Or rather, there was no real conflict _per file_ (in terms of content/changes in a single file); the only conflict was the order of the commits as seen by `git`.

Also, if we refresh the Git GUI client at this time, we'll both see the exact same commits in history - and the `afile.txt` file visible in both the Git GUI client, and the file manager. All that remains for Bob, is to do a `git push`, so the "main" repo gets Bob's latest commits:

    user@PC:/tmp/B/TheProject_git$ git push
    warning: push.default is unset; its implicit value is changing in
    Git 2.0 from 'matching' to 'simple'. To squelch this message
    and maintain the current behavior after the default changes, use:

      git config --global push.default matching

    To squelch this message and adopt the new behavior now, use:

      git config --global push.default simple

    When push.default is set to 'matching', git will push local branches
    to the remote branches that already exist with the same name.

    In Git 2.0, Git will default to the more conservative 'simple'
    behavior, which only pushes the current branch to the corresponding
    remote branch that 'git pull' uses to update the current branch.

    See 'git help config' and search for 'push.default' for further information.
    (the 'simple' mode was introduced in Git 1.7.11. Use the similar mode
    'current' instead of 'simple' if you sometimes use older versions of Git)

    Counting objects: 5, done.
    Delta compression using up to 4 threads.
    Compressing objects: 100% (3/3), done.
    Writing objects: 100% (3/3), 338 bytes | 0 bytes/s, done.
    Total 3 (delta 0), reused 0 (delta 0)
    To /tmp/main/TheProject.git
       8709a34..e69e8ec  master -> master

Again, we got the warning about `push.default is unset`; so we should have used, as in the previous case, `git push --all`, or `git push origin master`; however, the push itself succeeded, which is visible in the Git GUI client of "main" repo (after refresh and re-clicking the root node):

scrshot_022.png

Conclusions:

* Everytime you open a `git` repository, which is in a clean state, with intent to work on it, issue a `git pull --all` first, to make sure you pull all the latest commits, that may have popped up in the meantime, and that you might be missing - before you do any actual work (changes to files).
* If you've already made some changes and committed, do a `git pull --rebase` first before you push, in case new commits have popped up while you were working (so that your commits are "replayed" "on top" of those new commits, and you can easily commit)


## Alice keeps hacking - file content-level conflict, and mergetool resolution

Previously, we concluded that every time a fresh round of work starts, one should do a `git pull --all`. However, let us assume that Alice was unaware that Bob too started working in the same repository, and so didn't deem it necessary to do a `git pull --all` at the start of this round. And this time the intention is to edit `README.md`, which Bob has already changed in a commit that Alice hasn't pulled yet; as such, this will definitely cause a file-level conflict.

So, last time we left Alice's repo, it was at revision "*8709a34 afile.txt new file added*", and since no new changes were pulled, Alices new changes will be over this version of the `README.md` file. Alice will simply add a new line to the file, and then do `git add` and commit:

    user@PC:/tmp/A/TheProject$ echo "alice adding a new line" >> README.md
    user@PC:/tmp/A/TheProject$ git status
    On branch master
    Your branch is up-to-date with 'origin/master'.

    Changes not staged for commit:
      (use "git add <file>..." to update what will be committed)
      (use "git checkout -- <file>..." to discard changes in working directory)

      modified:   README.md

    no changes added to commit (use "git add" and/or "git commit -a")
    user@PC:/tmp/A/TheProject$ git add README.md
    user@PC:/tmp/A/TheProject$ git commit -m 'alice change of README.md'
    [master 302855d] alice change of README.md
     1 file changed, 1 insertion(+)

So far, nothing seems controversial. It is always a good idea to check the state of the repository with `git status`, before making an add or a commit; however, in this case, since there was no pull at start, the repository is unaware of changes in the "main" repo, and so wrongly reports "_Your branch is up-to-date_" (which will reinforce the wrong impression that everything is fine).

The conflict will become apparent as soon as we, as Alice, attempt to push to the "main" repository:

    user@PC:/tmp/A/TheProject$ git push --all
    To /tmp/main/TheProject.git
     ! [rejected]        master -> master (fetch first)
    error: failed to push some refs to '/tmp/main/TheProject.git'
    hint: Updates were rejected because the remote contains work that you do
    hint: not have locally. This is usually caused by another repository pushing
    hint: to the same ref. You may want to first integrate the remote changes
    hint: (e.g., 'git pull ...') before pushing again.
    hint: See the 'Note about fast-forwards' in 'git push --help' for details.

Here is the first sign of conflict - there are commits in "main" repo that Alice is missing. Taught by the previous experience, we immediately try `git pull --rebase` (instead of other forms of pull):

    user@PC:/tmp/A/TheProject$ git pull --rebase
    remote: Counting objects: 5, done.
    remote: Compressing objects: 100% (3/3), done.
    remote: Total 3 (delta 0), reused 0 (delta 0)
    Unpacking objects: 100% (3/3), done.
    From /tmp/main/TheProject
       8709a34..e69e8ec  master     -> origin/master
    First, rewinding head to replay your work on top of it...
    Applying: alice change of README.md
    Using index info to reconstruct a base tree...
    M	README.md
    Falling back to patching base and 3-way merge...
    Auto-merging README.md
    CONFLICT (content): Merge conflict in README.md
    Failed to merge in the changes.
    Patch failed at 0001 alice change of README.md
    The copy of the patch that failed is found in:
       /tmp/A/TheProject/.git/rebase-apply/patch

    When you have resolved this problem, run "git rebase --continue".
    If you prefer to skip this patch, run "git rebase --skip" instead.
    To check out the original branch and stop rebasing, run "git rebase --abort".

So, even if now rebase first did "_rewinding head to replay your work on top of it_", there is still a file-level conflict, in terms of changes of content to be applied to the `README.md` file, which is reported by "_CONFLICT (content): Merge conflict in README.md_".

How can we resolve this conflict? It is actually possible to do it entirely from the command line (for example, see [here](http://perrymitchell.net/article/merging-and-unmerging-with-git/)) - however, it is also somewhat difficult. It is much easier to resolve content based conflicts using a GUI tool designed for that purpose. One of the tools available on Linux for that is [Meld](http://meldmerge.org/) (which also can be considered cross-platform, as there exist Windows and macOS builds).

To call `meld` properly in a case where we got a "CONFLICT (content)" in `git` repo, we should simply run this command in the repository's directory:

    git mergetool

Upon running this command, the user is prompted to confirm the choice of a merging tool to call next; `git` keeps a list of several such programs, among which is also `meld`. If there are no other tools than `meld` installed on the system, `git` will automatically choose it as a merging tool, and eventually prompt:

    user@PC:/tmp/A/TheProject$ git mergetool

    This message is displayed because 'merge.tool' is not configured.
    See 'git mergetool --tool-help' or 'git help config' for more details.
    'git mergetool' will now attempt to use one of the following tools:
    opendiff kdiff3 tkdiff xxdiff meld tortoisemerge gvimdiff diffuse diffmerge ecmerge p4merge araxis bc3 codecompare emerge vimdiff
    Merging:
    README.md

    Normal merge conflict for 'README.md':
      {local}: modified file
      {remote}: modified file
    Hit return to start merge resolution tool (meld):

Upon pressing RETURN, `meld` is started for the conflicted file, in this case `README.md`:

meldmerge01.png

This form of usage is known as a 3-way merge:

* The left window shows `*.LOCAL.*` in the filename, and shows the state of the `README.md` file at the last local commit
* The right window shows `*.REMOTE.*` in the filename, and shows the state of the `README.md` file at the last remote commit (that one we didn't have locally before, but which we just pulled)
* The center window shows the part of the file which is identical in both LOCAL and REMOTE versions (that is, the version of the file at the last common commit for both local and remote histories)

The trick here is to edit the text in the central window, so it includes both the local and the remote missing state, then save that file and exit meld - upon which, `git` will consider the conflict to have been solved.

In order to edit the text in the central window, we can either copy/paste text from the left/right windows into the central one - or even easier, we can left-click and Ctrl-left-click the arrows shown in meld, to insert the missing text. So, at this time, the only decision we need to make in order to resolve this conflict, is whether Bob's line goes first (and Alice's second), or if Alice's line goes first (and Bob's second).

If we want to keep the chronological order of changes, then Bob's ("LOCAL") line should go first, and thus the final state of the central window would look like this:

meldmerge02.png

Note that the visualisation slightly changed now, and we have an indication that the center window file has been changed, with a small "harddrive/arrow" icon left of the central address bar, and an asterisk `*` near the central filename in the title bar. At this point, make sure the center window is focused (i.e. the text caret is in it), then hit Ctrl-S to save, then close `meld` - upon which, the `git mergetool` command will exit too.

At this point, let us check the status:

    user@PC:/tmp/A/TheProject$ git status
    rebase in progress; onto e69e8ec
    You are currently rebasing branch 'master' on 'e69e8ec'.
      (all conflicts fixed: run "git rebase --continue")

    Changes to be committed:
      (use "git reset HEAD <file>..." to unstage)

      modified:   README.md

    Untracked files:
      (use "git add <file>..." to include in what will be committed)

      README.md.orig

If we now inspect `README.md`, we'll notice it has the same content as the central window we saved in `meld`. So, we consider all conflicts fixed, and we can run, as recommended, "git rebase --continue":

    user@PC:/tmp/A/TheProject$ git rebase --continue
    Applying: alice change of README.md

Let's re-check the status again:

    user@PC:/tmp/A/TheProject$ git status
    On branch master
    Your branch is ahead of 'origin/master' by 1 commit.
      (use "git push" to publish your local commits)

    Untracked files:
      (use "git add <file>..." to include in what will be committed)

      README.md.orig

    nothing added to commit but untracked files present (use "git add" to track)
    user@PC:/tmp/A/TheProject$ git log --oneline
    e0da4fb alice change of README.md
    e69e8ec bob edited README.md
    8709a34 afile.txt new file added
    f183325 here is the second commit
    e9fe842 this is my initial commit

We don't really need `README.md.orig` anymore, so we can delete it with the `bash` command `rm` - and then we can try to `git push --all` again:

    user@PC:/tmp/A/TheProject$ rm README.md.orig
    user@PC:/tmp/A/TheProject$ git push --all
    Counting objects: 5, done.
    Delta compression using up to 4 threads.
    Compressing objects: 100% (3/3), done.
    Writing objects: 100% (3/3), 353 bytes | 0 bytes/s, done.
    Total 3 (delta 0), reused 0 (delta 0)
    To /tmp/main/TheProject.git
       e69e8ec..e0da4fb  master -> master

Finally, the push completed fine, - and if we refresh the Git GUI client of "main" repo, we'll see these commits in its history as well (note that, in spite of this, the GUI client of "main" repo will still show the state of `README.md` from some commits ago where it has only two lines!):

scrshot_023.png


## Reset and checkout of "main" repo - moving through commit history

Notice that so far, we've used the "main" repo as if it was a 'bare' server repo, that is, we were pushing content (or rather, commits) in its history "from the outside" (that is, from other clones of the repo). However, it is *not* a bare repo, in the sense that it has a work tree (working directory) files, and a `.git` subfolder which actually contains the commits.

And since we didn't do anything special to address that, at this moment, the "main" repo shows the work tree files in a state from several commits ago, while it otherwise contains much newer commits in its history. How can we synchronise the work tree files with the latest commit? First of all, let's check its status and log:

    user@PC:/tmp/main/TheProject.git$ git status
    On branch master
    Changes to be committed:
      (use "git reset HEAD <file>..." to unstage)

      modified:   README.md
      deleted:    afile.txt

    Untracked files:
      (use "git add <file>..." to include in what will be committed)

      whatever.txt

    user@PC:/tmp/main/TheProject.git$ git log --oneline --decorate
    e0da4fb (HEAD, master) alice change of README.md
    e69e8ec bob edited README.md
    8709a34 afile.txt new file added
    f183325 here is the second commit
    e9fe842 this is my initial commit

Note that we used the `--decorate` option for `git log` in order to show where the HEAD of the repository points to, and it points to the latest commit in `master` branch (here: e0da4fb). On the other hand, `git` considers the old state of the files as _new_ changes to be committed!

To bring the work tree files in sync with the HEAD, we could for one take `git`s own advice to use "`git reset HEAD <file>...`" - but since that command would have to be repeated for each and every file, we can use the stronger version `git reset --hard HEAD` to bring all work tree files in sync with the state in the HEAD commit.

On the other hand, we can use a slightly different command: `git checkout HEAD` - what this does, is it takes the repository tracked files in the state at the HEAD commit from history, and copies them over the work tree files. However, this command will not work, if we have files in the staging area (i.e. "Changes to be committed:"), so at this time, `git checkout HEAD` would result only with:

    user@PC:/tmp/main/TheProject.git$ git checkout HEAD
    M	README.md
    D	afile.txt

... which is a notification that some file changes are staged, and the checkout won't really succeed - and indeed, the status is unchanged after running this command.

We might be tempted to use `git reset --hard HEAD` and be done with it in one go - and thankfully, assumming that we need the untracked `whatever.txt` there (just not committed in the repo), this command will not delete it. Let's give it a try:

    user@PC:/tmp/main/TheProject.git$ git reset --hard HEAD
    HEAD is now at e0da4fb alice change of README.md
    user@PC:/tmp/main/TheProject.git$ git status
    On branch master
    Untracked files:
      (use "git add <file>..." to include in what will be committed)

      whatever.txt

    nothing added to commit but untracked files present (use "git add" to track)
    user@PC:/tmp/main/TheProject.git$ git log --oneline --decorate
    e0da4fb (HEAD, master) alice change of README.md
    e69e8ec bob edited README.md
    8709a34 afile.txt new file added
    f183325 here is the second commit
    e9fe842 this is my initial commit

At this point, after a refresh, also the Git GUI for "main" repo will show the same state of the files (just make sure you select the latest commit in the history).

scrshot_024.png

Here, let's do a review:

* If we add a line to otherwise unchanged `README.md`, then it is considered changed, but "unstaged" by `git`
* If then we do `git add README.md`, it is considered changed and staged
* If then we do `git reset HEAD README.md`, the file goes back to being unstaged, but the changes (the new line) are still kept
* If then we do `git checkout -- README.md`, the changes are lost, since the file is overwritten with its last committed state (this only works for unstaged files).

Here is a command log, which demonstrates this on the Alice repo (simply to avoid messages about untracked files):

    $ git status
    On branch master
    Your branch is up-to-date with 'origin/master'.

    nothing to commit, working directory clean
    $ echo "test line" >> README.md
    $ git status
    On branch master
    Your branch is up-to-date with 'origin/master'.

    Changes not staged for commit:
      (use "git add <file>..." to update what will be committed)
      (use "git checkout -- <file>..." to discard changes in working directory)

      modified:   README.md

    no changes added to commit (use "git add" and/or "git commit -a")
    $ git add README.md
    $ git status
    On branch master
    Your branch is up-to-date with 'origin/master'.

    Changes to be committed:
      (use "git reset HEAD <file>..." to unstage)

      modified:   README.md
    $ git checkout -- README.md   # says nothing, but doesn't change state, since currently README.md is staged!
    $ git status                  # same as previous
    On branch master
    Your branch is up-to-date with 'origin/master'.

    Changes to be committed:
      (use "git reset HEAD <file>..." to unstage)

      modified:   README.md
    $ git reset HEAD README.md
    Unstaged changes after reset:
    M	README.md
    $ git status
    On branch master
    Your branch is up-to-date with 'origin/master'.

    Changes not staged for commit:
      (use "git add <file>..." to update what will be committed)
      (use "git checkout -- <file>..." to discard changes in working directory)

      modified:   README.md

    no changes added to commit (use "git add" and/or "git commit -a")
    $ git checkout -- README.md   # says nothing, but this time state is changed:
    $ git status                  # we're back to where we started:
    On branch master
    Your branch is up-to-date with 'origin/master'.

    nothing to commit, working directory clean

Having understood this difference between `git` checkout and reset, note that we can "move" through the history of a repo using a `git checkout HASH` command. What this means is, that after running this command, all of the files in the work tree of the repository will take up the state they have in the commit labeled as `HASH`. It is implied that no file changes can be staged while doing this.

Let's again see this on an example, again using the Alice repo. Note that we will use the `bash` command `cat` to show the contents of a file in terminal.

First, let's confirm that we're in a pristine state at the latest revision, HEAD, using status and log, then we "print" out the file to see what its contents are in this state:

    $ git status
    On branch master
    Your branch is up-to-date with 'origin/master'.

    nothing to commit, working directory clean
    $ git log --oneline --decorate
    e0da4fb (HEAD, origin/master, origin/HEAD, master) alice change of README.md
    e69e8ec bob edited README.md
    8709a34 afile.txt new file added
    f183325 here is the second commit
    e9fe842 this is my initial commit
    $ cat README.md
    This is my first line
    Added my second line
    bob adding a line here
    alice adding a new line

Now, let's checkout the revision "f183325 here is the second commit", and check the state as previously, using status, log and `cat`:

    $ git checkout f183325
    Note: checking out 'f183325'.

    You are in 'detached HEAD' state. You can look around, make experimental
    changes and commit them, and you can discard any commits you make in this
    state without impacting any branches by performing another checkout.

    If you want to create a new branch to retain commits you create, you may
    do so (now or later) by using -b with the checkout command again. Example:

      git checkout -b new_branch_name

    HEAD is now at f183325... here is the second commit
    $ git status
    HEAD detached at f183325
    nothing to commit, working directory clean
    $ git log --oneline --decorate
    f183325 (HEAD) here is the second commit
    e9fe842 this is my initial commit
    $ cat README.md
    This is my first line
    Added my second line

Note that here:

* By doing `git checkout HASH` of earlier revision labeled HASH, now HEAD "went down" and points at this earlier revision
* This is indicated by shortened number of entries in `git log`
* We're getting a note about a "'detached HEAD' state", which [means you are no longer on a branch, you have checked out a single commit in the history](https://stackoverflow.com/questions/10228760/fix-a-git-detached-head)
* The file contents indeed correspond to this earlier revision in history

So, since now HEAD moved, if we do `git checkout HEAD`, we will not change the state at all:

    $ git checkout HEAD
    $ git status
    HEAD detached at f183325
    nothing to commit, working directory clean

Thus, if we want to go back to the latest commit, we should do `git checkout master` (that is, use the branch name):

    $ git checkout master
    Previous HEAD position was f183325... here is the second commit
    Switched to branch 'master'
    Your branch is up-to-date with 'origin/master'.
    $ git status
    On branch master
    Your branch is up-to-date with 'origin/master'.

    nothing to commit, working directory clean
    $ git log --oneline --decorate
    e0da4fb (HEAD, origin/master, origin/HEAD, master) alice change of README.md
    e69e8ec bob edited README.md
    8709a34 afile.txt new file added
    f183325 here is the second commit
    e9fe842 this is my initial commit
    $ cat README.md
    This is my first line
    Added my second line
    bob adding a line here
    alice adding a new line

And so, we've confirmed we're back where we started.

These were some of the crucial `git` concepts and approaches, when dealing with multiple users working in a single branch (here, the default branch, `master`).

-----

## Multiple users with own branches

As the tutorial shows so far, it is very easy to end up dealing with conflicts, when working in a single branch (here the default, `master` branch), even if there are only two users pushing to the "main" (remote) repo. Clearly, noone would want to deal with stuff like conflicts daily.

In `git`, that friction can be somewhat reduced, by allowing each user to have their own, _separate_ branch. Basically, each user would start from a known commit in `master` branch, say HEAD - and then, from there, branch out to their own branch. Then, they can keep hacking the very same files (i.e. `README.md`) in their respective branches, and conflicts like the ones described previously, would not occur.

Of course, this also means that, in general, individual branches will not really "know" what goes on in other branches (and this goes for the default `master` branch too), unless a merge is performed. This also means that the contributions from all the users will not be in the same place (at the same branch).

So, in order to gather all the contributions in the same branch, typically a merge with the `master` branch is performed - the frequency of doing this, is a matter of agreement of the users of the repository. During such merges, we can again expect conflicts - however, if the merge is agreed upon by the users in advance, it is likely that the merging procedure may be less painful, than the conflict handling described so far in this tutorial for single branch use.

What commands can we use to operate with new branches? As noted in [Git - Basic Branching and Merging](https://git-scm.com/book/en/v2/Git-Branching-Basic-Branching-and-Merging), there exists:

* a `git branch newbranch` command, which creates a new branch with name "newbranch" - but this command simply creates the branch, it doesn't _switch_ to the new branch
* a `git checkout newbranch` command - we mentioned previously that `checkout` can be used to switch between commits, but it can be also used to switch to branches (here, it would switch to the branch named "newbranch")
* a shorthand for both of these commands would be `git checkout -b newbranch`

Let's now see how this would work with the repos of Alice and Bob; having learned from the experience so far, the first thing we'll have them do each, is to pull the latest commits from the "main" repo.


## Alice branches out

Let's start by having Alice pull from "main" repo (even if we expect Alice's repo to be in sync at this moment):

    user@PC:/tmp/A/TheProject$ git pull --all
    Fetching origin
    Already up-to-date.
    user@PC:/tmp/A/TheProject$ git log --oneline --decorate
    e0da4fb (HEAD, origin/master, origin/HEAD, master) alice change of README.md
    e69e8ec bob edited README.md
    8709a34 afile.txt new file added
    f183325 here is the second commit
    e9fe842 this is my initial commit

So, if Alice creates a new branch now, it will be "split off" from the last common revision with the `master` branch, which is here labeled with hash e0da4fb. So, let's have Alice create a new branch, `a-branch`, and switch to it:

    user@PC:/tmp/A/TheProject$ git checkout -b a-branch
    Switched to a new branch 'a-branch'
    user@PC:/tmp/A/TheProject$ git status
    On branch a-branch
    nothing to commit, working directory clean
    $ git log --oneline --decorate
    e0da4fb (HEAD, origin/master, origin/HEAD, master, a-branch) alice change of README.md
    e69e8ec bob edited README.md
    8709a34 afile.txt new file added
    f183325 here is the second commit
    e9fe842 this is my initial commit

Notice that after switching to the new branch, both status and log `--decorate`, report this branch in their outputs. So, let's have Alice change the `README.md`, and commit that change in this new branch:

    user@PC:/tmp/A/TheProject$ echo 'a-branch added line by alice' >> README.md
    user@PC:/tmp/A/TheProject$ git add README.md
    user@PC:/tmp/A/TheProject$ git commit -m 'a-branch change of README'
    [a-branch 6e26ae4] a-branch change of README
     1 file changed, 1 insertion(+)

Uncontroversial so far; let's see how the push to "main" will go:

    $ git push --all
    Counting objects: 5, done.
    Delta compression using up to 4 threads.
    Compressing objects: 100% (3/3), done.
    Writing objects: 100% (3/3), 338 bytes | 0 bytes/s, done.
    Total 3 (delta 1), reused 0 (delta 0)
    To /tmp/main/TheProject.git
     * [new branch]      a-branch -> a-branch
    $ git log --oneline --decorate --graph
    * 6e26ae4 (HEAD, origin/a-branch, a-branch) a-branch change of README
    * e0da4fb (origin/master, origin/HEAD, master) alice change of README.md
    * e69e8ec bob edited README.md
    * 8709a34 afile.txt new file added
    * f183325 here is the second commit
    * e9fe842 this is my initial commit

Note here that we've used `--graph` option for `git log`, which would "_draw a text-based graphical representation of the commit history on the left hand side_"; however, there aren't enough commits at the moment, to really make the graphical representation of branching obvious (it is just mere asterisks `*` on the left for the time being). Something similar is visible in the Git GUI client:

scrshot_025.png

Interestingly, note that after the push, the "main" repo still does not show the new `a-branch` in its `git log` terminal output - however, the Git GUI client shows it!

Well, that passed smoothly - let's see if Bob too will have such luck...


## Bob branches out

As previously, let's first start by having Bob pull from "main" repo:

    user@PC:/tmp/B/TheProject_git$ git pull --all
    Fetching origin
    remote: Counting objects: 8, done.
    remote: Compressing objects: 100% (6/6), done.
    remote: Total 6 (delta 1), reused 0 (delta 0)
    Unpacking objects: 100% (6/6), done.
    From /tmp/main/TheProject
       e69e8ec..e0da4fb  master     -> origin/master
     * [new branch]      a-branch   -> origin/a-branch
    Updating e69e8ec..e0da4fb
    Fast-forward
     README.md | 1 +
     1 file changed, 1 insertion(+)
    user@PC:/tmp/B/TheProject_git$ git log --oneline --decorate --graph
    * e0da4fb (HEAD, origin/master, origin/HEAD, master) alice change of README.md
    * e69e8ec bob edited README.md
    * 8709a34 afile.txt new file added
    * f183325 here is the second commit
    * e9fe842 this is my initial commit

Interestingly, while the pull did report that the new branch by Alice, `a-branch`, has been retrieved - it is _not_ reported in the `git log`; one reason could be, that we've not switched to `a-branch` yet.

So, if Bob creates a new branch now, it will be "split off" from the last common revision with the `master` branch, which is again here labeled with hash e0da4fb. So, let's have Bob create a new branch, `b-branch`, and switch to it:

    user@PC:/tmp/B/TheProject_git$ git checkout -b b-branch
    Switched to a new branch 'b-branch'
    user@PC:/tmp/B/TheProject_git$ git status
    On branch b-branch
    nothing to commit, working directory clean
    user@PC:/tmp/B/TheProject_git$ git log --oneline --decorate --graph
    * e0da4fb (HEAD, origin/master, origin/HEAD, master, b-branch) alice change of README.md
    * e69e8ec bob edited README.md
    * 8709a34 afile.txt new file added
    * f183325 here is the second commit
    * e9fe842 this is my initial commit

Notice that after switching to the new branch `b-branch`, both status and log `--decorate`, report this branch in their outputs - although, Alice's `a-branch` is still ignored in the log. So, let's have Bob change the `README.md`, and commit that change in this new `b-branch`:

    user@PC:/tmp/B/TheProject_git$ echo 'b-branch (bob) adding line to README' >> README.md
    user@PC:/tmp/B/TheProject_git$ git add README.md
    user@PC:/tmp/B/TheProject_git$ git commit -m 'b-branch (bob) README edit'
    [b-branch f9418cf] b-branch (bob) README edit
     1 file changed, 1 insertion(+)

Went fine so far; let's see how the push to "main" will go:

    user@PC:/tmp/B/TheProject_git$ git push --all
    Counting objects: 7, done.
    Delta compression using up to 4 threads.
    Compressing objects: 100% (3/3), done.
    Writing objects: 100% (3/3), 344 bytes | 0 bytes/s, done.
    Total 3 (delta 1), reused 0 (delta 0)
    To /tmp/main/TheProject.git
     * [new branch]      b-branch -> b-branch
    user@PC:/tmp/B/TheProject_git$ git log --oneline --decorate --graph --all
    * f9418cf (HEAD, origin/b-branch, b-branch) b-branch (bob) README edit
    | * 6e26ae4 (origin/a-branch) a-branch change of README
    |/
    * e0da4fb (origin/master, origin/HEAD, master) alice change of README.md
    * e69e8ec bob edited README.md
    * 8709a34 afile.txt new file added
    * f183325 here is the second commit
    * e9fe842 this is my initial commit

Note here that we've used `--all` option for `git log`, which we can interpret as "show all branches" - even if the `git help log` is somewhat cryptic about this option: "_Pretend as if all the refs in refs/ are listed on the command line as <commit>_". Regardless, it _does_ show both `a-branch` and `b-branch` now, and it _does_ show a (textual) graphical indication of branching. Something similar is visible in the Git GUI client (after refresh):

scrshot_026.png

Note that in the screenshot, the Git GUI clients are refreshed both for "main" and Bob's repos - and they indeed show the same history, also in respect to branches (while with `git log` from the command line, there are slight differences in naming: "main" might just refer to `a-branch`, while Bob's repo would refer to it as `origin/a-branch`.

Well, that was nice - both Alice and Bob edited the same `README.md` file, but in their own separate branches, and there were no conflicts whatsoever reported by `git`. However, now the `master` branch has neither of these contributions - and for the `master` branch to have them, we'll have to perform a manual merge.


## Merging branches back to master - branch upstream tracking, octopus merge

Recall that here we consider the "main" repo to be a stand-in (or simulation) for a remote (online) 'bare' repository. When we have a 'bare' repository, we typically cannot perform branching or merging from the command line (although, here we could, as "main" is not a 'bare' repo). So, in a typical context, it would be either Alice or Bob that would perform the merge of changes in the branches back to master.

Let's say Alice is going to perform the merge here. Again, the first thing to do is `git pull --all`, so we have the latest commits from "main":

    user@PC:/tmp/A/TheProject$ git pull --all
    Fetching origin
    remote: Counting objects: 7, done.
    remote: Compressing objects: 100% (3/3), done.
    remote: Total 3 (delta 1), reused 0 (delta 0)
    Unpacking objects: 100% (3/3), done.
    From /tmp/main/TheProject
     * [new branch]      b-branch   -> origin/b-branch
    You asked to pull from the remote '--all', but did not specify
    a branch. Because this is not the default configured remote
    for your current branch, you must specify a branch on the command line.

Ok, so apparently we did fetch all the latest commits, but here we have a new warning: "_You asked to pull from the remote '--all', but did not specify a branch..._".

In fact, it turns out, this is because of a naive (mis)understanding of how `git` push and pull operations work, which was assumed throughout this tutorial: which is that `git pull --all` is a symmetrically opposite operation from `git push --all` -- and it turns out, it is **not**. This is explained in [git - Pull all branches from origin - Stack Overflow](https://stackoverflow.com/questions/24151990/pull-all-branches-from-origin):

> I can say this: `git push --all origin` and it will push all branches to origin.
> But if I do this: `git pull --all origin` then it doesn't pull all the branches from origin, it just returns an error [...]
> Ok, I do this: `git pull --all` but yet it says: `You asked to pull from the remote '--all', but did not specify ...`
> So how do I pull all the branches from origin (like I push all branches to origin by `git push --all origin`)?
>
> In what I think is a very unfortunate bit of naming, git has `fetch`, `push`, and `pull`. It sounds like `pull` is the opposite-direction equivalent of `push`, but it's not! The closest thing `push` has to an opposite is actually `fetch` (and even then they're not entirely symmetric). ...
>  A "regular" or "local" branch name — usually just called "a branch" — like `master` has the special property that, when you check it out by branch name and then make new commits in your repository, that branch name _automatically moves forward_ to include your new commits. ...
> Git also provides "remote branches", which (in git tradition) have a somewhat misleading name since they also live in _your_ repository, not in some other "remote" repository. These are prefixed with the name of the remote, e.g., `origin`, so you have `origin/master` as a "remote branch". Again, these are just labels for commits. Unlilke your local branches, they don't move when you make commits — but they _do_ move. They move when you use `git fetch`. ...
> `git fetch` brings over all branches, just as `git push --all` pushes all branches. What `fetch` does _not_ do is _merge_ any of those updates into your own local branches. This is also where `fetch` and `push` stop being mirror-images of each other: _when you `push` a branch to a remote, there is no automatic renaming_. ...
> The `git pull` script simply automates the fetch-and-merge/rebase part. But it does this with _only one branch_: whatever branch we have checked out right now.
> If you want to merge-or-rebase multiple branches, you have to check each one out, one at a time. ...  Fortunately `git fetch origin` will update all the remote-branches at once, so you need only one `git fetch`.
> Git generally assumes that unless you plan to _change_ something in a branch, or freeze it at a particular commit, you don't check out your own version of it.
>
> `git pull` will first `git fetch` everything, meaning the `origin` namespace will include all (remote tracking) branches from `origin` ...
> But it will merge only `origin/currentBranch` to `currentBranch`.
> It won't create the other branches.
> If it were to create _all_ the branches from origin, your git branch would be "polluted" by the potentially many branches of the upstream repo.
> Generally, you only want as local branches the one you will be working on.

So, when we did `git pull --all` in Alice's repo, that command first called `git fetch`, which already _did_ get all remote commits locally; the warning occurs due to confusion in how to merge in those commits locally. In fact, here we assumed that `--all` argument refers to "all branches", but that is incorrect - in fact, it refers to "all remotes", as `git help pull` says:

> --all
>    Fetch all remotes.

Since in this tutorial we have only one remote (`origin`), it was pointless to use `--all` as argument to `git pull` altogether. However, if we just do `git pull` in Alice's repo at this time, we'll get:

    user@PC:/tmp/A/TheProject$ git pull
    There is no tracking information for the current branch.
    Please specify which branch you want to merge with.
    See git-pull(1) for details

        git pull <remote> <branch>

    If you wish to set tracking information for this branch you can do so with:

        git branch --set-upstream-to=origin/<branch> a-branch

    user@PC:/tmp/A/TheProject$ git status
    On branch a-branch
    nothing to commit, working directory clean

Since we get a complaint "There is no tracking information for the current branch", we'd want to know not just the list of local and remote branches (obtained with `git branch --all`), but [how do I get git to show me which branches are tracking what?](https://stackoverflow.com/questions/4950725/how-do-i-get-git-to-show-me-which-branches-are-tracking-what) - the answer being `git branch -vv`:

    user@PC:/tmp/A/TheProject$ git branch --all
    * a-branch
      master
      remotes/origin/HEAD -> origin/master
      remotes/origin/a-branch
      remotes/origin/b-branch
      remotes/origin/master
    user@PC:/tmp/A/TheProject$ git branch -vv
    * a-branch 6e26ae4 a-branch change of README
      master   e0da4fb [origin/master] alice change of README.md

So, indeed, currently `a-branch` is considered just to be a local branch, which does _not_ track the remote `origin/a-branch` branch - even if the local repository "knows" about this remote branch. Since the current status is "On branch a-branch ; nothing to commit, working directory clean", let's checkout (switch to) `master`, and then go back to (checkout) the `a-branch` branch:

    user@PC:/tmp/A/TheProject$ git checkout master
    Switched to branch 'master'
    Your branch is up-to-date with 'origin/master'.
    user@PC:/tmp/A/TheProject$ git checkout a-branch
    Switched to branch 'a-branch'
    user@PC:/tmp/A/TheProject$ git branch -vv
    * a-branch 6e26ae4 a-branch change of README
      master   e0da4fb [origin/master] alice change of README.md

Well, that didn't change anything. Note also that when we switched back to `a-branch` via checkout, we did _not_ get a message "Your branch is up-to-date with 'origin/..."!

So, the `a-branch` in Alice's repo likely does not track a remote branch at this time, because it was _created_ in Alice's repo to begin with, -- and as such, it was _never_ pulled from "main" repo as a _new_ branch (which would, then, have set up the tracking information automatically).

So, at this time, we might want to listen to the advice `git` gave us earlier, saying that "if you wish to set tracking information for this branch you can do so with":

    user@PC:/tmp/A/TheProject$ git branch --set-upstream-to=origin/a-branch a-branch
    Branch a-branch set up to track remote branch a-branch from origin.

Let's check the branch tracking info now:

    user@PC:/tmp/A/TheProject$ git branch -vv
    * a-branch 6e26ae4 [origin/a-branch] a-branch change of README
      master   e0da4fb [origin/master] alice change of README.md
    user@PC:/tmp/A/TheProject$ git checkout master
    Switched to branch 'master'
    Your branch is up-to-date with 'origin/master'.
    user@PC:/tmp/A/TheProject$ git checkout a-branch
    Switched to branch 'a-branch'
    Your branch is up-to-date with 'origin/a-branch'.

Ah - that's more like it; now we can see our local `a-branch` tracks the remote `origin/a-branch` - and indeed, when we check it out, now we can see the "Your branch is up-to-date with 'origin/a-branch'" message. So if we do a:

    user@PC:/tmp/A/TheProject$ git pull --all
    Fetching origin
    Already up-to-date.

... there is no warning anymore.

So let's get back to the topic now - which was merging the commits in `a-branch` and `b-branch` in the `master` branch.

[Typically](https://stackoverflow.com/questions/5601931/best-and-safest-way-to-merge-a-git-branch-into-master/#5602109), we'd have to checkout `master` branch, then while in master, run `git merge a-branch`, and then `git merge b-branch`; this will however result with two [separate commits](https://stackoverflow.com/questions/366860/when-would-you-use-the-different-git-merge-strategies/#366940). On the other hand, we could use the so-called "octopus" merge strategy in git, by calling `git merge a-branch b-branch`, which would result with a single commit; however it [refuses to do a complex merge that needs manual resolution](https://stackoverflow.com/questions/16208144/how-do-i-merge-multiple-branches-into-master/#16238928).

So, since in this example, both `a-branch` and `b-branch` changed `README.md`, we would expect a file-level content conflict that would have to be resolved manually - meaning, an "octopus" merge would fail. Still, let's give it a try - but first, we should make sure we have both `a-branch` and `b-branch` show up as local branches, so that we can merge them in (a nice way to check is to try `git merge b-` and then press TAB in terminal; if it autocompletes, the local branch is available):

    user@PC:/tmp/A/TheProject$ git status
    On branch a-branch
    Your branch is up-to-date with 'origin/a-branch'.

    nothing to commit, working directory clean
    user@PC:/tmp/A/TheProject$ git branch -vv
    * a-branch 6e26ae4 [origin/a-branch] a-branch change of README
      master   e0da4fb [origin/master] alice change of README.md
    user@PC:/tmp/A/TheProject$ git checkout b-branch
    Branch b-branch set up to track remote branch b-branch from origin.
    Switched to a new branch 'b-branch'
    user@PC:/tmp/A/TheProject$ git branch -vv
      a-branch 6e26ae4 [origin/a-branch] a-branch change of README
    * b-branch f9418cf [origin/b-branch] b-branch (bob) README edit
      master   e0da4fb [origin/master] alice change of README.md

Nice - by checking out `b-branch`, we now have it as a local branch. Now, let's checkout `master`, and try to do an "octopus" merge with both `a-branch` and `b-branch`:

    user@PC:/tmp/A/TheProject$ git checkout master
    Switched to branch 'master'
    Your branch is up-to-date with 'origin/master'.
    user@PC:/tmp/A/TheProject$ git merge a-branch b-branch
    Fast-forwarding to: a-branch
    Trying simple merge with b-branch
    Simple merge did not work, trying automatic merge.
    Auto-merging README.md
    ERROR: content conflict in README.md
    fatal: merge program failed
    Automatic merge failed; fix conflicts and then commit the result.
    user@PC:/tmp/A/TheProject$ git status
    On branch master
    Your branch is up-to-date with 'origin/master'.

    You have unmerged paths.
      (fix conflicts and run "git commit")

    Unmerged paths:
      (use "git add <file>..." to mark resolution)

      both modified:      README.md

    no changes added to commit (use "git add" and/or "git commit -a")
    user@PC:/tmp/A/TheProject$ git mergetool

    This message is displayed because 'merge.tool' is not configured.
    See 'git mergetool --tool-help' or 'git help config' for more details.
    'git mergetool' will now attempt to use one of the following tools:
    opendiff kdiff3 tkdiff xxdiff meld tortoisemerge gvimdiff diffuse diffmerge ecmerge p4merge araxis bc3 codecompare emerge vimdiff
    Merging:
    README.md

    Normal merge conflict for 'README.md':
      {local}: modified file
      {remote}: modified file
    Hit return to start merge resolution tool (meld):

Well, since the first of the branches, `a-branch`,  was easy to merge without intervention (that is, it "fast-forwarded"), we only had a single conflict when thereafter trying to merge `b-branch`; and so the repository allowed us to resolve the confict manually with `git mergetool` - that is, using `meld`, as we used it previously. Again, we have a "3-way merge" situation, similar to previously:

meldmerge03.png

And similarly, if we want to resolve the conflict chronologically, first we'll add the content from Alice, and then from Bob:

meldmerge04.png

Again, once we're done putting in lines of text content, we focus on the center window in, Ctrl-S to save, then close `meld` to have the `git mergetool` command exit - and so the status becomes:

    user@PC:/tmp/A/TheProject$ git status
    On branch master
    Your branch is up-to-date with 'origin/master'.

    All conflicts fixed but you are still merging.
      (use "git commit" to conclude merge)

    Changes to be committed:

      modified:   README.md

    Untracked files:
      (use "git add <file>..." to include in what will be committed)

      README.md.orig

Here, let's try just `git commit` as `git` itself recommends (and then we can delete `README.md.orig` as we won't need it):

    user@PC:/tmp/A/TheProject$ git commit

Here a text editor is started (on Ubuntu, `nano` is started in the terminal), so as to provide us with the default merging commit message, and give us a chance to change it:

      GNU nano 2.2.6            File: /tmp/A/TheProject/.git/COMMIT_EDITMSG

    Merge branches 'a-branch' and 'b-branch'

    Conflicts:
            README.md
    #
    # It looks like you may be committing a merge.
    ...

Let's say we're happy with the commit message - all we need to do is simply exit the text editor `nano` using Ctrl-X; and in the terminal, `git commit` will conclude like so:

    user@PC:/tmp/A/TheProject$ git commit
    [master e967546] Merge branches 'a-branch' and 'b-branch'
    user@PC:/tmp/A/TheProject$ rm README.md.orig
    user@PC:/tmp/A/TheProject$ git status
    On branch master
    Your branch is ahead of 'origin/master' by 3 commits.
      (use "git push" to publish your local commits)

    nothing to commit, working directory clean
    user@PC:/tmp/A/TheProject$ git log --oneline --decorate --graph
    *   e967546 (HEAD, master) Merge branches 'a-branch' and 'b-branch'
    |\
    | * f9418cf (origin/b-branch, b-branch) b-branch (bob) README edit
    * | 6e26ae4 (origin/a-branch, a-branch) a-branch change of README
    |/
    * e0da4fb (origin/master, origin/HEAD) alice change of README.md
    * e69e8ec bob edited README.md
    * 8709a34 afile.txt new file added
    * f183325 here is the second commit
    * e9fe842 this is my initial commit

All that is left, is to push this merge commit to the "main" repo:

    user@PC:/tmp/A/TheProject$ git push --all
    Counting objects: 9, done.
    Delta compression using up to 4 threads.
    Compressing objects: 100% (3/3), done.
    Writing objects: 100% (3/3), 400 bytes | 0 bytes/s, done.
    Total 3 (delta 1), reused 0 (delta 0)
    To /tmp/main/TheProject.git
       e0da4fb..e967546  master -> master

And - we're basically done with merging the branches. Let's just try pulling these latest commits in Bob's repo - but note that at this time, Bob's repo has the same problem as Alice's previously: the local branch `b-branch` was created in that repository; and as such it doesn't track the remote branch. That should be fixed with `git branch --set-upstream-to`:

    user@PC:/tmp/B/TheProject_git$ git branch --all
    * b-branch
      master
      remotes/origin/HEAD -> origin/master
      remotes/origin/a-branch
      remotes/origin/b-branch
      remotes/origin/master
    user@PC:/tmp/B/TheProject_git$ git branch -vv
    * b-branch f9418cf b-branch (bob) README edit
      master   e0da4fb [origin/master] alice change of README.md
    user@PC:/tmp/B/TheProject_git$ git branch --set-upstream-to=origin/b-branch b-branch
    Branch b-branch set up to track remote branch b-branch from origin.
    user@PC:/tmp/B/TheProject_git$ git branch -vv
    * b-branch f9418cf [origin/b-branch] b-branch (bob) README edit
      master   e0da4fb [origin/master] alice change of README.md

... before we try the `git pull --all`:

    user@PC:/tmp/B/TheProject_git$ git pull --all
    Fetching origin
    remote: Counting objects: 7, done.
    remote: Compressing objects: 100% (3/3), done.
    remote: Total 3 (delta 1), reused 0 (delta 0)
    Unpacking objects: 100% (3/3), done.
    From /tmp/main/TheProject
       e0da4fb..e967546  master     -> origin/master
    Already up-to-date.
    user@PC:/tmp/B/TheProject_git$ git status
    On branch b-branch
    Your branch is up-to-date with 'origin/b-branch'.

    nothing to commit, working directory clean

And finally, all seems to be fine. At this point, the state of the repositories is like this:

scrshot_027.png

Note that the Git GUI clients, for all three repo directories, show graphically the same merging process in their graphs.

A final note: after this process:

* Alice's repo is on branch `master` (since Alice had to check out `master` in order to perform the merge)
* Bob's repo is still on own branch `b-branch`

So, if Bob continues hacking `README.md`, he will continue from the last state of the file he had in `b-branch` - meaning, he will miss the merged content of the file which is currently in `master`. So, Bob should either merge `master` into `b-branch` (resulting with a new merge commit) - or simply copy the content of the file in `master` into `b-branch` (resulting in detection of unstaged changed); so he can continue editing starting from the latest changed.

Alice, on the other hand, would have to do a checkout of `a-branch` first, in order to continue in own branch - and then, make sure the `README.md` file there has the latest content, similarly to Bob (either via merge, or via copy of content).


With this, the tutorial is concluded. Happy hacking! `:)`

sdaau, 2017
