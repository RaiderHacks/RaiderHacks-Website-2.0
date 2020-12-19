To submit push requets, your public key

must be added to the RaiderHacks git

server.

Good news. The RaiderHacks SSH Git Server

actually accepted my ed25519-sk key, even

though it requires touch-based FIDO U2F.

This makes the Git Server I set up more

secure and trustworthy than even GitHub's

or even GitLab's. Neither of them support

U2F-based public key authentication at this

time, let alone U2F-based Ed25519 public

key authentication.


It is now my responsibility to assist the

RaiderHacks use this new Git server.

Everyone is required to digitally sign

their commits as reliable assurance that

they are the real person performing the 

git commit and not someone unwelcome.

Everyone contributing the RaiderHacks

website must posses their own U2F key

to digitally sign their git commits

with the help of GPG.

It is my responsibility, Tanveer, to

ensure that everyone understands how

that works.

----------------------------------------------

December 13, 2020

Dear All of You,

I have set aside an actual GPG key that I will

use to sign all my git commits. It is meant

to be exclusively used for all RaiderHacks's

development. I will send and teach all of

you how to use GPG.

The reason we care about this is so we have

reliable assurance git commits are coming from

the actual person that claims to be someone.

My GPG key fingerprint is: 175D5E863DF1BDEFBF34CE5AEDCB0582B9A05B98.

The GPG secret key must be passwordless for this

to work.

Testing with Joseph's trusted GPG key.

Test actually failed. Trying again with

C20F226A5A31A184C7FD5D4C063265EFAFADD1FF.

This key has the short ID format: 063265EFAFADD1FF.

For some reason, GPG keys protected by a secret passphrase

fail for git commits.

Second test for commit using C20F226A5A31A184C7FD5D4C063265EFAFADD1FF.

Third test.

Fourth test.

Fifth test.

Sixth test.

Seventh test.

Eighth test.

----------------------------------------------------------------------

So the reason git commit signatures were failing is because

I forgot one final step. You HAVE to activate gpg-agent using the

following command:

$export GPG_TTY=$(tty)

To ensure that your git commit signature works properly, do the following:

1. Enter the directory of your local repository 

2. git config user.signingkey [FULL GPG FINGERPRINT HERE; NEVER USE SHORT FINGERPRINT ID]

3. export GPG_TTY=$(tty) #This launches the gpg-agent. Without doing this, the signing

of the git commit WILL fail (https://docs.github.com/en/free-pro-team@latest/github/authenticating-to-github/telling-git-about-your-signing-key)

----------------------------------------------------------------------

December 14, 2020

Attempting to perform a git-push --signed=true push request

----------------------------------------------------------------------

December 14, 2020 8:04:37 AM

Attempting to digitally sign commit and push request--both!

----------------------------------------------------------------------

December 14, 2020 8:04:37 AM

Attempting to digitally sign both commit and push request--without

the Yubikey inserted into the computer. We need to make sure

this will NOT work without the Yubikey being readable by the computer!

----------------------------------------------------------------------

December 14, 2020 8:04:37 AM

Attempting to digitally sign both commit and push request with touch

policy enabled on Yubikey.

----------------------------------------------------------------------

December 14, 2020 10:09:47 PM

Attempting to sign git push properly now that receive.certNonceSeed (HMAC)

has been configured locally

----------------------------------------------------------------------

December 14, 2020 10:36:05 PM

Attempting to sign git push properly again. Found actual push certificates

after typing git-receive-pack.

----------------------------------------------------------------------

December 19, 2020 12:57:55 PM

Attempting to push remotely to auth only by default.
