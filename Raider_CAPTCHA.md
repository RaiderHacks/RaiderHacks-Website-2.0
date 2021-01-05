Rationale for CAPTCHA

Password guessing attack: attacker tries to guess / brute-force the user's password by attempting many logins in parallel.

Solved easily by adding increasing login delay (wait time before the login is available again) after each wrong login attempt or even temporary account locking. Delays / locking should be done by IP address + username, to avoid login problems for the legitimate users.

Secure KDF-based password storage delays the password guessing process, so it is highly recommended.
Using a CAPTCHA after a 2-3 unsuccessful login attempts provides quite good protection.

Denial of service attack: attacker may attempt to login too many times to overload the system or can try to lock some user account with too many invalid login attempts for the same user.

The protection from this attack is similar to the previous attack: use a CAPTCHA and delay the login process for certain IP address after each login attempt.

Practical Cryptography for Developers

The Argon2 Whitepaper recommends a simple proof-of-work takes 100 milliseconds,

regardless of the device used.

The following exceeds 100 milliseconds:

time echo "passwords" | argon2 spartacus -d -t 1 -k 1048576 -p 8 -l 64 -e

or 

time echo "passwords" | argon2 spartacus -d -t 1 -k  786432 -p 8 -l 64 -e

and no bigger than

time echo "passwords" | argon2 spartacus -d -t 1 -k 1572864 -p 8 -l 64 -e


Cryptocurrency mining, that takes 0.1 seconds on a 2 Ghz CPU using 1 core --- Argon2d with 2

lanes and 250 MB of RAM

(https://www.password-hashing.net/submissions/specs/Argon-v3.pdf)

Truth be told this is only 20% more time than the Friendly CAPTCHA: 80 milliseconds.


For the CAPTCHA test meant to thwart supercomputers, we wish to force them to take

185 seconds before they finally pass the CAPTCHA challenge.

Based on the fact that each Argon2D hash calculation takes ~100 milliseconds, this will

mean the computer should have to guess amongst 222,000 bit combinations before finally

arriving at the correct hash. So that is half of the total number of bit combinations:

111,000.

The number of bits it would take for 222,000 combinations would be:

log_10(222000)/log_10(2)

Calculating that in Python:

```
>>> import math
>>> math.log(222000)/math.log(2)
17.760200151012196
>>>
```

So that is around 18 bits.

That is three bytes that the computer must randomly guess correctly :D.

-----------------------------------------------------------------------

A simple browser test should take ~3.2 seconds and here is how it will

work:

1. The Argon2 Parameters required for the CAPTCHA test is:

time echo "password" | argon2 spartacus -d -t 1 -k 124000 -p 8 -l 64 -e

The salt should ideally be randomized so clients cannot just perform rainbow

table attacks against the CAPTCHA. Now, although in this specific case the

salt is "spartacus" a CSPRNG should be used to generate a 16-byte salt.

2. So the above Argon2 verification test should take more than 100 milliseconds.

Of course, that's not long enough to thwart a real spam bot attack :)


I did say this test should take ~3.2 seconds. To accomplish this, we will force

the client to procure a hash whose first Base64 Encoded Byte is the exact

byte the server demands it to be. The server will obviously not be able to cheat

or shortcut their way around this since the client will be required to send

back the challenge puzzle buffer with the final byte that makes the entire

puzzle buffer output the exact Argon2D hash that meets the challenge.


The way the browser test will work is that the first base64 character in the

final Argon2 hash will be equal to the verification base64 character. Of course,

the user will not get away with brute-force figuring out what that single

base64 character is all by itself since the server will actually Argon2D hash

the puzzle buffer the client returns to the server anyway :)

Final Statistical Test

There are three kinds of machines the CAPTCHA is going to distinguish

against:

1. Standard laptop and desktop machines

2. Gaming machines--those with a large amount of GPUs

3. Titans--these are almost certainly up to no good. Blacklist

them at once.

1. Standard laptop machines will be subjected to the following test:

time echo "password" | argon2 spartacus -d -t 1 -k 124000 -p 8 -l 64 -e

2. Gaming Machines will get one last test--and only because they solved the first puzzle too quickly

If the computer completes the second puzzle too quickly then the computer's IPv4 address

is blacklisted at once.


To tell if the puzzle was solved too quckly a normal distribution-based p-level test

will be conducted on the amount of time it took for the computer to defeat

the challenge versus the expected time. If the p-level < 5%, then the server

gives the next challenge or blacklists the client machine.


3. Once the client finds the correct puzzle buffer that maps to an Argon2D

hash that begins with the correct Base64 character, the client will send

the correct puzzle buffer and the corresponding Argon2D hash.

4. The server verifies that the puzzle buffer maps to the claimed Argon2D

hash and that the hash begins with the required Base64 character. 


The whole point of this CAPTCHA test is that it disproves that the client

is an untargeted spam bot.

---------------------------------------------------------------------

Honeypot fields

(https://www.usertesting.com/blog/think-your-site-needs-captcha-try-these-user-friendly-alternatives)

(https://stackoverflow.com/questions/2230453/spam-prevention-reduction-contact-form)

A surprisingly effective technique to distinguish bots from real humans

is to have hidden fields.


There will be three hidden fields for the following:

1. Email Address

2. Password

3. Confirm Password

4. A hidden Javascript "CAPTCHA" Start Button. :)

5. Hidden "Register" button. In reality, the user is supposed to click 

on the "CAPTCHA" button on the web browser and after the test passes the 

POST request will automatically be made on behalf of the user.

This is arguably the most tempting button for a untargeted spam bot

to press. On the visible web page, the submission form field will

have the name "captcha" instead. But on the hidden form field it

will be "register".


The moment a bot clicks on **ANY** of these, their IPv4 address is 

sent to the server for blacklisting by the firewall :)

---------------------------------------------------------------------

Defeating Targeted Spam Bots


The CAPTCHA and Honeypot fields working together will almost certainly

defeat untargeted spam bots. These are bots that crawl through the

Internet looking for vulnerable websites to make spam blog posts or

fake accounts--two problems our website will actually deal with.

The whole point of the login system was to ensure bots and anyone

else unwelcome would not be able to spam the blog.


For now, the site is vulnerable to Cross-Site Resource Forgery (CSRF)

and the cure to this is using an Anti-CSRF HMAC-Blake2b token.

But more on that later.


The whole point of the CAPTCHA and the HoneyPot fields was to defeat

these untargeted spam bots that are not specifically targeting our

website. Many untargeted spam bots are unprepared to deal with the

Javascript on a webpage.

---------------------------------------------------------------------

How Memory Requirements Defeat SPAM bots Powered by Cloud-Storage

Providers

There are several cloud-storage providers out there with awesome

computer power.

1. The TTU HPCC Quanah Supercomputer Cluster is one of them.

It boasts an impressive 72 logical CPU(s). How awesome!

Now, only TTU students would be able to make spam bots

on that thing. So let's move on to more realistic options:

2. REPL.it (https://repl.it) (Googe Cloud Platform)

REPL.it has become famous for giving users a true online

bash environment--free of charge.

3. VULTR (https://vultr.com)

Our own website, https://raiderhacks.com, is actually hosted

on VULTR :)

And you wanna know what all three have in common?

All **three** of these cloud hosted server solutions give

each user less than 1 GB of RAM.

So an obvious way to defeat the bots that are powered by 

this much computing power is to do the following:

time echo "password" | argon2 spartacus -d -t 1 -k 1572864 -p 8 -l 64 -e will defeat

most cloud-storage hosted spam bots

The sad truth: how are you going to verify the hash

on the VULTR server?

Look at how much RAM the VULTR server itself uses:

top - 19:06:09 up 22 days, 17:33,  1 user,  load average: 0.00, 0.00, 0.00
Tasks: 		109 total,   		1 running, 	108 sleeping,   	0 stopped,   	0 zombie
%Cpu(s):  	0.0 us,  	0.0 sy,		0.0 ni,100.0 id,  0.0 wa,  0.0 hi,  0.0 si,  0.0 st
MiB Mem :    	977.5 total,    95.5 free,    	343.9 used,  538.1 buff/cache
MiB Swap:      	0.0 total,      0.0 free,      	0.0 used.    442.9 avail Mem

And even if you could, keep in mind it takes a very long time to verify hashes (> 1 second).

We ideally want a verification to only take 5 milliseconds at the worst.

Solution To The Problem:


Let clients that visit the index page of RaiderHacks do all of the hard work for us.

Whenever a random client visits the index page of RaiderHacks, they will receive a generate

a 256-bit nonce and with it the HMAC-SHA256.

Its the client's job to calculate the memory-expensive 256-bit Argon2ID hash, and the Blake2B 

verification hash of the Argon2D 

hash that the client calculated. 


The 256-bit nonce must itself have its own HMAC-SHA256

The hash calculation will only take >500 milliseconds. 


The only true way this would work is if the client could login from the command line.


This is definitely possible. That way, the server would time out the registration request and

blacklist the IPv4 Address. It would be extremely obvious a spam bot was trying to log in

since there will be a notice in the command line's help option that it only works if the 

client machine has more than 1.5 GB of RAM free at the time of login. The true benefit

of doing this is that it would prevent machines with many GPU cores but little RAM (often

the case with multi-core cloud-hosting services).


There is no reason a person should try to login using such a machine--especially since

we explicitly warn the user in plain detail.

To be honest this would be a far more secure login that would be no more convenient

than a standard login.


The command line application would have to manually insert the cookie the client receives

from the server into the user's browser's cookie database file. Of course, the CLI

would obviously do this on behalf of the user.


From the command line the user can literally replace password verificaiton with public

private key cryptography using LibSSH.


---------------------------------------------------------------------

Argon2 CAPTCHA Test (Final Version)

Most untargeted spam bots operate on cloud hosted technology--and those

only give at most 1 GB of RAM.

The following is a proper argon2 configuration that will take down all

bots that operate on cloud hosted technology:

echo "passwords" | argon2 spartacus -d -t 1 -k 1048576 -p 8 -l 64 -e

The amount of RAM is 1 GiB. That's more than 1GB of RAM.

The hash calculation on the cloud computer will fail simply because

the bot does not have access to the RAM necessary to get in.

Remember, this only defends against ***un***targeted spam, remember?

In the section below, we will deal with how we will deal with:

targeted spam.

---------------------------------------------------------------------

Targeted Spam


Let's have a funny story to depict how we will take down targeted spam.

Adib, our wonderful president, is trying to hack the RaiderHacks election.


Why? Because he wants to stay president. That's why.

To cast fake votes, Adib first needs to register fake accounts.

So he is going to spam the living hell out of the registration

system :O.

He writes a spam bot in Python. 

Adib is smart.

Adib uses Tor to spoof the Ipv4 addresses and hide his location

properly--defeating the firewall (very smart of him).


Adib tries to spam the hell out of the RaiderHacks registration

system by putting in fake email addresses.

Adib carefully read the free and open source source code published

by RaiderHacks on how the registration system works:

https://github.com/RaiderHacks/RaiderHacks-Website-2.0

Adib knows that the server will not accept any passwords

that fail to be Base64 encoded and that fail the ZXCVBN test.


So he randomly generates passwords for each fake account and

uses ZXCVBN to ensure that all passwords get a score of 4, the

highest score.


Keep in mind the registration website only accepts "@ttu.edu"

email addresses.

Now, Adib also knows the website uses the Argon2 CAPTCHA test

proposed above. So he does not bother trying to host the spam

bot on the Quanah/RedRaider cluster nor any cloud-hosted

solution for that matter. He knows that these services do

not have the RAM to pass the Argon2D test, which requires

a whoppin' 1 GB of RAM to pass.

Adib is quite bummed out about this because he was really

looking forward to taking advantage of Quanah's supercomputers.


Those bad boys boast 72 logical CPU(s), and thus Adib would

have been able to send MANY registration requests at a time

had it not been for that stupid CAPTCHA spam-bot test.

But Adib is still not giving up. With the power of Tor, Adib

is confident he cannot be traced.

And he awaits account creation for each...

This might be a great technique to protect the login

system. But it does not protect registration systems.

For that, you will still need to use the CAPTCHA

system you were proposing earlier to delay spam bots

on the registration page.

You know, the whole deal with forcing the client

to brute force figure out the last byte and hashing

that with a 100-millisecond Argon2 hash. :)

-------------------------------------------------------------

Vulnerabilities in Registration and Mitigations


Adib is not a fool. He has read the backend of the server

implementation very carefully. 


He knows he cannot bypass the Argon2D CAPTCHA test 

on the registration page since the server knows what the 

nonce originally was--especially since it was signed with

an HMAC!

He knows he can bypass the login system CAPTCHA since it

only takes ~8 seconds to complete.

But he also knows that the registration page asked for 

a valid TTU email.

Adib gets cocky and thinks he can submit registrations

with fake TTU email addresses.

He bases those fake email addresses on the real email

addresses of real people.


He figures the RaiderHacks Administrators probably

would not notice how weird any of that is. Its just

a student organization anyway.


Why do they care about what a person's email address

is?


Based on how the registration verification process

works so far, Adib would definitely succeed in

his task. There is nothing the RaiderHacks email

system does to verify the student's email address

is real...

---------------------------------------------------

The Reality of Spoofed Emails versus Verifying Emails

It is very easy to spoof emails since the sender has

full control over what information is sent to the

recipient. Now, to mitigate this, OpenPGP standard

was invented. If you are reading this, please

read up on how to use GNU Privacy Guard. It should

save you and the people you care about from social

engineering attacks through email one day:

(https://gnupg.org/)

Now, Adib is a smart guy. He knows that's a fundamental

flaw with how the Internet is designed. And he thinks

that therefore it should be extremely difficult to

verify if an email is real, right?

Wrong.

It is actually very easy to check if an email is real.

The next time you suspect if an email is fake, try

sending it an email. Your mail user agent ( usually

your email web-service application ) will actually

be able to tell you if an email was successfully

sent since it will be able to tell if it received

an acknowledgement packet. Once that happens,

the mail user agent knows the email was sent successfully.

Think about how email servers work.

Adib got the domain name correct: ttu.edu

So ttu.edu has its own email server.


The username is the critical part of the email address

at this point.


The email server will query its database and check if

a user has that email username. If not, then of course

its obvious that the email address does not exist.

ttu.edu's email server will send a packet that informs

the sender that the email message request failed.


Now, Adib learns that the hard way from **cough**

**cough** past experiences.


So this time he simply decides to enter the real-life

email addresses of actual TTU students--whose email

addresses do not exist yet in the RaiderHacks

database.


This works--the ttu.edu email server will be able to

find the email usernames of said people. And the ttu.edu

email server will send back an acknowledgement packet

to the RaiderHacks email server verifying the email

was processed succesfully.

Now, if the RaiderHacks team thinks carefully

about what I just said they will realize

this is obviously not enough.

There has to be one last step. One that the client

that caused the email verification process

to begin to finish off.

The final step the client has to do is login to

the email address the client claims to have 

access to and click on a "magic link".

This magic link is actually a route on

https://raiderhacks.com, hopefully

something like:

https://raiderhacks.com/verify


The magic links is going to be formatted

like this:

https://raiderhacks.com/verify?[HMAC-BLAKE2b-digital-signature-in-URL-Safe-Base64-Encoded-Form]


The part in brackets, the HMAC, is what is going to force Adib

to actually be able to login to the email addresses he claims

to own and click on the magic link directly.

A proof of work in its own right.

Because the HMAC-BLAKE2b will be based on a 256-bit nonce

generated by doing this:


HMAC-BLAKE2b(256-bit nonce,email address + 128-bit salt)

It will be impossible for Adib to brute force the HMAC

within the 3-minute time limit he has for **ALL** the

emails he claims to possess...since he first has to

brute-force hack their passwords. :D

See what was done there?

-------------------------------------------------------

Spam Account Deletion

A python script will be continously running in the background

checking if a requested account's email verification

time has expired. If that's the case--then destroy the

requested email addresses's information. :)

Of course this will also happen if the HMAC verification

test fails.

-------------------------------------------------------

Testing 1.5 GB RAM and 8 cores of parallelism on Windows Power Machine 

This Argon2D setup was tested on a client desktop

running Windows 10, 32 GB of RAM, and 32 logical CPUs.

It took ~4.5 seconds for the computation to finish

on that machine.

--------------------------------------------------------

Testing 1.5 GB RAM and 8 cores of parallelism on Linux laptop

This Argon2D setup was tested on a client laptop

running ArchLinux (5.4.77-1-lts), 8 GB of RAM,

and 4 logical CPU(s). It took ~7 seconds for the

computation to finish on that machine.

--------------------------------------------------------

Results for 4 GB of RAM systems.

Systems that only support up to 4 GB of RAM (32-bit CPU powered

systems) have less than 2 GB RAM free on average.

Testing 786432 KiB RAM and 1 core of parallelism on VULTR server:

Forcing the client to use 1.5 GB of RAM is too much for client

machines that only have 4 GB of RAM.

--------------------------------------------------------

The idea of requiring needs to be tested on a 64-bit

system with 4 GB of RAM and 4 logical CPU(s)


