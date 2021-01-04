Required Reading:

Practical Cryptography For Developers 

(https://wizardforcel.gitbooks.io/practical-cryptography-for-developers-book/content/mac-and-key-derivation/argon2.html)

Server Relief Password Authentication


1. This server will follow LibSodium Library's guidelines for password authentication.

These instructions are found at: https://libsodium.gitbook.io/doc/password_hashing#server-relief

2. So the idea of Server Relief is to force the client to do most of the hard work--relieving

the server most of the stress involved in password authentication.


Password hashing algorithms--including Argon2--are designed to be computationally expensive

to perform. This is what makes it difficult to crack the password in the first place!

But there is a tradeoff to this approach. In order for password hashing to be difficult to do,

even the server that must authenticate users in must perform computationally expensive operations

to verify the user as legitimate.

3. In a system that does NOT use Server Relief, here is what happens:

	A. The user types in their username and password in the login page.

	
	B. Both pieces of information are sent to the server in the original form

	they were typed in. We assume the information is encoded using UTF-8.

	
	C. Hopefully, the website enforces Preloaded Strict Transport Security.

	If you are sending passwords in plaintext, you better make sure this is

	the case or a Man-In-The-Middle Attacker can steal the data in transit

	to the server! In fact, you ideally want to make it an A+.

	(https://www.ssllabs.com/ssltest/analyze.html?d=raiderhacks.com)

	
	D. With TLS enforced, all of this information sent to the server is 

	encrypted. So the server will receive the username and password.

	
	E. The server will hash the original password. How this is done depends

	on the password hashing algorithm. For Argon2, the backend developer in

	charge of password authentication is responsible for setting the number

	of CPU cycles and the amount of RAM used in the computation.

	The recommended parameters for this for the sake of web server-based

	password authentication would look like the following in Python:

	hashed_passwd = [hashed password string from database] ( format: $argon2id$v=VERSION$m=MEM_USAGE,t=NUM_ITERATIONS,p=NUM_THREADS$[base64_encoded_hash_of_password] ) ( Reference: https://github.com/P-H-C/phc-winner-argon2 )
	
	crypto_pwhash_str_verify(hashed_passwd,PASSWORD,len(PASSWORD))

	What crypto_pwhash_str_verify does is that it takes whatever the password input is (PASSWORD) and translates that into an irreverisble hash string that conforms to the format specified above.

	So in a server that does not do server relief this can take a few seconds. Even a computation that takes as little as this is dangerous--especially in the event of a DDOS Attack. DDOS Attackers set up botnets that when combined all try to authenticate into the server using bogus logins.

	The point is when you have hundreds or even thousands of bots that are trying to authenticate into the server, the amount of seconds between each client increases until a session timeout for clients take place. Hence the DDOS attack. The more clients are requesting login means the more time it takes for each client to have their request processed. The point is this can end up taking so long the request exceeds the Time-To-Live time limit. At this point, the connection the client has to the server closes. On the server's side, stressing the server with too many clients can cause future clients that are requesting access to be unable to acesss the site, as the server's resources have been exhausted. As for clients in session, they can get stuck on page. We all have dealt with that problem before.
	
	The problem when it comes down to password authentication is the amount of time 

	it takes for the server to complete the processs of translating the original 

	user's password (along with the salt in the hash string) into the user's hash.

	But...if the server simply made that process too short, it would be easier for

	attackers to crack the password.

	
	So to solve this problem--ensuring it takes the server as little time as possible

	to authenticate the user--without sacrificing the user's security--security

	developers have decided to split up the work between server and client.

	
	Introducing Server Relief

	
	In Server Relief:

	
	1. The client first directly hashes their own password--using their username

	as a salt--directly on their browser. LibSodium has published a Javascript 

	version of their cryptographic library that allows this to happen. The password

	is actually not hashed using the exact API call described above (crypto_pwhash_str)

	but simply hashes the password into an array of raw binary bytes all by itself. 

	This hashing process on the client's browser should take at least a second.

	
	2. At this point, the parameters for hashing using crypto_pwhash on the client side

	will be the following:

	
	CPU cycle parameter: crypto_pwhash_OPSLIMIT_INTERACTIVE

	
	RAM parameters: crypto_pwhash_MEMLIMIT_MODERATE. This requires 256 MiB of RAM. 

	It will take about 0.7 seconds on a 2.8 GHZ Intel Core i7 CPU. This value

	may be increased to ensure the process only takes at least a second--even

	on the newly installed Red Raider Clusters :).

	
	The hash will be outputted into base64 encoded form and sent to the server

	in that encoding. This ensures the binary data is transmitted properly.

	Do not forget that HSTS-Preloading should be enforced or the hash the 

	client sends can get confiscated.	
		
	
	3. On the server, the server will translate the base64 encoded hash and 

	translate it back to raw binary data form in its RAM. Now the server

	hashes once again--except the server does a very weak hash--just to make

	sure the new hash is different than the previous. What is the whole point

	of re-hashing again? 
	
	
	4. Planning Ahead of Time: In the future, the password database will get

	stolen. Always does. Just look at all those password breaches from

	password management companies. Since the server needs to automatically be

	able to access the database, the password database file needs to have the

	correct chmod permissions to be able to access it. Just to be clear, there

	is NO reason to encrypt the password database file. The passwords are stored

	in hashed form for a reason. In the event the password database file gets

	stolen, it is the problem of the attacker to crack each user's password.

	
	So going back to your question on why re-hashing is important. The answer

	is straightforward: so the hash the client sends to the server is NOT the

	only piece of information the attacker needs to authenticate as that user.

	Imagine how awful it would be if the attacker got his hands on a password 

	database that only stored the password hash string that the client directly 

	sent to the server. They would be able to impersonate as the user immediately

	after stealing the database. By rehashing the hashed password the client sends

	to the server, the attacker is forced to attempt to crack the password using a

	designated password hash cracking tool.

	
	The PyNaCl Library is a Python binding of the original NaCl C library and was

	chosen to be used for this project.

	(https://pynacl.readthedocs.io/en/latest/password_hashing/)

	
	The PyNaCl library was chosen for the backend aspect of Server Relief.


	So the PyNaCl is actually used for the backend second hashing in the Server Relief

	authentication system. The backend must do crypto_pwhash_str				

	Here is a sample code use case where the minimal password hashing is done on

	the server:

>>> import nacl.pwhash

>>> client_hashed_passwd = b'[client's output of pwhash.kdf() here]'


>>> nacl.pwhash.argon2id.str(client_hashed_passwd,nacl.pwhash.OPSLIMIT_MIN,nacl.pwhash.MEMLIMIT_MIN)

b'$argon2id$v=19$m=8,t=1,p=1$Y2ug5BM6vfvGdDbm3AKg4A$kgWFYrMGlDwhY8aPE/rMZPsOpfKeawjG7tADXut5Qoc'


The API call nacl.pwhash.argon2id.str actually outputs the password hash in the next line

in the form it is to be stored in the password database at the time the user is

registering for a new account.

The process seen above is actually performed when the user is registering for an account.

When the user wishes to login, the following must be done:

import nacl.pwhash

>>> client_hashed_passwd = b'[client's output of pwhash.kdf() here]'

>>> nacl.pwhash.argon2id.verify(passwd_str_in_database,client_hashed_passwd)


Now that takes care of the server side.

The client side must use the Javascript binding of Libsodium to accomplish its task.

To use Libsodium in browser Javascript, you will need to download the sodium.js file

from the following resource: https://raw.githubusercontent.com/jedisct1/libsodium.js/master/dist/browsers-sumo/
sodium.js

The file will be found in the other javascript files in this repository.

So the sodium.js file is found in flask_app/static/scripts/sodium.js in this

repository.

In addition to having the sodium.js file, you also need to have the following

script declaration in every HTML file that you intend to call Libsodium

functions from:

<script>
    window.sodium = {
        onload: function (sodium) {
            let h = sodium.crypto_generichash(64, sodium.from_string('test'));
            console.log(sodium.to_hex(h));
        }
    };
</script>
<script src="sodium.js" async>
</script>

The following codepiece demonstrates how to actually use the Javascript

sodium.pwhashh() that the client needs to perform on their browser:

it('crypto_pwhash', async function() {
        this.timeout(0);
        if (!sodium) sodium = await test_helper.init();
        let password = 'correct horse battery staple';
        let salt = Buffer.from('808182838485868788898a8b8c8d8e8f', 'hex');
        let hashed =  Buffer.from(
            sodium.crypto_pwhash(16, password, salt, 2, 65536 << 10, 2)
        );
        expect(hashed.toString('hex')).to.be.equals('720f95400220748a811bca9b8cff5d6e');
    });


And the above function call is based on the pwhash function signature:


int crypto_pwhash(unsigned char * const out,
                  unsigned long long outlen,
                  const char * const passwd,
                  unsigned long long passwdlen,
                  const unsigned char * const salt,
                  unsigned long long opslimit,
                  size_t memlimit, int alg);

References: 

https://github.com/jedisct1/libsodium.js/blob/master/test/sodium_utils.js

https://doc.libsodium.org/password_hashing/default_phf

The client needs to perform the following hash function from sodium.js

since it allows the user to use an arbitary salt. The salt in this case

will actually be set to 16 NULL bytes ( 0x00000000000000000000000000000000 )

because the actual salt the client will use is its own username.

Unlike the server's CPU and RAM parameters, the client's CPU and RAM parameters

are going to be set to crypto_pwhash_OPSLIMIT_MODERATE

and crypto_pwhash_MEMLIMIT_MODERATE.

In Javascript, the javascript version of crypto_pwhash will be used.

The following is example code used for sodium.crypto_pwhash:

<html>
  <head>
    <script language="javascript">
      console.log("starting");
      window.sodium = {
        onload: function(sodium) {
          console.log('hello');
          let password = 'toor';
          let salt = sodium.randombytes_buf(sodium.crypto_pwhash_SALTBYTES);
          let key = sodium.crypto_pwhash(
            sodium.crypto_secretbox_KEYBYTES,
            password,
            salt,
            sodium.crypto_pwhash_OPSLIMIT_INTERACTIVE,
            sodium.crypto_pwhash_MEMLIMIT_INTERACTIVE, // 1024 * 1024 * 10 is fine, 11MB breaks
            sodium.crypto_pwhash_ALG_DEFAULT
          );
          console.log(key);
        }
      };
    </script>
    <script language="javascript" src="sodium.js" async></script>
  </head>
  <body>
    Hello, world
  </body>
</html>

That example gives us a strong idea on how to make a Javascript call to 

crypto_pwhash from sodium.js.


There are just TWO modifications we need to make to this. The key variable

must be converted to base64 encoded form in order for it to be ready

for transmission to the server.


Secondly, the call to randombytes needs to be discarded. If we simply

randomized the salt the call to crypto_pwhash uses on the client side,

then the output password hash would be different each and every time

the user logged in. It would be impossible to verify the client's

authenticity if we did this! So we are forced to use a constant

salt even at the client's side. And the salt used on the client-side

hashing is the actual username of the user.


A Footnote About Salting

What is salting and why does it matter? Consider how users' account

credentials are stored in a password database. The format would be

similiar the following:


username | email address | [password_hash_string] | [base64_encoded_salt]



Password databases are supposed to ensure that each and every username is

unique. When a password database discovers that a person is trying to make

a new account with a pre-existing username, it will send an HTTP Response

Text pointing that out and asking the new user to choose a different username.


But a good login system should NEVER reveal if a password is already being used

by a pre-existing user. If a login system does, then an attacker can map all 

the passwords used by each username simply by trying out different passwords from

the login page. Dedicated hash cracking tools can make this easy.


Instead of doing this, the login system will actually a user to use the same 

password as another user (GASP!) but here is the catch: a special string will

be concatentated to the actual password. And each user will have a unique

special string that is concatenated to the actual password. This way, if two

users have the same password, concatenating each of their passwords with each

of their unique special strings will force of each of those users to have

different [ password_hash_strings ] that are stored in the password database.


Security developers have named these special strings that are supposed to be

unique to each user: salts. Without using salts, an attacker can use what

are called Rainbow Tables. To make a rainbow table, an attacker recovers a

list of leaked passwords. You would be surprised how many of these are available

over the Internet. Here is a website that actually gives away files of leaked

passwords: https://wiki.skullsecurity.org/Passwords

(NOTE: The above website does NOT enforce HSTS Preloading Strict-Transport-Security).


After recovering a list of leaked passwords, the attacker hashes each and every

password and places the password followed by the hash into a database.

So when an attacker steals a password database--and it is easy to override

chmod permissions than we want to believe--they will simply have to search

the hash to the raw password already in the Rainbow Table.

Salting stops these Rainbow Table Attacks from working since concatenating

the salt string to the original raw password causes a completely new and

unique hash to be outputted.

So below is a diagram of this:


Hash(Password) ==> Hash_1 [Placed in Rainbow Table]

Hash(Password+Salt) ==> Hash_2 [Cannot be mapped to the raw password in Rainbow Table]

The point is, salts ruin the usefulness of precomputed tables. Here is a

security.stackexchange post on it:

(https://security.stackexchange.com/questions/51625/time-memory-trade-off-attacks)

The line work "Practical Cryptography for Developers"

provides a very nice table explaining the weaknesses of several password hashing

schemes used in the past:

Approach				Security		Comments

Clear-text passwords			Extremely low		Never do this: compromised server will render all passwords leaked

Simple password hash			Low			Vulnerable to dictionary attacks

Salted hashed passwords			Average			Vulnerable to GPU-based and ASIC-based password cracking

Secure KDF function (like Argon2)	High			Recommended, use strong KDF parameters


Aim for the Secure KDF function (like Argon2). It is free and open source :).


Seriously, Practical Cryptography for Develpers should be required reading

for the next generation of people that are responsible for managing

the security of the RaiderHacks website.

What is all this fuss about ASIC and FPGA resistance.

And what are the chances that a university student will be able to get

their hands on a very powerful computer?


I am sorry to tell you that--yes--you will be bewildered by how

ridiculously easy it is for any university student to get their

hands on a very powerful computer.

--------------------------------------------------------------------------

The HPCC Quanah and Raider Cluster Computers

Texas Tech gives free access to supercomputers to ALL university students.

How powerful you ask?

**                                                                           **
**     More information      www.hpcc.ttu.edu/operations/maintenance.php     **
**     -----------------------------------------------------------------     **
**                                                                           **
**                      Upcoming HPCC Training Sessions                      **
**     -----------------------------------------------------------------     **
**     XSEDE Big Data and Machine Learning            Dec 1-2   10am-4pm     **
top - 17:09:08 up 6 days, 21:29, 20 users,  load average: 3.54, 3.58, 4.49
top - 17:09:32 up 6 days, 21:29, 20 users,  load average: 3.46, 3.56, 4.46

Tasks: 1036 total,   4 running, 1030 sleeping,   2 stopped,   0 zombie

%Cpu(s):  4.8 us,  1.0 sy,  0.0 ni, 94.2 id,  0.0 wa,  0.0 hi,  0.0 si,  0.0 st

KiB Mem : 19797659+total, 92345392 free,  5700736 used, 99930456 buff/cache

KiB Swap: 48313340 total, 48313340 free,        0 used. 15820753+avail Mem 


The total amount of RAM that Quanah HPCC computer has free is 92345392 KiB of memory

So that's 92345392 / 1024 * 1024  is approximately 88 MiB of RAM.

Okay, so that's not impressive at all I have to admit. 

But take a look at how many cores it supports:

quanah:$ lscpu
Architecture:          x86_64
CPU op-mode(s):        32-bit, 64-bit
Byte Order:            Little Endian
CPU(s):                72
On-line CPU(s) list:   0-71
Thread(s) per core:    2
Core(s) per socket:    18
Socket(s):             2
NUMA node(s):          2
Vendor ID:             GenuineIntel
CPU family:            6
Model:                 79
Model name:            Intel(R) Xeon(R) CPU E5-2695 v4 @ 2.10GHz
Stepping:              1
CPU MHz:               2860.347
CPU max MHz:           3300.0000
CPU min MHz:           1200.0000
BogoMIPS:              4190.47
Virtualization:        VT-x
L1d cache:             32K
L1i cache:             32K
L2 cache:              256K
L3 cache:              46080K

So there are 72 CPUs, each with 2 thread(s) per core, and 18 core(s) 

per socket.

What does all of that mean?

The 72 CPU(s) means there are a total of 72 logical CPUs.

# of logical CPU(s) := Thread(s) per core x Core(s) per socket x Socket(s)

This information, the number of logical CPU(s) and RAM the server has will

be necessary in setting the hash cracking challenges that will be featured

in the CAPTCHA tool.

And that is because we need to give the server enough time to delete

spam accounts.


At the time of this writing, Texas Tech is transforming the original HPCC

cluster whose specs are shown here to the more robust and powerful

RedRaiderCluster, making the lives of hash crackers easier.

--------------------------------------------------------------------------

Email Authentication

I am sure that when making a new account on an online web service, the

web service sends you an email.

You thus have to login to your email account and click on a "Magic Link".


This magic link contains a 256-bit randomized string (in URL-Safe Base64

Encoded Form) and an HMAC of that 256-bit randomized string (also in

URL-Safe Base64 Encoded form)


The server stores both in a database table and there is a deadline after 

which the server will refuse to validate the user's account registration.


This is exactly what the RaiderHacks should do to ultimately defeat

Targeted Spam Defense. Spam Bots will NOT get away with using fake

email addresses using this technique. They can give a pre-existing person's

real email account--but if they cannot authenticate to said user's email

web service--the spam bot will still ultimately fail to register a spam

account on the website.


The additional benefit in using this email system is that RaiderHacks

can verify that whoever is requesting to register an account is indeed

a real TTU student.


The person whose email the account was registered under has less than

3 minutes to click on the magic link sent to them before the HMAC

sent to the user becomes invalid for account verification.


But even email account verificaiton will not stop spam bots from spamming

the server with fake accounts. After all, three minutes is **plenty** of 

time for any computer to submit ***A LOT*** of fake accounts.


The server is responsible for cleaning up failed account verifications.


That is why **both** email verification and CAPTCHA are necessary together.

After reading Practical Cryptography for Developers, you should be convinced

Argon2id is the best hashing algorithm to use to replace BLAKE2b. Unlike

BLAKE2b, it can be tweaked to fight against computers with a certain amount

of cores for parallelism and RAM. It is also designed to be resistant

agianst side channel attacks.

One problem with Argon2D is how are you going to make sure that the 

computer was forced to use those parameters without first forcing the

server to do them first? You can tell a client they need to compute

the hash under a certain amount of parameters. But how are you going

to ensure that the client did all the work. It is actually possible

to find hashes that pass the test proposed by Friendly CAPTCHA faster

than what we expected. Did you get the hint? The answer is measuring

the amount of ***time*** it took for the client to complete the challenge.

If the amount of time the user took to complete challenge is 

less than the amount of time expected--and it is statistically

significant (p-level < 5%), the client is blacklisted for at least

5 minutes. :)

Now, we can re-adopt the same technique that the original Friendly CAPTCHA

used: that the client will have to discover a valid Argon2 hash whose

first four bytes have a value less than a threshold.

The problem that you are still worried about: you do realize you do not

necessarily have to have computed the real Argon2D hash...just to find

a stupid 4 byte sequence that meets the minimum threshold.

The Answer:

Remember that only the last 8 bytes of the puzzle buffer are what the user 

is allowed to change, remember. 

So you actually DO need to use the real puzzle buffer to generate the final 

hash.


And remember, the HMAC is timestamped. So you cannot trick

the server in submitting later than past the deadline. 

The real problem is that the server must VERIFY the accursed hashes are proper.

In Friendly CAPTCHA's setup, BLAKE2b was used to make this inexpensive for the server.


But now that Argon2D is being used it may be extremely time-consuming for the server to

do the verification, especially since the attacker may have a stronger machine than

the server.


The server's best bet is to rely on the fact that the amount of ***time*** the server

took to complete the puzzle statistically and insignificantly differs from

the expected time. 


The expected time is the average amount of time it takes for a computer with a specific

number of cores and RAM to defeat a challenge of a specific byte length.

There are three different kinds of machines that will try to make accounts:

1. Average user's computer. So typically such machines have 4 cores and ~8 GB of RAM.

2. Power user computers. These are the desktop computers that are used by power gamers.

I am talking about the giant racks with 32 GB of RAM and 8 cores of CPU potential.

3. Hash Cracking Titans: The Quanah Supercomputer counts as one. What makes it a 

supercomputer at the time of this writing is that it has 72 logical CPU(s). But it

only has 88 MB of RAM per user.


In the real world, hash cracking machines focus on increasing the amount of CPU

logical cores their machines support. This allows the cracker to make what

is called a time/memory-space tradeoff. You are making a tradeoff between the

amount of RAM required (tough to expand easily) versus the amount of logical CPU(s)

required (much easier to expand).

You should seriously read the Argon2 whitepaper to better understand what all of this

means: 


(https://www.password-hashing.net/submissions/specs/Argon-v3.pdf)

According to the whitepaper, ASICs (Application Specific Inegrated Circuit),

FPGAs, and multiple-core GPU machines all share the same weakness:

It is still hard for all three of these devices to expand the amount of

RAM they can use.

The whitepaper reports Argon2D is recommended for backend servers and cryptocurrency

mining. Since our proof-of-work for CAPTCHA forces the user to compute a one-time

hash, there is really little value in anyone doing a side-channel attack to figure

out what the hash the client discovered was. Argon2D is actually preferable over

Argon2ID in this specific case.

The Argon2 Whitepaper said the following about user parameters:

1. Amount of memory M: make this as large as possible.

2. Number oT passes over the memory. Make this as large as possible.

3. Degree d of Parallelism: Ideally double the number of CPU cores.
 
According to the Argon2 Whitepaper, the purpose in designing Argon2

was to increase the amount of time it would take

for ASICs to crack hashes while having the same

execution time on CPU due to parallelism and

pipelining.

Hierarchy of CAPTCHA Tests:

1. The first test must take about three seconds, the amount of expected

time it would take for a user to submit an account registration request

at the bare minimum. The purpose of this CAPTCHA is to STOP untargeted

spam bots from getting in. In the future, we expect Friendly CAPTCHA

systems to become widespread.


---------------------------------------------------------------------------

Design of Email Verification System

---------------------------------------------------------------------------

Further Research on Server Relief

This amazing post on Security StackExchange gives two links on

Server Relief:

(https://security.stackexchange.com/questions/224629/password-hashing-that-is-resistant-to-asic-assisted-cracking-without-risking-dos)

Practical Cryptography for Developers

(https://wizardforcel.gitbooks.io/practical-cryptography-for-developers-book/content/mac-and-key-derivation/argon2.html)

----------------------------------------------------------------------------


Using FIDO/U2F/FIDO2/WebAuthn


Using server relief for password authentication is nice, but there is still

one last problem: phishing attacks. Despite the invention of HSTS preloading,

phishing attacks that steal account credentials are STILL a problem. It is 

VERY EASY to steal passwords from a computer. Keyloggers are the software

that can be used to steal passwords from a victim. Keyloggers are software

that--after the user downloads onto their computer--record all keystrokes

the user inputs with their keyboard. The keylogger can then send the 

password to a server that belongs to the writer of the keylogger.

Either that, or the password can get stolen from a phishing email.

This is much more likely to happen than a keylogger attack since RaiderHacks

relies on Email verification.


So what will stop these attacks from working is a reliable second factor of

authentication. Yubico and Google have worked together to make Yubikeys.


So in the event that a user accidentially gives away the password to a keylogger

or a phishing email, the U2F key will be the second factor of authentication

that the attacker will still lack--and therefore be denied admission.


U2F keys are hardware devices that perform digital handshake tests using public-key

cryptography. You cannot steal neither the private keys nor public keys from the U2F

device. U2F keys have internal CPUs and memory that only send responses to digital

handshake challenges. To ensure these challenges are only performed at the user's

discretion, the U2F key will refuse to send the challenge response until the user

taps and continually keeps their finger in contact with a button on the U2F device

until the digital handshake test completes. RaiderHacks should have an option

for U2F authentication for this reason.


Once U2F is enforced as a second factor of authentication, the attacker will

not only have to steal the user's password. The attacker will also have to

**physically** steal the user's U2F hardware key.

In the future support for FIDO2/WebAuthn will be done.


-----------------------------------------------------------------------------------

Testing for strength of passwords

1. At first Dropbox's ZXCVBN will be used to ensure the user's password is strong

enough to withstand attacks. Basically, zxcvbn in Python is used as the following:

>>> from zxcvbn import zxcvbn

>>> results = zxcvbn('Passwords are good for you, man')

>>> print(results)
{'password': 'Passwords are good for you, man', 'guesses': Decimal('269280010000000000000000'), 'guesses_log10': 23.430204114759736, 'sequence': [{'pattern': 'dictionary', 'i': 0, 'j': 7, 'token': 'Password', 'matched_word': 'password', 'rank': 2, 'dictionary_name': 'passwords', 'reversed': False, 'l33t': False, 'base_guesses': 2, 'uppercase_variations': 2, 'l33t_variations': 1, 'guesses': 50, 'guesses_log10': 1.6989700043360185}, {'pattern': 'bruteforce', 'token': 's are ', 'i': 8, 'j': 13, 'guesses': 1000000, 'guesses_log10': 5.999999999999999}, {'pattern': 'dictionary', 'i': 14, 'j': 17, 'token': 'good', 'matched_word': 'good', 'rank': 51, 'dictionary_name': 'us_tv_and_film', 'reversed': False, 'l33t': False, 'base_guesses': 51, 'uppercase_variations': 1, 'l33t_variations': 1, 'guesses': 51, 'guesses_log10': 1.7075701760979363}, {'pattern': 'bruteforce', 'token': ' for you, ', 'i': 18, 'j': 27, 'guesses': 10000000000, 'guesses_log10': 10.0}, {'pattern': 'dictionary', 'i': 28, 'j': 30, 'token': 'man', 'matched_word': 'man', 'rank': 88, 'dictionary_name': 'us_tv_and_film', 'reversed': False, 'l33t': False, 'base_guesses': 88, 'uppercase_variations': 1, 'l33t_variations': 1, 'guesses': 88, 'guesses_log10': 1.9444826721501687}], 'calc_time': datetime.timedelta(microseconds=60197), 'crack_times_seconds': {'online_throttling_100_per_hour': Decimal('9694080360000000538129560.912'), 'online_no_throttling_10_per_second': Decimal('26928001000000000000000'), 'offline_slow_hashing_1e4_per_second': Decimal('26928001000000000000'), 'offline_fast_hashing_1e10_per_second': Decimal('26928001000000')}, 'crack_times_display': {'online_throttling_100_per_hour': 'centuries', 'online_no_throttling_10_per_second': 'centuries', 'offline_slow_hashing_1e4_per_second': 'centuries', 'offline_fast_hashing_1e10_per_second': 'centuries'}, 'score': 4, 'feedback': {'warning': '', 'suggestions': []}}

All passwords on RaiderHacks must receive a score of 4 before they are accepted.

References:

https://github.com/dropbox/zxcvbn

Although the ZXCVBN library will be used for the first version of the RaiderHacks


database, a more up-to-date version will be used inspired by the forthcoming

security cracking tool: glados.

Finally, the replacement for ZXCVBN will be inspired by the paper:

Guess Again (and Again and Again): Measuring
Password Strength by Simulating Password-Cracking
Algorithms

https://cups.cs.cmu.edu/rshay/pubs/guessagain2012.pdf


How the Password Authentication will work:

1. User will type in their username and password.


2. The browser will use sodium.js to hash the password--using the username as a

salt. The real password's hash will be generated in 1.0 second. This hash

is hereby called H_1.



3. The client-side's hashes are sent to the server. The password

is quickly hashed using BLAKE2b. This hash is hereby called H_2. In Libsodium, this 


is done with crypto_generic_hash(). This is a hash that will be very inexpensive to compute. 

The computer will then use the  output of BLAKE2b to query the correct entry in the 

Auth table. 

There are THREE distinct tables that are necessary for authentication

to take place:

User Table:

Contains the user's username, Name, Email Address, and salt_2


Auth table:


Formatted as the following


username || H_2	=	BLAK2Eb(H_1,salt_2)	||	salt_3 

----------------------------------------------------------------------------

Email Magic Link

Some people are too lazy to care for passwords--even with a password

manager. For them, there is an email magic link option. They will be sent

an email with a link. To sign in, they will simply click on that link.

----------------------------------------------------------------------------

Reset Password

This is up to the system adminstrator.

I am literally giving the current system administrator two options:

1. The registration page gives the user a recovery password. The user 

will have to write down this recovery password and store it in a safe 

place. Maybe store in a password manager.


Other than that, it is recommended you write down the recovery

password and store in a safe place that is hard to reach. The 

problem is if someone steals that slip--and this more likely

to happen than we want to believe--you are screwed.


The benefit is that this means its the user's problem to reset

their password. The system administrator does not have to do

anything to help the user reset the password. The future

RaiderHacks system administrator better pick this option

if they are not willing to go through the trouble of **manually**

resetting the user's password. The procedure for this is described

below.


2. **Manually** resetting the user's password allows the user

to reset their password with the help of the system administrator.

The problem: The system administrator has to verify the student

member's identity either through video call or in person. Ideally

in person.

So here are the series of steps that need to happen if this option

is chosen.

	A. The user goes to an account recovery page.

	The user types in their new password.

	B. The user needs to schedule either a video call or

	in person meeting with a RaiderHacks system administrator.

	The student is REQUIRED to present their RaiderCard proving

	they are the true student.

	C. The system admin will run a Python script that incorporates

	the password the user sent to the server in step A. Once this

	happens the user's account information is reset to the new

	password.	

-------------------------------------------------------------------------

Securely Changing Password

Naturally, this will function in much the same way as the Registration Page.

The "Change Password" page will require the following fields from the user:

1. Current Email Address

2. Current Password

2. New Email (Outlook Allows You to Change This; If Same Email ... Leave Blank)

3. New Password

4. Re-type New Password


And that's it. The user submits and it either succeeds or fails.

Obviously, if the user types in the incorrect "Current Password",

or "Current Email Address" the request fails. :D

What may surprise you is that there is an option to actually

change one's Email Address. Outlook actually allows email addresses

to be changed, so it is important this feature is supported.

NOTE: The random 32-byte salt stored on the server should

also be replaced by a new 32-byte salt stored on the server.


Remember, ZXCVBN.js must be used to ensure the "New Password" is

sufficiently secure. The "New Password" must reach a ZXCVBN score

of at least 4 (actually the highest general score possible)

before the HTTP POST request is even sent.


If the ZXCVBN test above fails, Javascript will stop execution

and the user is forced to change their "New Password" and 

"Re-type New Password" fields before they have a chance of

their submission being accepted. Once again, the ZXCVBN

test takes place and checks if the strength of the "New

Password" is at least 4. Once this test passes, the HTTP

POST request takes place.

Advice For Implementing "Change Password" Page


The best advice is to carefully model the "Change Password"

page off of the RaiderHacks-Website-2.0/raider_hacks/auth/routes.py

file for inspiration on programming the backend of the 

"Change Password" page.

Take a close look at the following function:

```
def register():
```

in the routes.py file.

Now, the routes.py takes care of the server implementation.

For inspiration on designing the frontend of the "Change

Password" page, the file that programs what the user will

actually see on their web browser, take inspiration from:

RaiderHacks-Website-2.0/raider_hacks/auth/templates/register.html

That register.html file will be very similiar in design

to the "Change Password" file.


------------------------------------------------------------------

Defense Against UnTargeted Spam

AKA

Forcing The Client To Actually Retrieve The HTML File 

of the Registration Page


One of the most dangerous places on a website is the registration

page. 


At this time there is no way to force a client to actually

visit the Registration page when they are trying to create an

account.

If you take a close look at the parameters of the registration

page, the HTTP POST request parameters are definitely

NOT complicated:

1. First Name

2. Last Name

3. Email Address

4. Password

5. Re-Type Password


On every Internet Protocol everywhere--including HTTPS---there

are spam bots that randomly index the web looking for registration

pages to spam.


This is called "Spam User Registration".

A StackOverflow User:

(https://webmasters.stackexchange.com/questions/61291/why-do-registration-bots-exist-what-do-they-gain-from-registering-on-my-site)

The StackOverflow User pointed out the following reasons why User Spambots Are A Problem:

1. When they register, your site probably sends an email to a bad address or an address that belongs to someone that didn't register on your site. That makes you look like a possible spammer.

2. They could use the accounts to degrade performance on your site (this is one of the most concerning because if they triggered this using automated techniques it'd be very difficult to stop without inconveniencing your real users)

3. They could use the fake accounts to skew your performance metrics in areas like abandoned carts by customers, etc.

4. They could abuse features like refer a friend and sending wishlists to other email addresses that will then mark your emails as spam (If you have those available).

5. When you go to send a newsletter at a later date, your list may be filled with bad addresses.

6. These are bots trying to send you spam, or worse, trying to exploit your contact form to send spam to others.

So the spam bots can spam the database table with fake accounts.

And there is truly nothing stopping them from doing this

every 65 seconds as we speak.

At the time of this writing.


This is the exact kind of thing developers fear from SQL Injections.

Worse, a user can escape doing all the safety features the user

is supposed to protect their own accounts, or even more important,

defending the server from being overflowed with Spam Data. Or worse,

a DOS attack.

To stop bots from wreaking havoc on the registration system,

we need to FORCE the client to perform an amount of computational

work that delays the user's authentication long enough to stop

a spam attack from being effective yet fast enough four user

experience.


Finding the right time duration that combines the best of both

is a tough challenge that has challenged security developers

since web authentication became a serious problem.


Developers have devised a concept called Computer Automated

Public Turing Test To Tell Computers and Humans Apart (CAPTCHA) 

to ~~stop~~ slow down the speed at which bots that target

online webs services spam user's websites.


Today, Google's reCAPTCHA is the most famous implementation.

But reCAPTCHA has its own problems. Above all else, its not

free and open source. So no one outside of Google's Development

Team can confidently say they know how the code actually works.

They cannot say what the code is actually doing behind the scenes.

Keep in mind that in order for reCAPTCHA to work properly you need,

Google recommended you should embed it onto as many web pages on

your website as possible.

Go back and read that sentence again.

(https://www.fastcompany.com/90369697/googles-new-recaptcha-has-a-dark-side)

Anyways, a free and open source CAPTCHA alternative thankfully exists

called Friendly CAPTCHA:

https://friendlycaptcha.com/

That actually gives away the source code free of charge, even though

it has a commercial business model.

The Friendly CAPTCHA site sums up the problem with reCAPTCHA:

1. Accessibility

Normal CAPTCHA tasks are not easy for all humans. Those with poor eyesight, hearing or even using a screenreader may struggle to perform the tasks and are delayed or even denied access.

2. Usability and conversion

Nobody wants to label cars when all they wanted to do is post a comment. Every second spent labeling images is an opportunity for a visitor to give up on your website.
 
3. Privacy

The most popular CAPTCHA system, Google ReCAPTCHA depends on tracking users and collecting user data across the internet.

This is a price that you are forcing your users to pay in order to use your website. They can not opt out.

4. Bandwidth

Solving a full ReCAPTCHA challenge takes up to 2MB of bandwidth, which is a lot for users on a limited data plan.

5. It's broken (The absolute worst problem with it)

Tasks that are easy for all humans but difficult for computers may no longer exist.

Using machine learning or even browser plugins one can solve ReCAPTCHA in under a second. There are even CAPTCHA solving companies that offer thousands of solves for $1.

Normal CAPTCHAs are no longer effective at distinguishing users from bots.

6. VPN users get punished (So do TOR users, horribly)

ReCAPTCHA can not be reached consistently from certain countries such as China without a VPN. VPN users have to complete a never-ending amount of labeling tasks because they are harder to track for Google's anti-bot protection. 

In response to all of these problems, the inventor of Friendly

CAPTCHA decided to invent a CAPTCHA that used a Proof-of-Work algorithm

to filter out untargeted spam bots. The problem with machine learning

algorithms is that they required the programmers (or CAPTCHA AI) to acquire 

as much real data on user activity to improve.

But the Proof-Of-Work activity does not require this.

Instead, here is what Friendly CAPTCHA does:

1. First, randomly generate a 32-byte string using a cryptographically

secure random generator. On Linux systems, this would be using

/dev/urandom. This requires at least 256 bits of entropy to do

properly. To check how much entropy is available in the system:

```
$ cat /proc/sys/kernel/random/entropy_avail
```

It should be **far** greater than 256. It should be somewhere

above 3000. 

This 32-byte string will serve as the base of the puzzle we

are assembling for the user. It will make it practically

impossible for any computer--no matter how powerful to brute-force

guess the entire puzzle ahead of time.

The best chance a client has of passing the test is that they

actually have to make a GET request of the registration page:

"GET /register HTTP/1.1" 200 -


This is truly the fastest way of the user acquiring the final

puzzle that will be based on the 32-byte buffer in the first place :).

This 32-byte buffer actually serves as the nonce and secret key

used to generate an HMAC digital signature. An HMAC digital signature

works like this:

HMAC(secret_key,input_message) = Giant Number That Is Impractical


To Guess Nor Duplicate Using A Different input_message

So as you can see from the simple formula above, an HMAC uses a

symmetric key to derive a non-reversible, non-precomputable

hash of an input-message.


The original Friendly CAPTCHA specifications state that the

output hash will be 256-bits when using HMAC-SHA256.

But the author of Friendly-PoW decided to use HMAC-SHA256-128,

which only uses the first 128 bits of that 256-bit hash.


Here are three examples to make it very obvious what that means:


Test Case #1: HMAC-SHA-256 with 3-byte input and 32-byte key
   Key_len         : 32
   Key             : 0x0102030405060708090a0b0c0d0e0f10
                       1112131415161718191a1b1c1d1e1f20
   Data_len        : 3
   Data            : "abc"
   HMAC-SHA-256    : 0xa21b1f5d4cf4f73a4dd939750f7a066a
                       7f98cc131cb16a6692759021cfab8181
   HMAC-SHA-256-128: 0xa21b1f5d4cf4f73a4dd939750f7a066a

   Test Case #2: HMAC-SHA-256 with 56-byte input and 32-byte key
   Key_len         : 32
   Key             : 0x0102030405060708090a0b0c0d0e0f10
                       1112131415161718191a1b1c1d1e1f20
   Data_len        : 56
   Data            : "abcdbcdecdefdefgefghfghighijhijk
                      ijkljklmklmnlmnomnopnopq"
   HMAC-SHA-256    : 0x104fdc1257328f08184ba73131c53cae
                       e698e36119421149ea8c712456697d30
   HMAC-SHA-256-128: 0x104fdc1257328f08184ba73131c53cae

Test Case #3: HMAC-SHA-256 with 112-byte (multi-block) input
                 and 32-byte key
   Key_len         : 32
   Key             : 0x0102030405060708090a0b0c0d0e0f10
                       1112131415161718191a1b1c1d1e1f20
   Data_len        : 112
   Data            : "abcdbcdecdefdefgefghfghighijhijk
                      ijkljklmklmnlmnomnopnopqabcdbcde
                      cdefdefgefghfghighijhijkijkljklm
                      klmnlmnomnopnopq"
   HMAC-SHA-256    : 0x470305fc7e40fe34d3eeb3e773d95aab
                       73acf0fd060447a5eb4595bf33a9d1a3
   HMAC-SHA-256-128: 0x470305fc7e40fe34d3eeb3e773d95aab

Now, HMAC-SHA256-128 only works on 512-bit blocks.

(https://tools.ietf.org/html/draft-ietf-ipsec-ciph-sha-256-01#section-3.2)

The raw puzzle buffer contains the following information:

The input to solve consists of bytes (and their corresponding trailing offsets AKA cumulative sum of bytes)
 * 4 (Puzzle Timestamp)    | 4
 * 4 (Account ID)          | 8
 * 4 (App ID)              | 12
 * 1 (Puzzle version)      | 13
 * 1 (Puzzle expiry)       | 14
 * 1 (Number of solutions) | 15
 * 1 (Puzzle difficulty)   | 16
 * 8 (Reserved, 0 for now) | 24
 * 8 (Puzzle Nonce)        | 32
 * 32 (Optional user data) | 64

Or as characters (without user data):
tttt aaaa bbbb v e n d 00000000 pppppppp

(https://github.com/FriendlyCaptcha/friendly-pow)

The raw puzzle buffer ( input_message ) will be up to 64 bytes long.


We know 64 bytes is exactly 512-bits.


The problem: You need to send those 64-bytes over the Internet.

Anyone who has ever dealt with sending binary data over the Internet

will tell you should **ALWAYS** encode binary data in Base64

Encoded form.


So the HMAC-SHA256-128 is applied to the Base64 Encoding algorithm.

Base64( HMAC-SHA256-128( secret_key, Padded_Base64(input_message) )


And, of course, the actual raw puzzle buffer has to be applied to the

Base64 Encoding algorithm:

Padded_Base64 = Base64( input_message ) + zero bytes necessary to make 128 bytes buffer

The user will manipulate the Base64( input_message ) to complete the

challenge. 

**But** the user is supposed to leave the:

Base64( HMAC-SHA256-128( secret_key, input_message[0:31]) )

untouched. 


After the client's computer completes the puzzle,

it the client must send back the hash ***and*** the

HMAC exactly as it first received it--untouched.

This is reliable assurance the client actually made a complete

GET HTTP request from the actual registration page.


Now, there is a time limit as to how much time the user has

to complete challenge. Of course, this is to prevent the user

from spamming the user account database. It is also to give

the server enough time to delete spam if any spam attempts

succeed.


At the bare minimum, the Friendly CAPTCHA challenge needs

to take at least 3 seconds for this to work.


The formula for converting the length, in bytes **n**, of a binary input

to Base64 byte-length is: 4 * ceil( **n** / 3 )

So for 64 bytes that's:

4 * ceil ( 64 / 3 ) = 88 bytes

Now, the next multiple of 512-bits (64 bytes) after 64 is:

64 bytes * 2 = 128 bytes

That's why the Friendly PoW pads the Base64 output with zero bytes

until it reaches a size of 128 bytes exactly. :)

(https://github.com/FriendlyCaptcha/friendly-pow)


Now the user receives this Base64-Encoded message.

This is the Proof-Of-Work algorithm:

1. The client must change the last 8 bytes of the 128-byte message

until the following challenge is met:

2. The first 4 bytes of the BLAKE2b hash of the final 128-byte message

the client helped complete is less than the following number:

```
T = floor(2^((255.999-d)/8)))
```

I have not even yet talked about what that 'd' variable actually

means. It is actually a part of the original puzzle buffer message:

The raw puzzle buffer contains the following information:

The input to solve consists of bytes (and their corresponding trailing offsets AKA cumulative sum of bytes)
 * 4 (Puzzle Timestamp)    | 4
 * 4 (Account ID)          | 8
 * 4 (App ID)              | 12
 * 1 (Puzzle version)      | 13
 * 1 (Puzzle expiry)       | 14
 * 1 (Number of solutions) | 15
 * 1 (Puzzle difficulty)   | 16 (This is the 'd' variable)
 * 8 (Reserved, 0 for now) | 24
 * 8 (Puzzle Nonce)        | 32
 * 32 (Optional user data) | 64

Or as characters (without user data):
tttt aaaa bbbb v e n d 00000000 pppppppp

(https://github.com/FriendlyCaptcha/friendly-pow)

So the first 4 bytes of the BLAKE2b hash need to be less than

the T value = floor(2^((255.999-d)/8)))

Only then will the 128-byte buffer the client sends back as

a POST request--along with the HMAC-SHA256-128--be acceptable.

Otherwise, the user's IP address gets blacklisted by the server's

firewall for at least a minute ;).

Seriously, there is truly no excuse for failing this challenge

other than being too impatient.


Now, Friendly CAPTCHA's technique is great...but I see one flaw

in it.

The BLAKE2b algorithm is suspectible to specialized-hardware

attacks, including  but not limited to:

1. ASIC (Application-Specific Integrated Circuit Hardware)

2. FPGA

3. GPU




------------------------------------------------------------------

WebAuthn Protocol

RaiderHacks will support the WebAuthn protocol to educate students

on how to defend against Phishing attacks while using online web

services. 


The WebAuth protocol combines the U2F and UAF protocols and uses

public-private key cryptography-based digital signatures to give

both client and server reliable assurance of each others' identity

as a means of authentication. 


The official authenticator device that the RaiderHacks Team should

use should be a device from the Yubikey 5 Series:

https://www.yubico.com/products/yubikey-5-overview/


The reason Yubico's 5 Series were chosen as the official authenticator

device supported on the website is because their online documentation

is the absolute best of the best.

WebAuthn has server libraries that allow developers to support U2F

authentication on their website.

Our website's backend was built in Python.

Luckily for us, Yubico has a Python server library:

https://developers.yubico.com/WebAuthn/Libraries/List_of_libraries.html

https://developers.yubico.com/python-fido2/


