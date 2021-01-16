#include <stdio.h>
#include <string.h>
#include <time.h>
#include "/usr/include/sodium.h"
#include <emscripten/emscripten.h>

EMSCRIPTEN_KEEPALIVE int hash(char*argv)
{
	clock_t start, end;

	double cpu_time_used = 0;

	start = clock();
	
	unsigned char key[crypto_box_SEEDBYTES];

	unsigned char salt[crypto_pwhash_SALTBYTES];

	unsigned i = 0;
	
	char const * passwd = argv;
	
	if (crypto_pwhash(key,sizeof(key),argv,strnlen(passwd,4096),salt,1,1879048000,crypto_pwhash_ALG_DEFAULT) != 0 )
	{
		fprintf(stderr,"Error: out of memory\n");

		return 0;
	}

	end = clock();

	i = 0;

	while ( i < crypto_box_SEEDBYTES )
	{
		printf("%2x",key[i]);

		i++;
	}

	printf("\n");

	printf("Time Elapsed: %.6f\n\n",((double)(end-start))/CLOCKS_PER_SEC);

	printf("\n");

	return 3;
}

int main(void)
{
	return 0;
}
