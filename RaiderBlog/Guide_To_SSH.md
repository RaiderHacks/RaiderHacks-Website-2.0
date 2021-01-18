# Guide To SSH

## By Tanveer Salim

<p>SSH stands for the Secure Shell Protocol. It is one of the most famous [Linux commands](https://github.com/RaiderHacks/RaiderHacks-Website-2.0/blob/auth/Introduction_To_Linux.md)--ever.

<br>

This is the command the world's best developers use to control [their websites](https://linuxgazette.net/issue59/correa.html).

<br>

Here at RaiderHacks, the system administrators [(Joseph and I)](https://raiderhacks.com/members) always

<br>

use SSH to authenticate into the RaiderHacks server (available at IPv4 address 155.138.209.188).

<br>

Let's get int othe history of how SSH became a necessity.
</p>

<p>
In the beginning there was Telnet. It was a very simple Linux command that allowed a person

<br>

to establish a simple connection with a server. Telnet basically did everything that

<br>

SSH was allowed to do--except it did not use authenticated end-to-end encryption to

<br>
keep the information exchanged between server and client private.



<br>

To make this blog as fun as possible to read, let's go over all the nastiest attacks

<br>

that a [Man-In-The-Middle Attacker](https://us.norton.com/internetsecurity-wifi-what-is-a-man-in-the-middle-attack.html) can do without the encryption protection SSH

<br>

provides.

</p>

The Norton blog sure provides **a lot** of attacks that a Man-In-The-Middle Attacker can perform.

<br>

<ol>

<li>IP Spoofing</li>

<p>One of the worst things about the Internet is that whoever is sending data to a recipient

<br>

has near perfect control over what information they can send--even if its misleading.

<br>

Today, spam bots fake their own IPv4 addresses to bypass [weak Firewalls](https://us.norton.com/internetsecurity-malware-ip-spoofing-what-is-it-and-how-does-it-work.html)

<br>

But clients are not the only thing on the web that can fake their own IPv4 address.

<br>

So can fake websites. A Man-In-The-Middle-Attacher can easily see what information a

<br>

client and server are broadcasting with each other.

<br>

Once the attacker learns what kind of information a client expects, it can start

<br>

sending messages to impersonate the website.

<br>

For all of you visual learners, here is an image that depicts what I am talking about:

<br>

![IP Address  Spoofing](https://external-content.duckduckgo.com/iu/?u=http%3A%2F%2Fen.vcenter.ir%2Fwp-content%2Fuploads%2F2017%2F01%2FWhat-is-IP-Spoofing.jpg&f=1&nofb=1) "IP Address Spoofing"]

Let's pretend the Web server with IPv4 address 132.12.25.1 has a web application firewall.

<br>

It is the firewall's job to block clients that have made excessive HTTP requests in the past.

<br>

But when said firewall receives information from a spoofed IPv4 address, guess which IPv4

<br>

address is going to get blocked?

<br>

Hint: Not Hacker (IPv4 address: 168.12.25.5)

<br>

You can start to see how spoofing IPv4 addresses can cause serious problems for servers

<br>

in being able to handle requests fast enough for everyone.

<br>

There are 4,294,967,295 addresses available in the IPv4 address space, so for each attacker

<br>

that makes each request with each and every new IPv4 address...the client that seriously

<br>

does have that IPv4 address gets blocked from the server when the firewall decides

<br>

that the client with said IPv4 address is making too many requests at once.

<br>

You can easily start to see how easily an attacker that spoofs their IPv4 address

<br>

can block many IPv4 addresses in a short period of time.

<br>

If you know Python, the following code will tell you how many seconds it takes

<br>

to traverse through all 4,294,967,295 IPv4 addresses:


```
import time

i=0

begin = time.time()

while i <= 0xffffffff:
    i += 1

end = time.time()

print(end-begin)
```

Printed Result: 364.59005427360535

<br>


So it took ~365 seconds just to traverse through all numbers in an IPv4

address space.

<br>

Now, it takes a Python script ( e.g. a spam bot ) at least 10 milliseconds

<br>

to actually transfer a packet to a server on average.

<br>

But for an attacker to exhuast all IPv4 addressses against a dumb firewall

<br>

that cannot check if an IPv4 address is spoofed:

```
4,294,967,295 IPv4 addresses x ( 1 request / IPv4 address ) * ( 10 milliseconds / 1 request ) *  ( 1 second / 1000 milliseconds ) * ( 1 minute / 60 seconds ) * ( 1 hour / 60 minutes ) * ( 1 day / 24 hours )  == 497.10269618056 days

```

Okay, fine. So it would simply take too long for an attacker to actually exhaust all IPv4 address. 

However, an attacker still target a specific subset of IPv4 addresses--such as that allocated

for a specific region or an organization. And this can block such people out of the site

unfairly.

For your convenience, here's a fun map brought to you by ![XKCD](https://imgs.xkcd.com/comics/map_of_the_internet.jpg)

</p>

<p>
CloudFlare also points out that spoofing an IPv4 address with the fixed IPv4 address of an

<br>

established website can easily cause servers to flood said website with requests.

<br>

This is exactly what happened to GitHub back in [2018](https://us.norton.com/internetsecurity-malware-ip-spoofing-what-is-it-and-how-does-it-work.html).

<br>

And below is a diagram explaining how the ![GitHub 2018 Attack happened](https://external-content.duckduckgo.com/iu/?u=https%3A%2F%2Fupload.wikimedia.org%2Fwikipedia%2Fcommons%2Fthumb%2F7%2F72%2FIP_spoofing_en.svg%2F1200px-IP_spoofing_en.svg.png&f=1&nofb=1

<br>


</p>

<li>DNS Spoofing (DNS Cache Poisoning)</li>

<p>Without the protection end-to-end encryption provides, a Man-In-The-Middle Attacker

<br>

can first trick a DNS server--a server that translates a website's domain to an IPv4

<br>

address--into routing all requests to a malicious IPv4 address set by the Attacker.

<br>

It is not that hard to make a website look like another's.

<br>

Especially since you can download the HTML file of any webpage visible in the first

<br>

place using tools like [curl](https://curl.se/), [wget](https://www.gnu.org/software/wget/),

or best of all: [aria2](https://aria2.github.io/)

<br>

<li>HTTPS Spoofing</li>

Really, all this means is that an attacker successfully makes their website's domain

<br>

look indistinguishable in appearance--yet different--from the actual trusted, legitimate

website.

<br>

To really understand this attack, you need to understand [UTF-8](https://www.joelonsoftware.com/2003/10/08/the-absolute-minimum-every-software-developer-absolutely-positively-must-know-about-unicode-and-character-sets-no-excuses/)

<br>

Go ahead. Read it. We'll wait.

<br>

So now you know that multiple valid UTF-8 characters can look very similiar to one another,

<br>

you can easily start to see how a website's domain can be faked yet looked authentic.

<br>

Perhaps the most notorious variant of an HTTPS Spoofing attack would be an

<br>

[Internationalized Name Domain Homograph Attack](https://www.xudongz.com/blog/2017/idn-phishing/). 

<br>

This attack takeas advantage of similiar looking characters from different languages

<br>

registered in the Unicode character set.

<br>

Now, typically, Certificate Authorities forbid servers from registering websites

<br>

using characters from multiple languages since that is obviously dangerous and

<br>

unreasonably difficult for people to type.

<br>

But as Xudong Zheng pointed out, [Punycode](https://en.wikipedia.org/wiki/Punycode)

<br>

allows one to get around this rule.

<br>

Even Xudong Zheng pointed out that one of the best techniques to avoid this

<br>

problem is to allow a [Password Manager](https://keepassxc.org/) to autofill your credentials 

<br>

when logging into a website. 

<li>Email Spoofing (Phishing)</li>

Ah yes, the golden social engineering attack. Well, as they say save the best for last.

<br>

Attackers have been using this attack since email was invented to con many a person

<br>

into giving away their bank account and email address credentials.

<br>

This attack was so successful, a real life [Microsoft security engineer](https://haveibeenpwned.com/) made

<br>

an actual website where you can see how many of your email accounts got hacked.

<br>

Go ahead. We'll wait.

<br>

The hacker's simple trick?

<br>

Its surprisingly simple.

<br>

Just send the victim an email asking the user to login to their email account.

<br>

And in reality the victim gave away their credentials on a [faked website!](https://www.tessian.com/blog/what-is-credential-phishing/)

Well everyone, that sums all of the generalized ways attackers trick victims

<br>

into destroying themselves online!

<br>

If you were supposed to learn anything from this long blog, its that you better

<br>

stop trusting your eyesight.

<br>

It is too easy to fake appearances to the human eye.

<br>

Security deveopers have realized this--and decided to rely upon code execution

<br>

behavior to verify if a client's request is legitimate.

<br>

## The Birth of Public-Private Key Cryptography

So how do you get two machines on a network to verify each other's identity?

<br>

This is the exact problem Martin Hellman and Diffie Whitfield faced back in

<br>

the 1970s.

<br>

These cryptographers decided that both clients split up the work of verification.

<br>

The client who wishes to establish their identity to the recipient needs to

<br>

successfully execute an algorithm using a piece of information that only the real

<br>

client would know--called the secret. 

<br>

That would be unreasonably difficult even for the most powerful of computers to 

<br>

forge.

<br>

That anyone who possesses a piece of information available to the public

<br>

to verify the identity of.

<br>

That would basically make it not worth the attacker's money nor time to bypass.

<br>

Their solution came to be known as [public-private key cryptography.](https://en.wikipedia.org/wiki/Public-key_cryptography)

<br>

The client that needs to prove its identity to the recipient would need to possess

<br>

what is called a digital secret key. This is ideally a 256-bit randomly generated

<br>

number. To give you an idea of how difficult itwould be for a computer to guess what

<br>

that 256-bit number, let's first go over what a bit is.

<br>

### Bits

Below is a photo depicting the two possible values a bit can have:

a 1 or a 0.

<br>

So a 256-bit secret key is exactly what it sounds like--a consecutive sequence of

256 bits.

<br>

Below is a real 256-bit number in bit-form:

```
0	1	1	1	1	1	0	0	0	0	0	1	1	0	1	1	0	0	0	1	1	1	0	0	1	0	0	0	0	1	0	0	0	1	1	0	0	1	0	0	1	0	1	1	1	0	0	1	0	1	1	0	0	1	0	1	1	1	0	0	1	1	1	0	1	1	0	0	1	1	0	0	0	0	1	1	1	1	0	0	0	1	0	0	1	0	0	0	0	1	1	1	1	1	0	1	0	1	0	0	1	1	0	1	0	1	0	1	0	1	0	0	1	0	1	0	0	1	0	1	0	0	0	0	0	1	0	1	1	1	1	0	1	0	1	1	0	0	0	0	0	1	1	1	0	1	0	1	1	1	0	0	1	1	0	1	0	0	0	0	1	1	0	1	0	0	1	0	0	1	0	0	0	1	0	1	0	0	1	0	0	0	0	0	1	1	0	1	0	0	1	0	0	1	0	0	1	0	1	0	1	0	0	0	0	0	1	1	0	0	0	0	0	1	0	1	0	0	0	0	1	0	0	1	0	0	1	0	0	0	0	1	0	0	0	0	0	1	1	0	0	1	1	1	1	0	1	1	0	0	1	0	1	1	1	1

```

Did you guess that 256-bit number?

<br>

Well neither can the world's most powerful supercomputers either.

<br>

And that was the point.

<br>

Internet protocols needed a way to allow clients to easily identify one another.

<br>

But that would be very difficult for attackers to forge.

<br>

And the security world's answer to this hard problem was to randomly generate huge

<br> 

numbers.

<br>

## Public Key

Unlike the secret key, the public key is supposed to available to he recipient so

<br>

the recipient can easily verify if a message sent by a client actually owns the

<br>

corresponding secret key(remember, its a 256-bit number).

<br>

What public-private key algorithms do to generate the public key is that they

<br>

take a 32-byte integer (there are 256 bits in 32 bytes) and performs a bunc of complex

<br>

involving prime numbers (since you cannot factorize them) to generate the public key.

<br>

Since prime numbers cannot be factorized, the process is irreversible.

<br>

An owner of a secret key can always use the same algorithm to generate the exact

<br>

same public key from the same secret key.

<br>

But due to the nature of prime number factoriztaion, an owner of a public key would

<br>

never be able to deduce what the secret key is.

<br>

For all of you visual learners, here is a video on the topic:

[![ComputerPhile - Public-Private Key Cryptography](https://i.ytimg.com/an_webp/GSIDS_lvRv4/mqdefault_6s.webp?du=3000&sqp=CLK-lIAG&rs=AOn4CLAYknPcJlizOR3Z0caZFwDCP647xg)](https://www.youtube.com/watch?v=GSIDS_lvRv4)

<br>

The developer behind SSH was inspired by public-private key cryptography to help encrypt messages

<br>

back and forth between machines.

<br>

Before a session could begin, both clients on a network had to prove their identity to the other

<br>

using their secret keys.

<br>

As it turns out, you can literally use secret keys (aka private keys) to digiatlly sign

<br>

messages.

