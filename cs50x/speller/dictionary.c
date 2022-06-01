#include <ctype.h>
#include <stdbool.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <strings.h>

#include "dictionary.h"


/* GLOBALS */

// Represents a node in a hash table
typedef struct node
{
	char word[LENGTH + 1];
	struct node *next;
}
node;

// Prototypes for helper functions
bool unload_linked_list(node *head);

// Global to track number of words loaded into dictionary
unsigned int loaded_words = 0;

// Choose number of buckets in hash table
const unsigned int N = 1000000;

// Hash table
node *table[N] = { NULL };


/* FUNCTIONS */

// Returns true if word is in dictionary, else false
bool check(const char *word)
{
	node *head = table[hash(word)];

	while (head)
	{
		if (strcasecmp(head->word, word) == 0)
		{
			return true;
		}
		head = head->next;
	}

	return false;
}


// Hashes word to a number
unsigned int hash(const char *word)
{
	return (((strlen(word) * toupper(word[1])) + toupper(word[0])) << 5) % N;
}


// Loads dictionary into memory, returning true if successful, else false
bool load(const char *dictionary)
{
	/* Open file */
	char word[LENGTH + 1];
	FILE *file = fopen(dictionary, "r");

	if (!file)
	{
		perror("Error in opening dictionary file!");
		return false;
	}

	/* Read dictionary into hash table line-wise */
	while (fscanf(file, "%s", word) != EOF)
	{
		unsigned int h  = hash(word);
		node         *w = (node *)malloc(sizeof(node));

		if (!w)
		{
			perror("Unable to allocate memory from heap to 'word' node!");
			return false;
		}

		strcpy(w->word, word);
		w->next  = table[h];
		table[h] = w;

		++loaded_words;
	}

	/* Close file */
	if (fclose(file))
	{
		perror("Error in closing dictionary file!");
		return false;
	}

	return true;
}


// Returns number of words in dictionary if loaded, else 0 if not yet loaded
unsigned int size(void)
{
	return loaded_words;
}


// Unloads dictionary from memory, returning true if successful, else false
bool unload(void)
{
	for (int h = 0; h < (int)N; ++h)
	{
		if ((table[h]) && (unload_linked_list(table[h]) == false))
		{
			return false;
		}
	}

	return true;
}


// Recursive helper function to unload linked list from memory
bool unload_linked_list(node *head)
{
	if (head->next)
	{
		unload_linked_list(head->next);
	}

	free(head);
	return true;
}
