+++
title = "The Start of Baboon"
date = "2022-11-28T00:00:00+13:00"
draft = false
+++

##
Welcome to the start of Baboon. I created Baboon due to my use of Github pages for blogging moving to a use of Jekyll, then Jekyll-Now before having to go down the rabbit hole of customising Jekyll before breaking the whole thing to which I ended up throwing my hands in the air and going. Stuff it, I'll build my own generator and then use that for a blogging tool to publish blog.maxfrancis.me on. If you are reading this post from there, I was successful (yay), and if you didn't, then you're probably just reading a random Markdown file committed to GitHub (go out and touch some grass).

What I wanted from my tool were the following properties:

- I wanted this tool to resemble very old blogs (think 90's academic) where function was far more imporant than form. - I want there to be as little effort as possible (deployable via GitHub actions or a local build and push). - There should be few external dependancies.

The following was achieved by basing my engine off of Pelican and Jekyll Now. You write something like this. Push to production, and Python will build via GitHub Actions or via the site_gen.py file. Everything else is just index.html, css, and images.