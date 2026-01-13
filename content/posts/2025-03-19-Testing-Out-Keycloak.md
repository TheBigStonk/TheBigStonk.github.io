+++
title = "Untitled"
date = "2025-03-19T00:00:00+13:00"
draft = false
+++

# 

---

---

## Testing out Keycloak
### 19th March 2025
I was told by a good friend to check out Keycloak due to making "authentication easy as hell". With the commercialization of good auth on one side (Auth0, Okta) and on the other end poorly implemented auth (think OAuth with improper redirect_uri) I did have a gap in my heart for an opensource, extremely simple IAM solution for complex web applications.
Enter[github.com/keycloak/keycloak](https://github.com/keycloak/keycloak), analyzing the code and docs, there are a few characteristics worth noting:

- Built with Java
- Strong engagement with 26k stars and +1k contributors
- Support for Argon2 for password hashing algorithm[as default](https://github.com/keycloak/keycloak/tree/main/crypto/default/src/main/java/org/keycloak/crypto/hash)
- Support OpenID Connect and IdP integrations both user defined and social
- Distributed under Apache 2.0 license
- Deployable from a docker image via a one liner `docker run -p 8080:8080 -e KC_BOOTSTRAP_ADMIN_USERNAME=admin -e KC_BOOTSTRAP_ADMIN_PASSWORD=admin quay.io/keycloak/keycloak:26.1.4 start-dev`
- Supported by the Cloud Native Computing Foundation (CNCF)
[So let's spin it up:

![](/images/keycloak_spinup.png)

[This build up the IAM and drops a web server locally on port 8080 we can visit the keycloak panel to manage the auth setup:

![](/images/keycloak_users.png)

[From here we'll:

- Create a Realm
- Create a User
- Register and Secure Our First Application on the Keycloak test application
[You can find how to do this on https://www.keycloak.org/getting-started/getting-started-docker however for the most part I found it simple enough.

![](/images/keycloak_oauth.png)

[The URL redirects from that to our OpenID Connect between the https://www.keycloak.org/app/ test app and our local 8080. With a Authorization Code Grant with PKCE (Proof Key for Code Exchange) and a couple other things like nonce and state set, this is definitely well implemented and something I'd general call secure when set up properly with a few tweaks and swapping `start-dev` out for `start`

![](/images/keycloak_alldone.png)

[Not least of it we have RBAC through groups added and managed in Keycloak, ability to swap out algorithms, add SSO (both user defined and social), handle multiple realms and implement auditing of user sessions:

![](/images/keycloak_useraudit.png)

[Overall my thoughts are that this gets two ticks from me. I started this research less than an hour ago, and having fulling build up a development IAM server and had the time to blog about this, I am super excited to see how this amazing open source project goes.