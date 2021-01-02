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

1. Email

2. Current Password

3. New Password

4. Re-type New Password


And that's it. The user submits and it either succeeds or fails.

Obviously, if the user types in the incorrect "Current Password",

the request fails. :D


Remember, ZXCBVN.js must be used to ensure the "New Password" is

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



