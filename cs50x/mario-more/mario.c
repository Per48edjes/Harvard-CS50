#include <stdio.h>
#include <string.h>

void bricks(int layer, char *row);

int main(void)
{
	// Prompt user for height of bricks
	int n, height, argc;
	do
	{
		printf("Height: "); argc = scanf("%i", &n);
		height = (argc == 1) ? n : 0;
	} while (!(height >= 1 && height <= 8));

	// Initialize row string
	int row_width = 2 * (height + 1);
	char row[row_width + 1]; row[row_width] = '\0'; memset(row, ' ', row_width);

	// Print bricks
	bricks(height, row);

	return 0;
}


void bricks(int layer, char *row)
{
	int row_width = strlen(row);
	int left = (row_width / 2) - layer - 1, right = (row_width / 2) + layer;

	if (layer > 1)
	{
		bricks(layer - 1, row);
	}

	row[left] = '#'; row[right] = '#';

	// Lop off trailing spaces to satisfy CS50 specs :)
	for (int i = 0; i < right + 1; ++i)
	{
		printf("%c", row[i]);
	}
	printf("\n");

	return;
}
