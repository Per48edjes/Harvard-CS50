#include <cs50.h>
#include <stdio.h>
#include <ctype.h>
#include <stdlib.h>
#include <string.h>

#define ALPHABET_LENGTH 26
#define UPPERCASE_ASCII_MIN 65
#define UPPERCASE_ASCII_MAX (UPPERCASE_ASCII_MIN + ALPHABET_LENGTH - 1)
#define LOWERCASE_ASCII_MIN 97
#define LOWERCASE_ASCII_MAX (LOWERCASE_ASCII_MIN + ALPHABET_LENGTH - 1)

char rotate(int character, int shift);

int main(int argc, string argv[])
{
	if (argc != 2)
	{
		puts("Usage: ./caesar key");
		return 1;
	}

	// Check that argument is an integer
	for (int i = 0; argv[1][i] != '\0'; i++)
	{
		if (!isdigit(argv[1][i]))
		{
			puts("Usage: ./caesar key");
			return 1;
		}
	}

	int key = atoi(argv[1]);
	string plaintext = get_string("plaintext:  ");

	// Print ciphertext
	printf("ciphertext: ");
	for (int i = 0; plaintext[i] != '\0'; ++i)
	{
		printf("%c", rotate(plaintext[i], key % ALPHABET_LENGTH));
	}

	printf("\n");
	return 0;
}

char rotate(int character, int shift)
{
	if (isalpha(character))
	{
		const int char_set_max = (isupper(character) ? UPPERCASE_ASCII_MAX : LOWERCASE_ASCII_MAX);
		const int char_set_min = (isupper(character) ? UPPERCASE_ASCII_MIN : LOWERCASE_ASCII_MIN);
		return
            (character + shift <= char_set_max) ? 
            character + shift : 
            char_set_min + ((character + shift - 1) % char_set_max);
	}
	return character;
}
