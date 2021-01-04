The Argon2 Whitepaper recommends a simple proof-of-work takes 100 milliseconds,

regardless of the device used.

The following exceeds 100 milliseconds:

time echo "password" | argon2 spartacus -d -t 1 -k 126976 -p 8 -l 64 -e

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





