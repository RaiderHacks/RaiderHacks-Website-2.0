RaiderWall

The RaiderHacks Firewall is designed to prevent

spam bots on the Internet from spamming our server

from excessive requests---especially on registration

and login pages.

Out of the two, the registration page is the most dangerous

page on the entire site.

Think about it--you have no idea who is trying to make

an account.

Marcus J Ranum invented the concept of the Firewall, and

he wrote an excellent article explaining the dumbest

idea people have when it comes down to its necessity:


http://www.ranum.com/security/computer_security/editorials/dumb/


You see, bots are not smart enough to tell if your website

is interesting enough to be worth hacking.

They just parse pages looking for ways to get into the website to

feed off of its resources.

Hence why Marcus was forced to invent the Firewall.

So what is a firewall?


It is a program that allows certain IPv4 addresses to communicate

with a website's server. 


When a client with an Ipv4 addresses makes ***too*** many requests

within a certain time period--say within a minute--the firewall will record 

the client's IPv4 address in a hash table and refuse to allow the client with

that Ipv4 address to access **ANY** page featured on the website

for a specified period of time.

And just how many requests will a client have to make to

get **blacklisted** by the firewall?

Well, let's do some math here.


It will take ~20 seconds for any client to pass the CAPTCHA

tests featued on the registration and login pages.


Don't worry, once the user logins/registers in, they

can automatically login using a Cookie.

USE A PASSWORD MANAGER: https://keepassxc.org/

:)

So realistically, there is **NO** way a client is supposed

to make more than only 3 requests per minute.


How would it be possible for a machine to make more than 3

requests per minute?


Sadly for the Internet, the command line is always a viable

option.


The HTTP Protocol does not require clients to execute Javascript

to make any HTTP Request of any kind. 


So even a client bot that can only read HTML5 can unfortunately

still make HTTP POST requests.


Many spam bots will fall prey to the Honeypots already enforced

on the login and registration pages.


But the Honeypot by itself does nothing to limit the rate at

which a bot will be able to make successful POST requests.


For that to work, a working Web Application Firewall built directly

using the Backend Technology will be necessary.

Put simply, the firewall on the server backend is a giant hash table.

In each hash table entry, the following information for each

client exists:

1. 16-byte Blake2b keyed Hash of the following: IPv4 address + port number + 16-byte nonce

2. 16-byte Key

3. 16-byte nonce. More on why this is necessary below.

4. 4-byte POST Timestamp. This marks the time period by which the client must not make

the user should **NOT** make more than 3 requests.

When a client attempts to make a GET request on the

login or registration pages on the server, the 

operation specified in (1.) is done.

Here is Python source code that gives an idea of what

is being said (Requires PyNaCL Library):

```
import nacl.hash
import nacl.encoding
import os

secret_key = os.urandom(32) # NOTE: Only the server is supposed to know this!!!

nonce = os.urandom(16) 

data = '[IPv4 address here] + [Port Number Here]'

data = bytes(data,encoding='utf8')

# timestamp =  # The timestamp needs to be set to 1 minute after the current datetime

hmac = nacl.hash.blake2b(data,32,secret_key,nonce,encoder=nacl.encoding.Base64Encoder) # Send this HMAC to the 

# client in an HTTP Response Text

print(hmac)

```

Put documentation on how to extract IPv4 address from client here

in Python Flask

That weird function up there "nacl.hash.blake2b" takes the four arguments:

1. secret_key

2. nonce

3. data

4. Timestamp

to generate what is called the hmac hash.


Each and every hash table node needs to store 

all these four things **ALONG** with the

hmac.


The secret_key is like the password used to generate the hash, which is called the hmac.

The nonce is concatenated to the client's IPv4 address and port number. A port number

is actually just an unsigned 16-bit number. 


Port numbers were literally invented

to prevent two distinct clients that

have the **exact same IPv4 address**

from receiving information that

was originally meant for the other

person.


In this case, it is possible that

both IPv4 addresses and even port numbers

match since there are **A LOT** more

clients on the Internet than back

when this important paper was written:

(https://rist.tech.cornell.edu/6431papers/MorrisThompson1979.pdf)

That's why the nonce variable in the Python

code above was necessary.

The nonce--requiring 16 bytes of random data

brought to you by os.urandom(16), is going

to make sure that the server can distinguish

amongst clients.

See that weird variable name "hmac"?


An HMAC is actually just a **VERY** big number

that is unique to a client. 


Now, this big number called an HMAC is going to 

help the server identify a client that visited

the website in the past.


When a client makes a GET request, the server

will read what the client's (alleged since

it can be spoofed) IPv4 address and port numbers

are, and with that information and the server's

secret key (only the server is supposed to know

the secret key), the server will generate an

HMAC that will be used to identify the client

when it makes a POST request.


If any client tries to make a POST request on the

login and/or registration pages and fails to submit

a valid HMAC within its POST request, it is blacklisted

on the Web Application Firewall immediately with no

mercy.


Said client will be timed out for 3 minutes straight.


I did say previously that its actually possible

for two different clients to end up with the same

IPv4 address.


Thanks to NAT, this is definitely a possibility.

That's why the nonce had to be concatenated to

the client's IPv4 address to generate said client's

HMAC.


The nonce is what will separate different clients

from one another.


There is no reason to believe any computer on planet

Earth has the resources to exhaust enough numbers in

a 128-bit space in a reasonable time.


A computer will have a higher chance of overflowing

the hash table instead without the protection

provided by the Web Application Firewall.


So going back to the discussion about the firewall.

Its supposed to stop the server from being overwhelmed

by excessive HTTP requests from the client.


One of the smartest ways Firewall Engineers have proposed

doing this is to simply DROP the request.


That means the server does **NOT** send anything back to

the client in response to receiving a request.


The real reason why this is a great idea is that client

programs are often programmed to wait for a response from

a server.

So when a server drops a request, the server just keeps 

waiting...and waiting...and waiting...until it times out.


The famous NMAP port scanner can wait up to 600 seconds

(in paranoid mode of course) before it bothers sending

another packet to a server.

NMAP scanners sometimes do this to avoid detection.


This will obviously **REALLY** slow down the speed

at which a spammer can make requests to a server.

Other than DROPPING the request, the server can

simply send a notification that the request has

been denied. Maybe send back an HTTP 401 Error code.

So often the firewall will simply DROP the request.


-------------------------------------------------

How does doing something as simple as DROPPING

or REJECTING a request help fight DDOS and spammers.

The trick is ensuring the server can more quickly

drop or reject requests than the client can

upload spam requests to the server.

And luckily for us, time is actually on the server's

side and not the client.

How is that possible when a server can have millions

of requests at any moment.

The answer is that how fast a client can send information

to a server is limited by how fast the Internet can

actually carry it to the server.

I actually performed tests in Python that measured

how fast Python can send HTTP Requests to a typical

server. Python could only send information as fast

as 1 every 9 milliseconds.

So that's around once every 10 milliseconds.

Meanwhile, servers can reject a request in **microseconds**.

You might think I am making this up, but even the inventor

of the famous Hashcash algorithm admits this is the reality:


But won't spammers steal CPU time?

Spammers already compromise security on many users machines to make so-called "Zombie" armies to send spam from. However currently the rate at which spammers can send mail on a zombie machine is limited purely by the speed of those machine's internet links. A typical DSL user might be able to send 25 unique messages per second each of size 1KB (assumes 256kbit uplink). Or many more messages per second if the messages are delivered to multiple users at once (using multiple Cc or Bcc recipients). Even a 20-bit stamp takes 1/2 second per recipient on the highest end pc hardware at time of writing. This would slow spammers down by a factor of 10-100 or more per compromised machine (depending on whether the messages sent are sent individually or to many users at once).

(http://www.hashcash.org/faq/)

-------------------------------------------------

So its literally impossible--even for the world's fastest computer to upload

faster than one request every 10 milliseconds on average.

Microseconds versus milliseconds is nice.

But it would be nicer if we could figure out if a client is illegitimate

in nanoseconds.


In order to accomplish this feat, we will need to use an amazing data structure

called a Bloom Filter ( actually a clever variant called

a Xor Filter ) with a false positive error rate of 0.0001%


(https://lemire.me/blog/2019/12/19/xor-filters-faster-and-smaller-than-bloom-filters/)


But in version 1.0 of the Web Application Firewall, we will simply stick

to the good ol' Hash Table since it has a false positive error rate

of 0%.


So we will use the SipHash-2-4 shorthash algorithm to hash entries

into the Web Firewall's database.

You should check if your programming language of choice already

uses this amazing DOS-resistant hash algorithm.


(https://www.aumasson.jp/siphash/)


So unlike other standard hashing algorithms, SipHash-2-4 was designed

to prevent a linked-list based hash table from causing a DOS attack.

How is that possible?


Consider how Linked-List based hash tables work?

They have to traverse from the very top of a linked list, checking

each and every node along the way, all the way until the computer

hits the very bottom node in the linked list since there is node

that matches the hash entry we are looking for.


Let's see a diagram of this take place at every step:

1)

x
|
1

2)

x
|
1
|
2

3)

x
|
1
|
2
|
3

So as you look at the above crappy diagram,

keep in mind that the number of nodes that

the computer has to traverse increases by

one after the insertion of each and every

node.

Gee, that's a nice mathematical series:

1 + 2 + 3 + ...

Oooh, an arithmetic series.

This arithmetic series has a name:

(https://en.wikipedia.org/wiki/1_%2B_2_%2B_3_%2B_4_%2B_%E2%8B%AF)

Did you see that summation formula?

It proves this linked list lookup has a lookup time of

Time Complexity O(n^2).

That's bad!!!

Keep in mind our NGINX server is designed to suport up to 100,000

clients to defend against Slow Loris Attacks. An attack you can

seriously perform with a single machine.

So the time complexity when there are 100,000 nodes in one linked

list is (worst possible case scenario):

So 100,000^2 = 1.0 * 10^10

Yeah...that's how a hash table can cause a DOS attack. 

The SipHash-2-4 was designed to slow the growth of any linked list

in a hash table at any given time.

For more on how this algorithm works, you can see the following

page if you want:

https://en.wikipedia.org/wiki/SipHash

If you are coding in Python, use the csiphash library:

(https://github.com/zacharyvoase/python-csiphash)


You need to convert the unsigned 8-byte bytes object to

an unsigned 64-bit integer.


So the hash table is meant to store doubly-linked lists at every hash bucket.

And remember, each node is meant to store the following information:


1. secret_key (16 bytes)

2. Timestamp ( 4 bytes)

3. HMAC ( 4 [IPv4 address] + 2 [Port Number] + 16 (nonce) ) == 16 bytes of HMAC output :)

So each node will take up 16 + 4 + 16 == 36 bytes


When a client makes too many requests before the timestamp deadline

passes, the client's request is typically DROPPED.

That means the server will simply exit the function call without

even sending back a response to the client. The client will 

likely waste several seconds before figuring out the connection

request failed--unless the client is literally trying to flood

the server with requests (this is called a connection depletion

attack).


More on how to defend against connection flood requests later.


So how are we going to make up our mind about how many bucket

entries should exist in the hash table?

Well, if it takes ~10 milliseconds for a request, and the NGINX

server is supposed to support up to 100,000 clients at any time,

and we need to actually delete hash table entry nodes that are

outdated, we need to ensure we do not have too many hash table

entries to delete at any time without requirng too many

hash **buckets** in the hash table.

Let's first calculate the maximum amount of hash nodes Python

should have to delete **at the worst**.


So keep in mind that on average, it takes ~10 milliseconds

at the best for information to be uploaded to the server.

But keep in mind that timestamps must last at least 1 minute.

A client can make up to 3 requests every minute.

So in 1 minute, a bot can literally make ( 1000 milliseconds * 60 )/10 milliseconds

6000 requests in a minute.

In Web Firewall 2.0, the firewall will be programmed

to slow down the speed at which clients can make an HTTP GET request

to reduce the number of spam requests a bot can make.

It will involve the Xor Filter described previously.
 

Python should thus be able to destroy 6000 hash node entries

every time it needs to traverse into the table.

Keep in mind Python can perform such operations in around 

half of a **micro**second.


Go ahead. Make a short Python program and time the amount

of time it takes for Python to delete a node in linked list

on average. We'll wait.


So this should actually be no problem for Python.

For now, just know that the hash table will have 

So how much time would Python actually need to destroy

6000 nodes at the **bare** minimum.

6000/(0.5 * 10^(-6))

Here is the dimensional analysis in Python:

```
>>> (6000 * (0.5 * 10**(-6)))/1
0.003
```

So that's (6000 nodes * (0.5 * 10^(-6) seconds)/(1 node deleted))  ==

3 milliseconds :D

So at the bare minimum, it will take the server 3 milliseconds

at the bare minimum to delete 6000 nodes.

The load factor for a hash table with 100000 buckets would require

the hash table to receive 100000 inputs before we expect at least

one collision.

To reach a load factor of 1.0, it would take 100,000 insertions

We expect it to take 100000 insertions * 10 milliseconds/insertion == 1,000,000 milliseconds

before hash collisions start to become frequent.

Yeah, if it takes that long before hash collisions even to start to

exist in the hash table and 3 milliseconds < 1,000,000 milliseconds

1,000,000 milliseconds/1000 milliseconds/60 seconds == 16.6667 minutes


So after 16.6667 minutes, hash collisions will start happening pretty

much after every insertion...

Yeah...there is no way a client is going to overflow the hash

table at this point.

As long as the Web Application firewall is programmed to delete

hash node entries whose timestamps have **EXPIRED**,there is no

way the hash table will reliably get flooded since it takes 16.6667 minutes

before the load factor finally becomes >= 1.0. Meanwhile, any hash node

entry's time stamp only lasts 1 minute.

Despite these excellent math statistics, the coder should still setup

a hash table experiment to see if the computer freezes from a hash table overflow.

The hash table should be attacked with random IPv4 addresses for at least 60 minutes.

If no serious toll takes place on the computer's free RAM, then the hash experiment

is successful.
 
This hash experiment should take place on the RaiderHacks development server.

How much RAM will the computer use to maintain the Web Application Firewall?

Well, a single hash node entry takes 36 bytes.

And because there are 100,000 buckets in this hash table with an average expected

load factor of ~1.0 thanks to the deletion feature in the hash table's programming,

this should take up 36 bytes * 100,000 == 3,600,000 bytes.

So that's ~3.6 MB.

The VULTR server always has 99.5 MB free.

This is worth it.

Now, you may be wondering why not just **DELETE** all nodes in the hash table when

it reaches a load factor of 1.0. The problem with this is that many users can get

their legitimate requests denied if the server does that.

Also, it would take > 1.29 seconds for the server to delete all buckets.

In the real world, the amount of time would be WAY worse. Even if you just 

delete the node from the hash table plainly keep in mind Python uses a garbage

collector and **NOT** dynamically allocated memory that's managed by a developer

that manually manages how much memory is spent within a program.

Here is the Python code demonstrating how long it takes just to delete 

100,000 buckets in a list:

```
i = 0

list = []

while i < 100000:
    list.append(3)
    i += 1

i = 0

begin = time.time()

while i < 100000:
    list.pop(0)
    i += 1

end = time.time()

print(end-begin)

```

A more serious experiment will

be performed on the RaiderHacks Development

Server on this metric to ensure an average

of only 3.6 MB is expended regardless of how

seriously an attacker tries to overwhelm

the Web Application firewall.

3.6 MB is the expected equilibrium of the 

amount of RAM the computer will use.

So after doing all of this math

we can safely use a prime number larger than 100,000 is:

100,003.

:D

The weakness of this Web Application Firewall system

is a botnet of course. A botnet of size 100,000 devices

could easily overwhelm the Firewall since it can force

all devices to send requests to the server simultaneously.

The best way to deal with this is to split the work amongst

several firewalls evenly. 


So let's say one firewall becomes **FIFTEEN** distinct firewalls

each the same size as the original firewall.

So each firewall handles 0xffffffff/15 IPv4 addresses

each.

So now each of those 15 firewalls handle: 286331153 IPv4 addresses each.

Since each firewall handles one-fifteenth of what the original

firewall used to handle.

The only downside of this approach is that we will use 15 times as much

RAM.

Still, 3.6 MB * 15 = 52.5 MB of RAM.

The VULTR server has 478.0 MiB of RAM free is approximately 501 MB.

MiB Mem :    478.0 total,      7.4 free,    378.3 used,     92.2 buff/cache

The VULTR server will definitely be fine. :)


Any server should be okay with surrendering just 52.5 MB of RAM to handle

a DDOS attack. No server should be brought down just because of it.

Now the DDOS attacker will need to send requests at 15 times the

original rate to replicate the

same harmful effect on the server.


Now that the Firewall system has 15 times the memory space, it can evenly

divide the work amongst each of the fifteen hash tables.

So what is the threshold for that harmful rate?

Its


-----------------------------------------------

Web Application Firewall Version 2.0

Version 2.0 will not just deal with excessive POST requests but also

GET requests.


The problem with GET requests is that this is where the client

may not necessarily have visited the website yet.


You cannot just perform the HMAC quiz we did for POST

requests since we can expect the client to have visited

the site at least once previously.


To prevent a client from making excessive GET requests, the server

can simply time out the client if it makes requests at superhuman

speeds.

Believe it or not, a human cannot click something faster than 10 clicks/second.

Don't believe me?

Here, try to prove me wrong:

https://clickspeedtest.net/1-seconds.php

I'll wait.

Alright. So if the Web Firewall finds a client making more than

10 clicks within a second---it is banned for 3 minutes

straight without mercy.

There--that oughta keep those pesky bots at bay.

Since we obviously cannot rely on HMACs to test if a client is making

excessive requests when they are making GET requests, clients will

instead be required to solve a puzzle that takes an average of

~100 milliseconds to execute.


The Equihash algorithm can be set to force the client to use

a certain amount of RAM to solve the puzzle, this way, regardless

of how CPU-intensive the client's machine is, it will take around

the same amount of time as any other machine to solve the puzzle--

 less than 100 milliseconds. Before the client gets the information they

are asking for, they need to submit the puzzle solution in a

second HTTP GET Request. There is no need to hide the HMAC

solution as the puzzle solution is not easy to brute-force

guess (256 bits of entropy).

Any client that makes an HTTP GET request with the actual

puzzle solution in their HTTP GET request in

(applicaton/x-www-encoded-form) will actually get the contents

of the page they are looking for.

Any client that tries to make an HTTP GET request with a wrong

solution gets banned :).


Most bots are not designed to process Javascript. But for those

that do, this process will still slow them down by 100 millliseconds.


To account for this, two new fields will have to be appended to

the original hash table entry fields:


1. 16-byte Blake2b keyed Hash of the following: IPv4 address + port number + 16-byte nonce

2. 16-byte Key

3. 16-byte nonce. More on why this is necessary below.

4. 4-byte POST Timestamp. This marks the time period by which the client must not make

more than 3 POST requests.

5. 4-byte GET TIMESTAMP 

Ok, so that's (16 * 3 + 4 * 2) == 48 + 8 = 56 bytes

So that's now 56 bytes * 100,000 is aproximately 5.6 MB. Oh well.

----------------------------------------------------------------------------


