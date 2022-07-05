#include <cs50.h>
#include <stdio.h>
#include <string.h>
#include <ctype.h>

#define ALPHABET_LENGTH 26
#define UPPERCASE_ASCII_MIN 65
#define LOWERCASE_ASCII_MIN 97 
#define CASE_OFFSET (UPPERCASE_ASCII_MIN - LOWERCASE_ASCII_MIN)

// Create struct to do conversion
struct letter_cipher_s
{
	char upper_char;
	char lower_char;
} letter_cipher_default = {'\0', '\0'};
typedef struct letter_cipher_s letter_cipher;


bool key_checker(char *key, letter_cipher *letter_map);

int main(int argc, string argv[])
{
	if (argc != 2)
	{
		puts("Usage: ./caesar key");
		return 1;
	}

	// Key checking also populates map 
	letter_cipher letter_map[ALPHABET_LENGTH] = { letter_cipher_default };
	if (!key_checker(argv[1], letter_map))
	{
		puts("Key must contain 26 characters.");
		return 1;
	}

	string plaintext = get_string("plaintext:  ");

	// Print ciphertext
	printf("ciphertext: ");
	for (int i = 0; plaintext[i] != '\0'; ++i)
	{
		int cipher_i = toupper(plaintext[i])-UPPERCASE_ASCII_MIN;
		printf(
            "%c", 
            isalpha(plaintext[i]) ? 
            (
                isupper(plaintext[i]) ? 
                letter_map[cipher_i].upper_char :
                letter_map[cipher_i].lower_char
            ) : plaintext[i]
        );
	}

	printf("\n");
	return 0;
}

bool key_checker(char *key, letter_cipher *letter_map)
{
	// Loop checks key is correct length & composed of alphbetic characters
    int key_dupes_map[ALPHABET_LENGTH] = {0};
	for (int i = 0, key_len = strlen(key);
	     ((key_len == ALPHABET_LENGTH) && (i < key_len) && isalpha(key[i]));
	     ++i)
	{
		// Check to see if letter has already been accounted for in cipher
        int cipher_i = toupper(key[i]) - UPPERCASE_ASCII_MIN;
		if (key_dupes_map[cipher_i])
		{
			break;
		}
        ++key_dupes_map[cipher_i];
        letter_map[i].upper_char = isupper(key[i]) ? key[i] : key[i] + CASE_OFFSET;
        letter_map[i].lower_char = islower(key[i]) ? key[i] : key[i] - CASE_OFFSET;
        if (i == ALPHABET_LENGTH-1)
        {
            return true;
        }
	}
	return false;
}
