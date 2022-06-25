// Modifies the volume of an audio file

#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

// Number of bytes in .wav header
const int HEADER_SIZE = 44;
typedef int16_t SAMPLE;
typedef uint8_t HEADER;
const int SAMPLE_SIZE = sizeof(SAMPLE);

int main(int argc, char *argv[])
{
    // Check command-line arguments
    if (argc != 4)
    {
        printf("Usage: ./volume input.wav output.wav factor\n");
        return 1;
    }

    // Open files and determine scaling factor
    FILE *input = fopen(argv[1], "r");
    if (input == NULL)
    {
        printf("Could not open file.\n");
        return 1;
    }

    FILE *output = fopen(argv[2], "w");
    if (output == NULL)
    {
        printf("Could not open file.\n");
        return 1;
    }

    float factor = atof(argv[3]);

    // TODO: Copy header from input file to output file
    HEADER header[HEADER_SIZE];
    fread(header, 1, HEADER_SIZE, input);
    fwrite(header, 1, HEADER_SIZE, output);

    // TODO: Read samples from input file and write updated data to output file
    SAMPLE buffer = 0;
    while (fread(&buffer, 1, SAMPLE_SIZE, input) == SAMPLE_SIZE)
    {
        SAMPLE scaled_sample = (SAMPLE)(buffer * factor); 
        fwrite(&scaled_sample, 1, SAMPLE_SIZE, output);
    }

    // Close files
    fclose(input);
    fclose(output);
}
