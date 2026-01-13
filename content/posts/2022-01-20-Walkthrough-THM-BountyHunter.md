+++
title = "Untitled"
date = "2022-01-20T00:00:00+13:00"
draft = false
+++

# 

---

---

---

Hey all, Happy New Year 🍾🍾🍾 I hope everything has been going well for you all. 2022 looks like it is shaping
        up to be an amazing year for cybersecurity, from trends in people adopting blockchain technologies and
        buzzwords, to an ever-growing threat of supplychain-related vulnerabilites on software (One only need look at
        Log4J). With such complexity it is nice to sometimes have a casual box to tinker away at. That casual box is
        Bountyhunter.This box can be found[here](https://tryhackme.com/room/cowboyhacker)

![](/images/bountyhunter_intro.png)

The following requires you to run a Linux distribution and have a TryHackMe account. Once that is all done you
        can connect to the VPN to access the THM network and with the machine spun up you should have an IP for
        Bountyhunter to get started.

We will start with a basic Nmap scan to enumerate ports. You could use Rustscan or masscan however sometimes it's
        best to keep it simple.

The command syntax we will be using is:

> 

sudo nmap -sC -sV -T4 [IP_ADDRESS] -oN initial_scan

What this command does is scan the first thousand ports (you can specify more with the '-p' tag). The**-sC**stands for default scripts, the**-sV**enumerates for versions, and the**-T4**is a speed flag. The**-oN**then outputs the scan to a file so we can
        reference this again. Note that if you don't get the results shown below that is because:
        1. You aren't connected to the network properly
        2. Your scan command is not correct
        3. You may have an underlying error in identification of the server, try more scans!

![](/images/bountyhunter_nmap.png)

Now highlighting the important stuff here we notice that FTP (File Transfer Protocol) is running with anonymous
        access enabled, which basically means that you can access the FTP share by setting your name when you login with
        the username 'anonymous', the other two points to note is that you also have HTTP 80 open so there is a website
        running, and SSH 22 which is a Secure Shell remote access protocol. We could take a look at 80, or enumerate
        users on 22. For now though we will just login anonymously to 21 and pull all the files we can using the
        following syntax:

> 

ftp [IP_ADDRESS]

Once logged in

> 

ls
            cd [DIRECTORY_TO_CHANGE]
            GET [FILENAME]

![](/images/bountyhunter_ftp.png)

As you can see, we used some additional commands not discussed. A more full list can be found[here](https://www.cs.colostate.edu/helpdocs/ftp.html).

Viewing the text files, we notice we have a note from*lin*, and a credential list. Based upon the
        questions in the room we can assume we have everything to get the user and root flag.

![](/images/bountyhunter_ftp.png)

If you remember before, we stated that we have 22 SSH for remote login and management open as a port on the
        machine, we could assume there is a*lin*user on the box, and that one of those passwords in that list
        might belong to*lin*. We can test this with a quick bruteforce attack using hydra. If you don't know
        hydra you can read more about it[here](https://github.com/vanhauser-thc/thc-hydra).

The command syntax to perform this attack is this:

> 

hydra -l lin -P locks.txt 10.10.152.130 ssh

![](/images/bountyhunter_ssh.png)

As you can see. We are now successfully in the machine by bruteforcing lin's password and performing an SSH
        connection to confirm the results of the hydra script. At this point a quick look on the machine while give you
        the user.txt flag for the machine. Now to target root.

There are a number of ways to escalate privileges on a machine once you have some user access. However we will
        check which command the user can run as root using sudo (short for super user do). The command to check this is:

> 

sudo -l

![](/images/bountyhunter_check.png)

Sudo privileges can be dangerous. From our check we noticed that we are able to run tar as a root user. Going to
        GTFObins, a site dedicated to privesc using bin programs on the machine we can see there is a[privilege escalation using tar with sudo](https://gtfobins.github.io/gtfobins/tar/). The tar
        command they recommend to run runs the bash command to give us the shell using the -I flag, which filters data
        (in this case /dev/null) through a command. I won't bore you with the other commands however I implore you to
        deconstruct the shell privesc using tar as sudo. Note we are using the command for GNU tar. We can check this is
        infact GNU tar on the machine by checking the**--help**flag.

> 

tar xf /dev/null -I '/bin/sh -c "sh <&2 1>&2"'

![](/images/bountyhunter_root.png)

And there we have it. I hope you learned something here. This was an easy box with straightforward escalations
        and enumeration without any rabbit-holes. However I do implore you to note the methodology is important to know
        when you are stuck and how to test everything. As someone who has had a realisation in 2022, I have come to
        understand CTFs if anything teach attention to detail and leaving no stone unturned, every failed command or
        privesc is just more information around what does and doesn't work.

Happy hunting out there ya'll 🤙

---