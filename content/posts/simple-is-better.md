+++
title = "Simple Is Better"
date = "2022-12-01T00:00:00+13:00"
draft = false
+++

Welcome everyone. I would like to introduce this website as the new and improved blog for 2022 before the end of the year.

Many would argue this looks like something out of 1997 — and they would be absolutely right. What I’ve built is a blog compiled via **static site generation**, deployed to **GitHub Pages**, and costing me exactly **$0**.

What this is *not*:
- A convoluted WordPress codebase  
- A site-in-a-box wrapper like Wix or Squarespace  
- JavaScript-heavy or CSS-driven  

There is no JavaScript. There is no CSS. There may occasionally be images — but only when words aren’t enough.

---

## Benefits of the new approach (over a generic Jekyll blog)

Honestly, there are many — but the main ones, broken down by **S.U.U.S.S**, are:

### **Super fast**
This thing is fast — *Formula One fast*. That’s thanks to GitHub’s infrastructure, Varnish caching, and Fastly CDN.

Using SolarWinds Pingdom Website Speed Test, I get:

- **181 ms** — North America (San Francisco)
- **221 ms** — Europe (London)
- **254 ms** — Asia (Tokyo)
- **320 ms** — Pacific (Sydney)

*If you don’t trust me (fair), run your own test at*  
👉 https://tools.pingdom.com

---

### **Unique**
I feel like a full-blown hipster saying this — but I wrote my own tool called **_Baboon_**.

It takes my questionable monkey-brain ideas, converts Markdown into HTML, branches a new article, and deploys when I’m happy with it.

Everyone has WordPress, Jekyll, or Blogger.

At the time of writing, I’m the only one with a **Baboon-driven, static HTML-only blog**.

---

### **Understandable**
I know this site.

- I know where the servers are  
- I know how it’s generated  
- I know exactly what’s on it (very little)  
- I know what cookies and local storage it uses (**none**)  
- I even know its total size down to the kilobyte  

That level of understanding is rare with dynamic platforms.

---

### **Secure**
I’ve spent years doing web application security for accounting systems and handling bug bounties.

One of the strongest indicators of vulnerability is **complexity**.

The more tech, frameworks, plugins, and abstractions you add:
➡️ the larger your attack surface becomes.

Simple, well-understood systems consistently outperform complex black boxes.

That said, this site still has:
- MFA
- SSL
- DNS security flags
- Long-term domain locking
- Alerting
- A one-click migration plan to https://surge.sh

I *actively encourage* security researchers to hack this site.

If you succeed:
- I’ll pay you
- I’ll publish a `security.txt`
- We’ll agree on bounty value

---

### **Simple**
This site exists to serve content — not div soup.

No Ruby gems.  
No JavaScript CVEs.  
No dependency hell.

Just content, engineered to be **as un-engineered as possible**.

---

What this ultimately means is that this **no-framework approach may become the framework** I stick with.

Less really is more.

Either this flops…  
or you’ll see a *lot* more articles.

---

![Simple Spider-Man](/simple_spidey.jpg)

---
