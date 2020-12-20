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

	But...if the server simply made that process to short, it would be easier for

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

	but simply hashes the password into a hash all by itself. This hashing process on 

	the client's browser should take at least a second.

	
	2. At this point, the parameters for hashing using crypto_pwhash 

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
