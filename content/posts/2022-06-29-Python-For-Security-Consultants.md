+++
title = "Untitled"
date = "2022-06-29T00:00:00+13:00"
draft = false
+++

# 

---

---

---

# Introduction
Python is a fantastic scripting language that is well aligned to the discerning cybersecurity consultant due to:
    * The ability to learn quickly and script quick solutions in easily readible scripts;
    * Extensive number of security-related Python packages (i.e.[BS4](https://pypi.org/project/beautifulsoup4/),[python-nmap](https://pypi.org/project/python-nmap/),[pyca/cryptography](https://cryptography.io/en/latest/), and[scapy](https://pypi.org/project/scapy/)); and
    * Abundance of security related tooling and scripting already going on with Python.

This article is made to help address the topic around how a security consultant could effectively take their
    journey towards learning Python in an efficient manner, and then work on that towards what nice Python code would
    look like and how to further branch out their code into meaningul modules, libraries, etc.

The outline of this post is as follows:
    1.[Getting Started with Python Fast](#getting-started-with-python-fast)2.[Good Practices around Scripting for Security](#good-practices-around-scripting-for-security-tasks)3.[Building towards Meaningful Security
      Consulting with Python](#building-towards-meaningful-security-consulting-with-python)

---

# Getting Started with Python Fast
There are a ton of tutorials around how to start coding with Python from installation of the required stuff to
    making sure you have the right PATH and so forth. We are going to make this much easier.

Start by going to[replit.com](https://replit.com/)and clicking 'Sign up'

Feel free to skip all the onboarding stuff shown, it doesn't really matter!

Now that you are in the replit account, you can now creat a Python Repl (please note that this will by public). To
    save cognitive load the appropriate clicks are shown below:

![](/images/python101_replit_createproject.png)

We have a project with a shell to install stuff, a console to view stuff, and overall a cloud environment for free
    (didn't even need to confirm the email to get to this point). The reason we have picked this method to get sorted
    is:
    - It's lightning fast;
    - It allows us to sync to our Github later (heck you can even login via GitHub);
    - You can access your code wherever;
    - You can share and allow other people to view repls; and
    - You can publish your Replits to enable others to use your little snippits.

Later on, you can work towards a different environment, however for now I find that this is the best way to get
    started.

![](/images/python101_replit_ui.png)

---

## Good Practices around Scripting for Security Tasks
Now while you're working on Python there is a few things I believe should be applied from the aspect of a security
    consultant being, in order from most important:
    1.**Design secure code:**We could go into a whole realm of secure development from running Static Application Security Tools (SAST) to making
    sure credentials like API keys aren't embedded and beyond however I propose that you ask yourself if you are
    breaching any confidentiality by running your code with sensitive data (especially in a public space like Replit),
    if you have any issues around the integrity of your system that could be abused (i.e. putting weird stuff in
    inputs), and if there are availability concerns you have to address to ensure nothing bad happens if your system
    goes down.
    As a security consultant, it is important that you research and get colleagues to vet your code, as being in the
    security industry there is a higher justification to set a good standard.
    2.**Design easy to read code:**Comment your code and make code that is logically simple to follow. This will both ensure any poor logic isn't
    hidden away with hard to read code and bad spacing. Python is designed with human readibility with top of mind, plus
    you will thank yourself later revisiting nice to read code when you have to eventually refactor it.
    3.**Design easy to use things:**If you can't share your tool or if it isn't easy to use, there is ultimately moot point to having it exist.
    Sometimes it's the simple to use but beautiful experiences that outweigh the highly intelligent systems that are
    only usable by the esoteric few. As a general rule of thumb your application should be able to be accessible by a
    browser, a mobile app, or desktop application and without the need for code. If you spend all day making command
    line tools and APIs you will be limiting the application to those that can use those things. There is something
    amazing about an system that completes a task automatically or through a single button click.
    4.**Design extensible code:**Try to learn what`__name__ == '__main__'`is and more importantly that code you write can be reused.
    Although it is tempting to just write a single script in one file, it does pay to build a repository of scripts that
    both achieve something when run directly, and that can be called upon via an`import`in order to use
    their methods. This will both encourage you to write scripts that are good as you will have to live with any
    technical debt, and will allow you to be more efficient as you start building up your security code library.

Oh and other things:
    * Have a python checklist handy.
    * Google error codes, most errors have already been discovered.
    * Comment your code.
    * Document things you like or what you find innovative.
    * Share your code.
    * Have a purpose to your code, don't just code for the sake of it.

The most important thing of all as well is to just write code when you're starting, code can be extended as much or
    as little as you want, and you can definitely overengineer a solution. As a general rule of thumb if you are
    designing something and it works, then feel free to veto everything else (even security without a purpose of value
    protection is unnecessary).

---

## Building towards Meaningful Security Consulting with Python
So now that we have a good environment, and some good principles up our sleeve, let's write a tool that does
    something cool, how about a tool that gives us the interesting sites of a domain that our client owns and does it
    all in a GUI so that other people in our team can use this.

The way we will build this is by doing the following
    1. Create a Simple GUI using PythonSimpleGUI;
    2. Write a script to interact with[Sectigo's Certificate Search](https://crt.sh/);
    3. Have interesting domains pop up in the console; and
    4. Publish the repl for everyone to use.

### Building the Certiciate Transparency Checker
Create a file in the replit called`main.py`and add the following code to it.


```
# main.py
import PySimpleGUI as sg
    import searcher as crtSearch
    import json

def callAPI(domain):
    crtSearch.search(domain)

def main():
    layout = [ [sg.Text("Add a domain name to search for additional subdomains")],
    [sg.InputText()],
    [sg.Button("Search for Certificates")],
    [sg.Button("Close App")] ]

window = sg.Window(" Client Domain Scanner", layout, margins=(100, 50))

while True:
    event, values = window.read()`  if event == "Close App" or event == sg.WIN_CLOSED:
      break

  print('Searching Domains for: ', values[0])

  callAPI(values[0])
`

window.close()

if**name**== '**main**':
    main()
    
```
Create a file called 'searcher.py' and add the following code to it:

```terminal

# searcher.py
import requests, json

def search(target):
    req = requests.get("https://crt.sh/?q=%.{d}&output=json".format(d=target))
    json_data = json.loads(req.text)

domains_list = []

for (key,value) in enumerate(json_data):
    domains_list.append(value['name_value'])

domains_list = list(set(domains_list))

for domain in domains_list:
    print(domain)
    
```
Now run it a couple of times, notice how this could be extended to do more stuff (maybe to run more input fields,
    accept a list of domains, run daily, send you an email or text when a thing happens, etc.) however for the sake of
    our quick demo this is done. Now let's publish it. This doesn't require a long winded explanation, and you should
    just be able to follow the applicable prompts.

![](/images/python101_replit_publish.png)

[! NOTE: You will need to verify your account email before publishing a Repl !]

At this point you should have something published that you can share and embed. Good job on that! From here the
    world is your oyster! You are encouraged to continue working on this and potentially straying off into the Python
    wilderness to create even more novel solutions in more permanent environments (i.e. in a proper deployment such as
    AWS).

### Afterthought
Now that we have something working, we could ehance it (make it a desktop app, make it run for all your client
    domains and alert when something is exposed), run this on an internal server, start making a tool to sell, or just
    use task related scripts in order to remove menial IT security tasks to instead be able to focus on higher level
    thinking. Although you would think scriping and automation is something best left to penetration testers and
    engineers, there is a ton of things the security consultant (someone who is more into GRC, strategy, ethics, review,
    and assessment) can do including but not limited to:
    - Key word searching and suggestions from previously discussed topics in an email server for specific clients.
    - Statistical performance collection for consulting tasks (time to reply, engagement length)
    - Information collection on clients
    - Report generation for clients
    - Enhancements to Customer Relationship Management Systems

Whatever you decide to build, the goals of enhancing value, removing menial work (imagine if accountants didn't use
    software.. :yikes:), and ultimately understanding your job better is never a bad thing.

---

# Conclusion
Python is like anything else a tool. I implore the reader to look for and unearth solutions, however, I also caveat
    this with not creating a solution if one already exists, and not 'shoe-horning' python into a problem just for the
    sake of using Python. There are cases where Python is useful, however at the end of the day the
    script/package/library you have built should facilitate the improvement of current processes in your organisation,
    and not complicate them.

---