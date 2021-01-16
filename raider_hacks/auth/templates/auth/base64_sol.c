#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include <string.h>
#include "../sodium.h"

unsigned char table[65];

unsigned char decode_table[256];

void fill_table(void);

void fill_decode_table(void);

void base64_encode(unsigned char * input,const unsigned long long size,unsigned char *out)
{
	if ( size == 0 )
	{
		return;
	}

	unsigned char * output = out;

	unsigned long long int i = 0;

	unsigned char byte = 0, c = 0;

	while ( i < size )
	{
		if ( size - i == 1 )
		{
			byte = ( input[i] >> 2 );

			c = ( input[i] & 0x03 ) << 4;

			*output++ = table[byte];

			*output++ = table[c];

			*output++ = '=';

			*output++ = '=';

			i++;
		}

		else if ( size - i == 2 )
		{
			byte = ( input[i] >> 2 );
	
			c = ( input[i] & 0x03 ) << 4;

			*output++ = table[byte];

			i++;

			c |= ( input[i] & 0xf0 ) >> 4;

			*output++ = table[c];

			byte = ( input[i] & 0x0f) << 2;

			// END CROSSOVER

			*output++ = table[byte];

			*output++ = '=';

			i++;	
		}

		else
		{
			// copying code block for elif above

			//until END CROSSOVER

			byte = ( input[i] >> 2 );
	
			c = ( input[i] & 0x03 ) << 4;

			*output++ = table[byte];

			i++;

			c |= ( input[i] & 0xf0 ) >> 4;

			*output++ = table[c];

			byte = ( input[i] & 0x0f) << 2;

			// END CROSSOVER

			i++;	
			
			byte |= ( input[i] & 0xc0 ) >> 6;

			*output++ = table[byte];

			c = ( input[i] & 0x3f);
	
			*output++ = table[c];
			
			i++;
						
		}
	}

}

void base64_decode(unsigned char * input,unsigned long long int size,unsigned char * out)
{
	unsigned long long int i = 0;

	unsigned char byte = 0, c = 0, * output = out;

	while ( i < size )
	{
		byte = (decode_table[input[i]] << 2);

		i++;

		byte |= (decode_table[input[i]] >> 4);

		c = (decode_table[input[i]] & 0x0f ) << 4;

		*output++ = byte;

		i++;

		if ( input[i] == '=' ) { return; }

		c |= (decode_table[input[i]]) >> 2;

		*output++ = c;

		byte = (decode_table[input[i]] & 0x03 ) << 6;

		i++;

		if ( input[i] == '=') { return; }

		byte |= (decode_table[input[i]]);
	
		*output++ = byte;

		i++;

	}

}

void fill_table(void)
{

	unsigned char c = 'A';

	unsigned i = 0;
	
	memset(table,0x0,65*sizeof(unsigned char));

	while ( c <= 'Z' )
	{
		table[c-'A'] = c;

		c++;
	}
	
	i = 26;

	c = 'a';

	while ( c <= 'z')
	{
		table[c-'a'+i] = c;
		
		c++;
	}

	c = '0';

	i = 52;

	while ( c <= '9')
	{
		table[c-'0'+i] = c;
		
		c++;

	}

	table[62] = '+';

	table[63] = '/';

	table[64] = '=';
}

void fill_decode_table(void)
{
	unsigned i = 0;

	unsigned char c = 'A';
	
	memset(decode_table,0x0,256);

	while (i < 26)
	{
		decode_table[c] = i;

		i++;

		c++;
	}

	c = 'a';

	while (i < 52)
	{
		decode_table[c] = i;

		c++;
		
		i++;
	}

	c = '0';

	while ( i < 62)
	{
		decode_table[c] = i;

		c++;

		i++;

	}

	decode_table['+'-0] = 62;

	decode_table['/'-0] = 63;

}


int main(int argc,unsigned char ** argv)
{
	fill_table();

	fill_decode_table();
	
	unsigned long long int insize = 0;
	
	unsigned long long int trim = 0;
	
	unsigned long long int outsize = 0;

	unsigned long long int numpads = 0;

	unsigned long long int i = 0;


	if ( argv[1] != NULL )
	{
		outsize = (unsigned long long int)strnlen(argv[1],88);

		trim = outsize;

		i = outsize - 1;
		
		while ( ( i >= 0 ) && ( argv[1][i] == '=') )
		{
			numpads++;
		
			i--;
		}	

		trim -= numpads;

		insize = (unsigned long long int)(floor((trim*3.0)/4.0));
		
	}

	else
	{
		outsize = 0; 	

		insize = 0;
	}
	
	i = 0;

	if (sodium_init() == -1 )
	{
		fprintf(stderr,"sodium_init() failed\n");

		return 1;
	}
	
	unsigned char * decodeput = (unsigned char*)sodium_malloc(outsize+1);

	unsigned char * in = (unsigned char*)sodium_malloc(insize+1);

	memset(decodeput,0x0,outsize+1);

	memset(in,0x0,insize+1);
	
	base64_decode(argv[1],outsize,in);

	i = 0;

	printf("raw input:0x");

	while ( i < insize )
	{

		printf("%.2x",in[i]);
	
		i++;	
	}

	putchar(0xa);

	memset(decodeput,0x0,outsize+1);

	base64_encode(in,insize,decodeput);		
	
	printf("base64:%s\n",decodeput);

	memset(in,0x0,insize+1);
	
	memset(decodeput,0x0,outsize+1);
	
	sodium_free(in);

	sodium_free(decodeput);

	return 0;
}
//2
