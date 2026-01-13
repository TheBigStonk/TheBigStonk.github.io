+++
title = "Untitled"
date = "2021-10-22T00:00:00+13:00"
draft = false
+++

# 

---

---

---

### Introduction
Username enumeration is very much undervalued as a risk. For most people they see this as little more than
        knowing a handle or a profile name.

> 

So what if they have my email address to login? They don't have my password so I'm safe.

Although it is true that username enumeration is not 'be all, end all' of an attack, it is certainly a core step
        in the Cyber Killchain[For more information on
            the Lockheed Martin Cyber Killchain, click here](https://www.lockheedmartin.com/en-us/capabilities/cyber/cyber-kill-chain.html). Once a full list of usernames on the system is
        enumerated, an attacker can go on to perform other attacks such as:
        - Credential Stuffing: Where a previously used password is relayed to other accounts to check for password
        resuse.
        - Brute Force: Most likely using a wordlist of commonly used passwords to check for low hanging fruit.
        - Phishing: Taking the domain and discovered usernames to produce a plausible looking password reset to capture
        creds that way.

### Core Concepts

![](/images/i_dont_exist.png)

Testing for username enumeration using the Open Web Application Security Project (OWASP) under ID*WSTG-IDNT-04*is perscriptive in identifying this risk. The latest updated*WSTG-IDNT-04*can be
        found[here](https://github.com/OWASP/wstg/blob/master/document/4-Web_Application_Security_Testing/03-Identity_Management_Testing/04-Testing_for_Account_Enumeration_and_Guessable_User_Account.md.)

### Examples
Let's use the PortSwigger Academy labs to illustrate the few examples of username enumeration.

###### 1. Username enumeration via different responses:
We start off with a website around blogging, included is a homepage and a page to view your account.

![](/images/username_enumerate_example1.png)

Clicking on the account gives us a login page with a username and password field. Let's just try to enter a
        random username password combination to ascertain what happened:

![](/images/username_enumerate_example2.png)

Hold up... It says*Invalid username*... maybe we could run a username list through this in Burp Suites
        Intruder function to start testing different username combinations with the password as 'password'.

Testing with a 8,894 size username list that comes default with Burp Suite. We note a lack of rate limiting with
        475 attempts a minute on average possible, with which we are able to exhaust our list in 19 minutes.

For the sake of time though we stopped the list at 2,000 and instead used the 101 size username wordlist provided
        with the lab.

![](/images/username_enumerate_example3.png)

As you can see, we sort the responses by length since a length of 3290 bytes seems to always return when*Invalid username*is used. When the*asterix*username is submitted however we get a returned
        3292 byte length response. This is because as shown in the response instead of*Invalid username*, the
        response returned is*Incorrect password*.

With a little bit more brute-forcing on the password side this time since we know the user, we successfully
        breach the users account. Although the username is the less sensitive of the two fields, it is still 1/2 the
        digital combination lock.

![](/images/username_enumerate_example4.png)

###### 2. Username enumeration via response timing:
Now we will look at the application configured with a response timing user enumeration issue.

![](/images/username_enumerate_example5.png)

As we can see, we have no verbose error messaging that indicates an incorrect username. Instead we are returned
        with*Invalid username or password.*. What we should do then since we are given a list of potential
        usernames for this lab is send these through the Burp Suite intruder again to ascertain if we can get anything
        out of the form through enumerating other factors of the response.

![](/images/username_enumerate_example6.png)

Now we have an issue where we are shown that there is an issue around too many incorrect login attempts, and that
        we have to try again in 30 minutes. This will not do and we require a way to bypass this.

This is where the*X-Forwarded-For*header comes into place. Further information can be found around the
        header[here](https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/X-Forwarded-For)however in a
        nutshell this is used to collect an IP address for ascertaining additional information about the user and
        perform additional actions such as seeing returning location specific content based on the IP address. Through
        enumeration it was discovered that the application is using IP addressing to block too many requests, and since
        the application accepts the*X-Forwarded-For header*we change the IP around to bypass this protection.

![](/images/username_enumerate_example7.png)

![](/images/username_enumerate_example8.png)

Now that we have a bypass, let's do Intruder again. This time we should will include our new header and utilise*Pitchfork*as with the same username list but with randomly generated IP addresses courtesy of[https://www.browserling.com/tools/random-ip](https://www.browserling.com/tools/random-ip). Also
        note that we set the password to around 100 characters in order to potentially add computation time to see if
        this changes the responses potentially enough to enumerated between active and inactive usernames.

![](/images/username_enumerate_example9.png)

So as we can see, user*azureuser*takes longer than the rest to return at the 900-ish mark. Note as well
        that this is confirmed through a few attempts in repeater. Now that we have a valid user we repurpose our bypass
        enumeration user enumeration tab to bruteforce the password.

![](/images/username_enumerate_example10.png)

This was a combination of response timing and length with bypass, but shows how user enumeration can get a bit
        more complex than what one might initially expect.

### Prevention
Now for prevention. The following four steps should in combination or as a complete set for most applications, be
        seen as complete and adequate prevention.

![_config.yml](../images/remediations_username_enumeration.png

###### 1. Implement MultiFactor-Authentication (MFA)
This is always a good idea to enable MFA as both a user of the application, and as a developer implementing
        security protections in order to better protect your customers and improve the overall security of your
        platform.

MFA does not outright prevent username/email enumeration, but what it does do is provide defence in depth against
        further compromise such as where a malicious threat actor may perform enumeration and password brute-force
        attacks to attempt to gain access to a particular account. MFA is especially important for administrator
        account, although potentially you could leave one without MFA for a "break-glass" event (note that Availability
        needs to be weighed up against Confidentiality in this case).

For more information on MFA,[click
            here](https://www.cert.govt.nz/it-specialists/critical-controls/multi-factor-authentication/).

##### 2. Rate limiting
Rate limiting puts a cap on how often someone can perform an action within a certain timeframe. There are
        considerations on how this is performed, including:
        - Lock out penalties once a cap has been triggered;
        - How many attempts over how long justifies a cap being triggered;
        - How rate limiting is analysed to indicate threats to the system; and
        - How to prevent automatic repetition of requests (i.e., bots).

By far the easiests methods of implementing rate limiting in web applications is to integrate a front facing Web
        Application Firewall (WAF) into your system. A product like Cloudflare would help to do this however the
        negative effect of this is that now you have point of failure for your web application front facing proxy. An
        additional preventitive control would be to implement a Completely Automated Public Turing test to tell
        Computers and Humans Apart (CAPTCHA). A CAPTCHA is an excellent way to check that the individual making the
        request is not an automatic script but is instead a human being. CAPTCHA is especially effective in scenarios
        such as protecting submission forms.

##### 3. Using non-unique error messages
This one is simple but also incredibly overlooked. Information on responses from request made to authenticate,
        reset passwords, and anything else that requires the confirmation should not inform the request maker whether
        the information entered was correct. This includes simple but effective changes like instead of "username wrong"
        return "username and/or password wrong" in the case of our username password combination.

##### 4. If possible, use non-attributable usernames (i.e, email addresses)
There are a number of reasons for this. Firstly, an attributable username makes targetted username enumeration
        more plausible. This is particularly true where attacks such as password reuse come into play where potentially
        gaining full access to an application reveals credentials and work email addresses, which allows for further
        password spraying on other platforms.

I am not saying don't use email addresses for username verification, I am just saying consider the system. If
        this is for a highly sensitive system maybe even a unique user ID might be a better option.

##### 5. Ensure response times for endpoints are consistent between correct/incorrect usernames
There are a few ways that this can be achieved however the simplest way to prevent time based user enumeration is
        to pad the response times with an acceptable random ammount of time to add complexity to timing responses to
        perform username enumeration. A Web Application Firewall (WAF) may also assist in padding and timing as a
        prevention technique however this is not always guaranteed. There are cases where even addition tenths of a
        second on a login could impact the performance of an application. In those cases the risk of enumeration should
        be weighed up with performance (In comes the classic Confidentiality vs Integrity balance).

### Conclusion
Username enumeration in a number of cases in unavoidable unless an overhaul on how sign-up and authentication is
        redesigned. The core principle of identifying username enumeration and designing protections against
        exploitation (Our examples only include login, these don't include sign-ups, advanced bypass like those seen in[bypassing
            session handling rules with anti-CSRF tokens](https://portswigger.net/support/using-burp-suites-session-handling-rules-with-anti-csrf-tokens), or the many other factors that may need to be considered).
        It is due to this security architects and developers alike instead focus on what can be managed and remediated
        on in terms of defence in depth and minimising the impact of user enumeration on the userbase and platform. This
        includes where possible using non-attributable usernames over email addresses where appropriate, as well as rate
        limiting and preventing protections endpoints that can be used to enumerate users. The core protections however
        are to use non-unique, generic error messages and normalise timing between failed and accepted username input so
        that error message and time based authentication is more difficult, and therefore not viable for an attacker.

#### References

- [https://portswigger.net/web-security/authentication/password-based](https://portswigger.net/web-security/authentication/password-based)
- [https://owasp.org/www-project-web-security-testing-guide/latest/4-Web_Application_Security_Testing/03-Identity_Management_Testing/04-Testing_for_Account_Enumeration_and_Guessable_User_Account](https://owasp.org/www-project-web-security-testing-guide/latest/4-Web_Application_Security_Testing/03-Identity_Management_Testing/04-Testing_for_Account_Enumeration_and_Guessable_User_Account)
- [https://www.rapid7.com/blog/post/2017/06/15/about-user-enumeration/](https://www.rapid7.com/blog/post/2017/06/15/about-user-enumeration/)
- [https://www.vaadata.com/blog/user-enumerations-on-web-applications/](https://www.vaadata.com/blog/user-enumerations-on-web-applications/)

---