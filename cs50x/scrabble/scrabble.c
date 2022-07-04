#include <ctype.h>
#include <cs50.h>
#include <stdio.h>
#include <string.h>

#define UPPERCASE_ASCII_MIN 65

// Points assigned to each letter of the alphabet
int POINTS[] = {1, 3, 3, 2, 1, 4, 2, 4, 1, 8, 5, 1, 3, 1, 1, 3, 10, 1, 1, 1, 1, 4, 4, 8, 4, 10};

int compute_score(string word);

int main(void)
{
    // Get input words from both players
    string word1 = get_string("Player 1: ");
    string word2 = get_string("Player 2: ");

    // Score both words
    int score1 = compute_score(word1);
    int score2 = compute_score(word2);

    // Print the winner
    printf(
        "%s\n", 
        (score1 > score2) ? "Player 1 wins!" : 
        (score2 > score1) ? "Player 2 wins!" : "Tie!"
    );
}

int compute_score(string word)
{
    // Compute and return score for string
    int word_len = strlen(word);
    int score = 0;
    for (int i = 0, letter_idx; i < word_len; ++i)
    {
        letter_idx = (int)toupper(word[i]) - UPPERCASE_ASCII_MIN;
        score += (letter_idx >= 0 && letter_idx < 26) ? POINTS[letter_idx] : 0;
    }
    return score;
}
