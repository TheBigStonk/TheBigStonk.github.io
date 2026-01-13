+++
title = "Linux Security Basics Deepdive"
date = "2022-06-26T00:00:00+13:00"
draft = false
+++

# 
BlogAbout
---

---

### Introduction
Linux is everywhere. Although that is a really obvious statement, it hits home when you realise that there are a
small number of people who learn to properly use this wonderful open source environment, and even less so is the
amount of people who focus on Linux and then branch out into security considerations and making software to
secure and harden this lovely operating system.
With this article I want to provide a small journey for those starting out and want to be part of that small
group. Overall the content of this post will follow the format and inspiration of the[LPIC-Linux Essentials Topic 5. Security
and File Permissions](!https://learning.lpi.org/en/learning-materials/010-160/5/). The two key areas we will look at are:
-*All Linux Machines have users*- Users in Linux and User Administration; and
-*Everything is a file*- File Permissions and Management of Access.
By the end of the article, you will be able to go over a system, assess the users on the system, view interesting
file permissions, and explain linux security concepts to your friends (if they are the slightest bit
interested).

### Topics
Linux works off of two main concepts which is worth engraining in your mind. These are simple by principle and
are:
1.**All Linux machines have users**- Linux is a multi-user operating system (not all operating
systems have been like this in the past, especially where shared computing time was a thing), and ensures the
security of files (see step 2.) with the concepts of "ownership" and "permissions". The fundamental act of
privilege escalation (where a malicious actor tries to become the highest level user on the machine) works on
abusing ownership and permissions to switch their user account in use for the intention to manipulate and use
all the 'files', and as a result being able to do whatever they want on your system.
2.**Everything is a file**- Although technically 'everything is a stream of bytes', for the
purposes of abstraction this statement rings true. This is the core concept of the architecture of the operating
system which is designed where everything from processes, directories, sockets, pipes, and services are
represented by a file and by accessing the command line with the right permissions, almost every aspect of Linux
can be changed through editing a file edit and restarting a process.
A lot of liberties have been taken to abstract linux here, however when explaining to the layman what the
fundamentals are with linux security, you will have covered off a lot of the basics with just these two rules.
From Super User ID (SUIDs) abuse, to Cron Job file manipulation, to reading files with sensitive information and
even manipulating files that enable remote access (i.e. SSH Keys), it becomes aparrant that abuse of these two
concepts is the vast majority of security failures in linux.

#### Users in Linux and User Administration
There are four different account types that make up a linux system, and these are:
-**The Superuser Account**- On Linux, the superuser account is```root```, which always
has a UID (Unique User Identifier) of 0. The superuser, or root account, is sometimes called the*system
administrator*, and has unlimited access and control over the system, including access of other users.
The default group for the superuser has a GID (Group Identifier) of 0, and is also named```root```. The
home directory for the for the superuser is a dedicated, top level directory called```/root```at the
top of the linux filesystem, and is only accessible by the root account (or an account with root equivalent
permissions). Generally though we only want one superuser account on the linux system.
-**Standard User Accounts**- These are your general day-to-day accounts, with a standard user
account being technically defined as all accounts other than root, but on a Linux user often are 'regular'
(unprivileged) accounts accessible by a human. They typically have the following properties, with select
exceptions:
- UIDs starting at 1000 (four digits), although some legacy systems may start at 500.
- A defined home directory, usually a subdirectory of```/home```, depending on the site-local
configuration, and usually the subdirectory named after the username.
- A definted login shell. In Linux the default shell is usually the*Bourne Again Shell*located at```/bin/bash```, although others may be available.
If a user account does not have a valid shell in their attributes (usually defined in```/etc/passwd```,
but we will get to that later), the user will not be able to open an interactive shell most of the time. Usually```/sbin/nologin```. is used as an invalid shell. This may be purposeful if the user will only be
authenticated for services other than console or SSH access, e.g., Secure FTP (sftp) access only. The following
image is an example of analysing a few accounts that don't have an interactive shell.

![](/images/linux101_sbin.png)

- **System Accounts**- System accounts are typically pre-created at system installation time.
These are for facilities, programs and services that will not run as a superuser. In an ideal world, these
would all be operating system facilities.
The system accounts vary, but their attributes include:
- UIDs are usually under 100 (two-digit) or 500-1000 (three-digit).
- Either*no*dedicated home directory, or a directory that is usually not under```/home```.
- No valid login shell (typically```/sbin/nologin```), with rare exceptions.
Most system accounts on Linux will never login, and do not need a defined shell in their attributes.
Many processes owned and executed by system accounts are forked into their own environment by the
system management, running with the specified, system account. These accounts usually have limited
or, more often than not,*no*privileges.

- **Service Accounts**-*Service accounts*are typically created when services are
installed and configured. Similar to system accounts, these are for facilities, programs and services that
will not run as the superuser.
In much documentation, system and service accounts are similar, and interchanged often. This includes the
location of home directories typically being outside of```/home```, if definted at all (service
accounts are often more likely to have one, compared to system accounts), and no valid login shell. Although
there is no strict definition, the primary difference between system and service accounts breaks down to
UID/GID.
- System account: UID/GID <100 (two-digit) or <500-1000 (three-digit)
- Service account: UID/GID >1000 (4+ digit), but not a "standard" or "regular" user account, an
account for services, with an UID/GID >1000 (4+ digits)
Some Linux distributions still have pre-reserved service accounts under UID <100, and those could
be considered a system account as well, even though they are not created at system installation.
E.g., on Fedora-based (including Red Hat) Linux distributions, the user for the Apache Web server
has UID (and GID) 48, clearly a system account, despite having a home directory (usually at```/usr/share/httpd```or```/var/www/html/```).

Some accounts have a login shell, while others do not for security purposes as they do not require interactive
access. The default login shell on most Linux distributions is the*Bourne Again Shell*or```bash```, but others shells may be available like the C Shell (```csh```), Korn shell
(```ksh```), or Z Shell (```zsh```), to name a few.
Now that we have gone other account types, we will move onto administration and analysis.
Listing basic user information is a common, everyday practice on a Linux system. In some cases, users will need
to switch users and raise privilege to complete privileged tasks.
Even users have the ability to list attributes and access from the command line, using the commands below. Basic
information under limited context is not a privileged operation.
Listing the current information of a user at the command line can be done simply by typing```id```, which
will bring up the User ID (UID), primary Group ID (GID), and any additional GIDs that the user running```id```has been assigned.

![](/images/linux101_id.png)

If we want to view the last time user have logged into the system, we can use the```last```command:

![](/images/linux101_last.png)

The information listed in columns may vary, but some notable entries in the preceding listing are:
- A user ( ec2-user ) logged in via the network (psudeo TTY pts/2) and is still logged in.
- The time of current boot is listed, along with the kernel. In the example above, done on June 12th when the
cloud instance was first provisioned.
- The superuser ( root ) logged in via the netowrk (psuedo TTY pts/0), and logged out immediately after.
[NOTE: If you want to see bad logins, you can also run the command```lastb```].
As a general fun to look at, you can run a quick```sudo lastb | head```. As we can see there have been
10 logins attempts in less than 20 minutes as this machine is exposed to the internet.

![](/images/linux101_loginb.png)

The commands```who```and```w```list only the active logins on the system.
In Linux, you can add a new user account with the```useradd```command, and you can delete a user account
with the```userdel```command.
If you want to create a new user account named```tony```with default settings, and set a password with```passwd```, you can do so with the following example.

![](/images/linux101_useradd.png)
.
The most important options which apply to the```useradd```command are (using descriptions taken from the*man*pages):
- -c COMMENT. It is generally a short description of the login, and is currently used as the field for the
user's full name.
- -d HOME_DIR. The user's login directory. The default is to append the LOGIN name to BASE_DIR and uses that as
the login directory name.
- -e EXPIRE_DATE. The date on which the user account will be disabled. The date is specified in the format
YYYY-MM-DD.
- -f INACTIVE. The number of days after a password expire until the account is permanently disabled. A value of
0 disables the account as soon as the password has expired, and a value of -1 disables the feature.
- -g GROUP. The group name or number of the user's initial login group. The group name must exist. A group
number must refer to an already existing group.
- -G GROUPS. A list of supplementary groups which the user is also a member of. Each group is sperated from the
next by a comma, with no intervening whitespace. The groups are subject to the same restrictions as the group
given with the -g option. The default is for the user to belong only to the initial group.
- -m Create the user's home directory if it does not exist. The files and directories contained in the skeleton
directory (which can be defined with the -k option) will be copied to the home directory.
- -M Do not create the user's home directory, even if the system wide setting from /etc/login.defs (CREATE_HOME)
is set to*yes*.
- -s SHELL. The name of the user's login shell. The default is to leave this field blank, which causes the
system to select the default login shell specified by the SHELL variable in /etc/default/useradd, or an empty
string by default.
- -u UID. The numerical value of the user's ID. This value must be unique, unless the -o option (allow
assignment of duplicate UIDs) is used. The value must be non-negative. The default is to use the smallest ID
value greater than or equal to UID_MIN and greater than every other user.
On a note of the```userdel```command, it is important to note that the*-r*option also removes
the user's home directory and all its contents, along with the user's mail spool. Other files, located
elsewhere, must be searched for and deleted manually. Only those that have root authority are able to use this
command and delete user accounts.
When you add a new user account, even creating its home directory, the newly created home directory is populated
with files and folders that are copied from the skeleton directory (by default```/etc/skel```). The idea
behind this is simple: a system administrator wants to add new users having the same files and directories.
Therefore, if you want to customize the files and folders that are created automatically in the home directory
of the new user accounts, you must add these new files and folders to the skeleton directory.
Regarding group management, you can add or delete groups using the```groupadd```and```groupdel```commands. If you want to create a group called*researcher*with a specific group
ID of 1080, and then subsequently delete it, you can do so via the commands shown below.

![](/images/linux101_group.png)
.
The final thing we will be going over is the*passwd*command which is primarily used to change a user's
password. Any user can change their password, but only a root equivalent user can change any user's password.
The most important options which apply to the```passwd```command are (using descriptions taken from the*man*pages):
- -d This is a quick way to delete a password for an account. It will set the named account passwordless.
Available to root only.
- -e This is a quick way to expire a password for an account. The user will be forced to change the password
during the next login attempt. Available to root only.
- -l This option is used to lock the password of specified account and it is available to root only. The locking
is performed by rendering the encrypted password into an invalid string (by prefixing the encrypted string with
an !). Note that the account is not fully locked - the user can still log in by other means of authentication
such as the SSH public authentication method. Use```chage -E 0 user```command instead for full account
locking.
- -u This is the reverse of the*-l*option - it will unlock the account password by removing the !
prefix. This option is available to root only. By default passwd will refuse to create a passwordless account
(it will not unlock an account that has only "!" as a password). Thye force option*-f*will override
this protection.
- -S This will output a short information description about the status of the password for a given account. The
status information consists of 7 fields. The first field is the user's login name. The second field indicates if
the user account has a locked password (LK), has no password (NP), or has a usable password (PS). The third
field gives the date of the last password change. The next four fields are the minimum age, maximum age, warning
period, and inactivity period for the password. These ages are expressed in days.
At this first stage of two, you now understand how users and groups work in Linux, and how to at a basic level
perform administrative tasks for users.

#### File Permissions and Management of Access
As a bridge between discussing users, and looking at files, now is a appropriate time to discuss UIDs/GIDs and
how to see login attempts, current logins, adding and deleting users. How is this all managed? Well a common way
is through common Access Control Files.
The main files related to user accounts, attributes and access control are:
-**/etc/passwd**- This file stores basic information about the users on the system, including UID
and GID, home directory, shell etc. Despite the name, no passwords are stored here.
-**/etc/group**- This file stores basic information about all user groups on the system, like
group name, GID, and members.
-**/etc/shadow**- This is where user passwords are stored. They are hashed, for security. As a
security person it is worth asking how password hashes are stored and simply put, they are stored as either MD5,
Blowfish, or SHA. More information on understanding the /etc/shadow file can be found[here](https://www.cyberciti.biz/faq/understanding-etcshadow-file/).
-**/etc/gshadow**- This file stores more detailed stores more detailed information about groups,
including a hashed password which lets users temporarily become a member of the group, a list of users who can
become a member of the group at and time and a list of group administrators.
[NOTE: This files are designed to never be edited directly]
So a user will probably want to use a file, to do that linux uses something called file permission sets (this is
formally referred to as Unix symboloic notation).
To begin, let's just dive into what a permission set would look like by running the command```ls -l```:

![](/images/linux101_permissions.png)

The section```-rw-r--r--```is the permission set, the first dash is to indicate whether the object is a
file (defined by```-```), or a directory (defined by```d```). After this we repeat three groups
of three characters which ask if the user can read (```r```), write (```w```), and/or execute
(```x```) the file. These three groups themselves show:
- What the file owner can do.
- What the file owner's group can do.
- What everyone else can do.
So the three dashes```rw-```shows what the file owner can do which is read the file, and write to the
file, with the last part being a dash meaning that the user can't execute the file. The next three dashes```r--```shows what the file owner's associated group can do which is read the file. The last three
dashes```r--```shows what everyone else on the system can do which is read the file.
Now that you have a basic idea of permission sets, next is to look at a bunch and understand what they do, for
instance:
1.```-rwxrwxrwx```eveyone can read, write, and execute the file.
2.```drwx------```only the user can read, write, and execute the directory/folder.
3.```-r--r--r--```everyone can only read the file.
So now that we know how to read a linux permission set, let's change it with the command```chmod```,
which is short for change file mode bits.
At a basic level changing file permissions can be done by providing three numbers without spacing like```141```or```777```with each number represention permission for in order the file owner
privilege, group privilege, and eveyone else's privilege. You add up numbers 4 for read, 2 for write, and 1 for
execute to determine the permission. As an example:
1.```007```which means everyone execept for the file owner and their groups can read, write and execute
the file.
2.```300```only the file owner can write and execute the file.
3.```111```everyone can only execute the file.
So now that you know how this works. Putting into a pratical example, how would we edit a key file so that only
the user owner can read it?```chmod 400 key.pem```
There we go! That is one successful file edit with the result being:```-r--------```.
Now that we are gucci with setting file permissions, we need to talk about one thing before moving onto what SUID
is. It should be noted that the root user does not have file permission restrictions and can both veto and
permissions and change file permissions, even if the underlying file or folder being edited was not created by
root.
Now SUID, and SGID stand for:
- Set User ID
- Set Group ID
Certain programs like```passwd```, which changes a user's password might need to be accessible by
everyone however they might also need to be able to be run as the administrator (i.e. sudo). To solve this with
the passwd example the file permissions will look something like this:```-rwsr-xr-x```
I bet you're thinking "where did that 's' come from? You lied to me there was only read (r), write (w), and
execute (x)?!". There is actually also the```s```character which stands for the Set ID bit, which means
that whenever this command is entered, it will set the user ID (SUID) of the file owner if it is in the execute
set for the file owner. For the second group of three the```s```can be set to ensure that when the file
is run, it is done so with the permissions of the group that own the file. More than likely the SUID is set for
a normal user to run a command but with administrator powers, as even with the command passwd being used to
change your own passwd, files like```/etc/shadow```will need to be edited which only root can do. There
are multiple SUID security risks where some programs allow you access to a shell (place to input commands), and
by having the SUID set will give you a command line as root.
That last part around SUID/GUIDs can be a tough concept to understand, and I recommend watching videos and trying
to set your own SUIDs/GUIDs to get a gauge for how this all functions.

### Conclusion
This has by far been by longest post and hope this makes up for the long pause. I implore you the reader, if you
have gotten this far, to continue looking into the interesting world of Linux security, which covers a wide
gamut of topics such as having canary files published to look for a trigger, the uncomplicated firewall which
restricts network traffic at the host device stage, and many other more concepts.
Go forth you newly minted Linux security champion and I hope you conquer the hackers and save the digital world
(or at least try to).