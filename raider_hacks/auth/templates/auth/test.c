#include <stdio.h>
#include <string.h>
#include <time.h>
#include "/usr/include/sodium.h"

int main(void)
{
	clock_t start, end;

	double cpu_time_used = 0;

	start = clock();

	if ( sodium_init() < 0 )
	{
		return 1;
	}

	
	unsigned char key[crypto_box_SEEDBYTES];

	unsigned char salt[crypto_pwhash_SALTBYTES];

	char const * passwd = "Password\0";
	
	if (crypto_pwhash(key,sizeof(key),passwd,strnlen(passwd,64),salt,1,1879048000,crypto_pwhash_ALG_DEFAULT) != 0 )
	{
		fprintf(stderr,"Error: out of memory\n");
		
		exit(1);
	}

	end = clock();

	printf("Time Elapsed: %.6f\n",((double)(end-start))/CLOCKS_PER_SEC);

	return 0;
}

