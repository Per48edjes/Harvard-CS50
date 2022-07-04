#include <cs50.h>
#include <stdio.h>
#include <ctype.h>
#include <string.h>
#include <math.h>

int count_letters(string text);
int count_words(string text);
int count_sentences(string text);

int main(void)
{
	string text = get_string("Text: ");
	printf("%s\n", text);

	double coleman_liau = (0.0588 * ((double)count_letters(text)/count_words(text) * 100)) \
	                      - (0.296 * ((double)count_sentences(text)/count_words(text)) * 100) \
	                      - 15.8;
	int reading_level = (int)round(coleman_liau);

	(reading_level < 1) ? printf("Before Grade 1\n") :
	(reading_level >= 16) ? printf("Grade 16+\n") :
	printf("Grade %i\n", reading_level);
}

int count_letters(string text)
{
	int num_letters = 0;
	for (int i = 0, text_len = strlen(text); i < text_len; ++i) {
		num_letters += isalpha(text[i]) ? 1 : 0;
	}
	return num_letters;
}

int count_words(string text)
{
	int num_spaces = 1;
	for (int i = 0, text_len = strlen(text); i < text_len; ++i) {
		num_spaces += (text[i] == ' ') ? 1 : 0;
	}
	return num_spaces;
}

int count_sentences(string text)
{
	int num_end_marks = 0;
	for (int i = 0, text_len = strlen(text); i < text_len; ++i) {
		num_end_marks += (text[i] == '!' || text[i] == '.' || text[i] == '?') ? 1 : 0;
	}
	return num_end_marks;
}
