#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <string.h>

typedef uint8_t BYTE;
#define BLOCK_SIZE 512

int main(int argc, char *argv[])
{
	if (argc != 2)
	{
		puts("Usage: ./recover [forensic image filename]");
		return 1;
	}

	FILE *infile = fopen(argv[1], "r");
	if (!infile)
	{
		puts("File did not open correctly! Check file pathname.");
		return 2;
	}

	BYTE buffer[BLOCK_SIZE] = { 0 };
	BYTE jpeg_signature_trio[] = { 0xff, 0xd8, 0xff };
	FILE *outfile = NULL;
	int outfile_counter = 0;
	char outfile_name[7 + 1];

	// Iterate over "memory card" file (`infile`)
	while (fread(buffer, 1, BLOCK_SIZE, infile) == BLOCK_SIZE)
	{
		// Look for JPEG signature
		if((memcmp(jpeg_signature_trio, buffer, 3) == 0) && ((buffer[3] >> 4) == 0b00001110))
		{
			// Close existing `outfile` if it exists
			if (outfile)
			{
				fclose(outfile);
			}
			// Once found, open `outfile` to write JPEG into
			sprintf(outfile_name, "%03d.jpg", outfile_counter++);
			outfile = fopen(outfile_name, "w");
		}
		// Write JPEG "block" into `outfile`
		if (outfile)
		{
		    fwrite(buffer, 1, BLOCK_SIZE, outfile);
		}
	}
	fclose(outfile);
	fclose(infile);
	return EXIT_SUCCESS;
}
