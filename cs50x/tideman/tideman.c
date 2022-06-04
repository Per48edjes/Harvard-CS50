#include <cs50.h>
#include <stdio.h>
#include <string.h>
#include <stdlib.h>

// Max number of candidates
#define MAX 9

// preferences[i][j] is number of voters who prefer i over j
int preferences[MAX][MAX] = {{ 0 }};

// locked[i][j] means i is locked in over j
bool locked[MAX][MAX];

// Each pair has a winner, loser
typedef struct
{
	int winner;
	int loser;
}
pair;

// Array of candidates
string candidates[MAX];
pair pairs[MAX * (MAX - 1) / 2];

int pair_count;
int candidate_count;

// Function prototypes
bool vote(int rank, string name, int ranks[]);
void record_preferences(int ranks[]);
void add_pairs(void);
void sort_pairs(void);
void lock_pairs(void);
void print_winner(void);
int compare_win_strengths(const void *p, const void *q);
bool check_is_cycle(pair p, int source);

int main(int argc, string argv[])
{
	// Check for invalid usage
	if (argc < 2)
	{
		printf("Usage: tideman [candidate ...]\n");
		return 1;
	}

	// Populate array of candidates
	candidate_count = argc - 1;
	if (candidate_count > MAX)
	{
		printf("Maximum number of candidates is %i\n", MAX);
		return 2;
	}
	for (int i = 0; i < candidate_count; i++)
	{
		candidates[i] = argv[i + 1];
	}

	// Clear graph of locked in pairs
	for (int i = 0; i < candidate_count; i++)
	{
		for (int j = 0; j < candidate_count; j++)
		{
			locked[i][j] = false;
		}
	}

	pair_count = 0;
	int voter_count = get_int("Number of voters: ");

	// Query for votes
	for (int i = 0; i < voter_count; i++)
	{
		// ranks[i] is voter's ith preference
		int ranks[candidate_count];

		// Query for each rank
		for (int j = 0; j < candidate_count; j++)
		{
			string name = get_string("Rank %i: ", j + 1);

			if (!vote(j, name, ranks))
			{
				printf("Invalid vote.\n");
				return 3;
			}
		}

		record_preferences(ranks);

		printf("\n");
	}

	add_pairs();
	sort_pairs();
	lock_pairs();
	print_winner();
	return 0;
}

// Update ranks given a new vote
bool vote(int rank, string name, int ranks[])
{
	for (int i = 0; i < candidate_count; ++i)
	{
		if (strcmp(name, candidates[i]) == 0)
		{
			ranks[rank] = i;
			return true;
		}
	}
	return false;
}

// Update preferences given one voter's ranks
void record_preferences(int ranks[])
{
	bool is_candidate_accounted[MAX] = {
		false
	};
	for (int r = 0; r < candidate_count; ++r)
	{
		int i = ranks[r];
		for (int j = 0; j < candidate_count; ++j)
		{
			if (i != j && !is_candidate_accounted[j])
			{
				++preferences[i][j];
			}
			is_candidate_accounted[i] = true;
		}
	}

	return;
}

// Record pairs of candidates where one is preferred over the other
void add_pairs(void)
{
	for (int i = 0; i < candidate_count; ++i) {
		for (int j = i + 1; j < candidate_count; ++j) {
			if (preferences[i][j] > preferences[j][i]) {
				pairs[pair_count].winner = i;
				pairs[pair_count].loser = j;
			} else if (preferences[i][j] < preferences[j][i]) {
				pairs[pair_count].winner = j;
				pairs[pair_count].loser = i;
			} else {
				continue;
			}
			++pair_count;
		}
	}
	return;
}

// Sort pairs in decreasing order by strength of victory
void sort_pairs(void)
{
	qsort(pairs, pair_count, sizeof(pair), compare_win_strengths);
	return;
}

// Lock pairs into the candidate graph in order, without creating cycles
void lock_pairs(void)
{
	for (int i = 0; i < pair_count; ++i) {
		locked[pairs[i].winner][pairs[i].loser] = true;
		if (check_is_cycle(pairs[i], pairs[i].winner)) {
			locked[pairs[i].winner][pairs[i].loser] = false;
		}
	}
	return;
}

// Print the winner of the election
void print_winner(void)
{
	for (int j = 0; j < candidate_count; j++) {
		int inbound_edges = 0;
		for (int i = 0; i < candidate_count; ++i) {
			inbound_edges += (int)locked[i][j];
		}
		if (inbound_edges == 0) {
			printf("%s\n", candidates[j]);
			return;
		}
	}
}


int compare_win_strengths(const void *p, const void *q)
{
	/* Descending order */
	if (preferences[((pair *)p)->winner][((pair *)p)->loser] > preferences[((pair *)q)->winner][((pair *)q)->loser]) {
		return -1;
	} else if (preferences[((pair *)p)->winner][((pair *)p)->loser] < preferences[((pair *)q)->winner][((pair *)q)->loser]) {
		return 1;
	} else {
		return 0;
	}
}


bool check_is_cycle(pair p, int source)
{
	/* Base case */
	if (p.loser == source)
	{
		return true;
	}

	/* Recursive case */
	else
	{
		for (int j = 0; j < candidate_count; j++) {
			if (locked[p.loser][j]) {
				pair next_p = {
					.winner = p.loser, .loser = j
				};
				if (check_is_cycle(next_p, source)) {
					return true;
				}
			}
		}
		return false;
	}
}
