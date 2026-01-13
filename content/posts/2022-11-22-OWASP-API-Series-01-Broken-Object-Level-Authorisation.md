+++
title = "OWASP API Top 10 Build and Break Series - 01 - Broken Object Level Authorization"
date = "2022-11-22T00:00:00+13:00"
draft = false
+++

Welcome to the following series showing you all how to build an intentionally vulnerable API. The goal of this experiment is to teach you, the discerning engineer how to identify vulnerabilities in APIs. I believe that if you can build your own vulnerable version of something, you are more knowledgeable in breaking it (just ask an architect how to breach the castle they designed 🏰). Once you get good at doing this. You can then move on to testing other peoples APIs 🤘

Broken Object Level Authorisation in a nutshell is where an attacker is able to manipulate the query of an API in order to access an object without the API performing additional authorisation checks regarding the validity of the data. This is similar to Insecure Data Object Reference (IDOR) and in many cases this is one in the same, however differences can arise in the event of something like state of the user in the API not being tracked, and potentially accessing information that is referenced correctly, but not via the users current position within the confines of the system. Broken Object Level Authorization (sometimes called BOLA) can be many different types of things and a broken authorisation catch all for APIs, so it is no surprise that this is rated as the top.

## Example: Big Bank Account Balances

- Say I start out with my bank having bigbank.com and I have just logged in (a bearer token is issued alonside the profile number)
- After this, the website takes me to bigbank.com/profile, with the webpage calling`api.bigbank.com/{PROFILE_NUMBER}/balance`which checks if the bearer token is a legit one and will then return a name and account balance with the bank
- We notice that the`/balance`object is not authorized, and as long as a bearer token is valid, will go through with the request
- What's more. The account numbers are sequentially numbered (i.e. 5489, 5490, 5491)
- Changing the request from`api.bigbank.com/5489/balance`to`api.bigbank.com/5490/balance`ends up validating against our token, and giving us another customers balance!
For the visually inclined, see below:

![](/images/owasp_api1_example.jpg)

## Setup
Throughout this series we will be building an API in C# with the ASP.NET Core 6.0 framework. We are running with this over the popular Express API in JS and simple FastAPI in Python due to enterprise IT favoring .NET and the extensibility the .NET MVC gives up for the extension of the API as we progress throughout the OWASP API Top 10. For more information on how to get started building an ASP.NET Web API please visit [Microsoft\'s official documentation](https://learn.microsoft.com/en-us/aspnet/core/tutorials/first-web-api?view=aspnetcore-7.0&tabs=visual-studio).

Start by opening up a copy of Visual Studio 2022 and creating a new**ASP.NET Core Web API**template. Ensure you are at the place where you have a weather controllers setup. We are going to add a model for our account data object which will look like such:`csharp namespace BigBank.Models { public class Account { public int Id { get; set; } public string? Name { get; set; } public float? Balance { get; set; } } }`Once that is done, we will then add a database context which handles how data models are managed with the database in relation to the Entity Framework. The code for this is: ```csharp using Microsoft.EntityFrameworkCore;

namespace BigBank.Models { public class AccountContext: DbContext { public AccountContext(DbContextOptionsoptions) : base(options) { }`public DbSet<Account> Accounts { get; set; } }`

} ``` Moving on we set an in an InMemoryDB and create a scaffolded controller using Visual Studio. If you have done everything correct it should all fall into place.

![](/images/owasp_api1_entity.jpg)

As this tutorial is going on, we won't be bothering too hard with the authentication of the API at this stage, however we will just pretend auth happened, and that the header has the bearer token value of "wumbo" in it: ```csharp [HttpGet("{id}/account")] public async Task> GetAccount(int id) { var account = await _context.Accounts.FindAsync(id);`if (Request.Headers.ContainsKey("Wumbo")) { if (account == null) { return NotFound(); } else { return account; } } else { return Unauthorized(); } }`
``` At this point we should have two endpoints that we will use to break the application, these two are: -`POST /bank`and -`GET /bank/{id}/account`.

## Breaking it
Okay so we have a POST endpoint, let's add two users being:

- 5489, Max, 15 - 5490, John, 955483

![](/images/owasp_api1_add_endpoints.jpg)

At this point, let's just pretend we are looking at the API for the web application for the bank. When we log in we notice that we get a page displaying our information and that a request was made to`api.bigbank.com/bank/5489/account`to get our info for Max.

Being the discerning tester, we say**Why don't we directly try accessing an incremental ID via this API to check the auth?**. Doing this we come across this response by the API:

![](/images/owasp_api1_unauth.jpg)

However, let's not just blindly trust this message, there may be Object Level Authorisation issues at play here, and that we are just missing authentication parameters (had this happen in an internal security assessment before, so it's worth noting Devs miss auth error messages up all the time, if the message isn't generic to begin with).

Intercepting a legitimate request, we notice that we were missing the auth header (in our example 'Wumbo'), adding this in we find that if you're authenticated then there is broken authorisation on pulling account details.

![](/images/owasp_api1_whoops.jpg)

This is less likely to happen where you are using a tool like Burpsuite where you intercept and modify a legitimate request that already contains all the header information required, however it does happen with direct API testing without an application and without legitimate requests to springboard off. My general advice is:

- Headers are important to modify as well as payloads when testing APIs
- Broken Object Level Authorisation is still broken even if you're using hard to guess UUIDs, that's just security through obscurity
- Most Broken Object Level Authorisation will exist in complexity and endpoints that are unintented as such, so when testing:

- Obtain the Swagger documentation of a .NET API if you can grab it
- Create user data if you can and note every variable that can contribute to object referencing
- Sometime Broken Object Level Authorisation only appears once that object has been created and modified in a number of ways first. This can lead to local testing failing to identify this and subsequently leading to it being discovered in prod where those data objects are thrown around and used.

## Prevention
Now I am going to steal directly from the OWASP API recommendations [here](https://github.com/OWASP/API-Security/blob/master/2019/en/src/0xa1-broken-object-level-authorization.md) however I have changed them slightly as 2019 was a long time ago, and I would vouch to have them rewritten as such:

- Implement a proper authorization mechanism that relies on the user policies and hierarchy.
- Implement the bare minimum the user should have access to, require authoristaion checks for these actions, and deny all else. A model of implicit denial and least privilege is a good step forward.
- Prefer to use random and unpredictable values as GUIDs for records’ IDs.
- Write tests to evaluate the authorization mechanism. Do not deploy vulnerable changes that break the tests.
- Dynamic business logic testing can uncover authorisation issues and should be done often, especially for complex systems.