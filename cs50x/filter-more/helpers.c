#include "helpers.h"
#include <stdio.h>
#include <math.h>

// Helper function to swap two pixels
void swap_pixels(RGBTRIPLE *a, RGBTRIPLE *b)
{
	RGBTRIPLE tmp = *a;
	*a = *b;
	*b = tmp;

	return;
}

// Helper function to apply Sobel algorithm to pixel
RGBTRIPLE sobel(int i, int j, int height, int width, RGBTRIPLE image[height][width])
{
	RGBTRIPLE new_pixel;
	int offsets[3] = { -1, 0, 1 };
	int Gx[3][3] = { {-1, 0, 1}, {-2, 0, 2}, {-1, 0, 1} };
	int Gy[3][3] = { {-1, -2, -1}, {0, 0, 0}, {1, 2, 1} };

	int horiz_sum[3] = { 0 };
	int vert_sum[3] = { 0 };

	for (int x = 0; x < 3; x++)
	{
		for (int y = 0; y < 3; y++)
		{
			if ((i+offsets[x] >= 0) && (i+offsets[x] < height) && (j+offsets[y] >=0) && (j+offsets[y] < width))
			{
				horiz_sum[0] += Gx[x][y] * image[i+offsets[x]][j+offsets[y]].rgbtRed;
				vert_sum[0] += Gy[x][y] * image[i+offsets[x]][j+offsets[y]].rgbtRed;
				horiz_sum[1] += Gx[x][y] * image[i+offsets[x]][j+offsets[y]].rgbtGreen;
				vert_sum[1] += Gy[x][y] * image[i+offsets[x]][j+offsets[y]].rgbtGreen;
				horiz_sum[2] += Gx[x][y] * image[i+offsets[x]][j+offsets[y]].rgbtBlue;
				vert_sum[2] += Gy[x][y] * image[i+offsets[x]][j+offsets[y]].rgbtBlue;
			}
		}
	}
	int red_value = (int)round(sqrt(pow(horiz_sum[0], 2) + pow(vert_sum[0], 2)));
	int green_value = (int)round(sqrt(pow(horiz_sum[1], 2) + pow(vert_sum[1], 2)));
	int blue_value = (int)round(sqrt(pow(horiz_sum[2], 2) + pow(vert_sum[2], 2)));
	new_pixel.rgbtRed = red_value > 255 ? 255 : red_value;
	new_pixel.rgbtGreen = green_value > 255 ? 255 : green_value;
	new_pixel.rgbtBlue = blue_value > 255 ? 255 : blue_value;
	return new_pixel;
}

// Convert image to grayscale
void grayscale(int height, int width, RGBTRIPLE image[height][width])
{
	for (int i = 0; i < height; ++i)
	{
		for (int j = 0; j < width; j++)
		{
			int greyscale_value = (int)round((image[i][j].rgbtRed + image[i][j].rgbtGreen + image[i][j].rgbtBlue) / (float)3);
			image[i][j].rgbtBlue = greyscale_value;
			image[i][j].rgbtGreen = greyscale_value;
			image[i][j].rgbtRed = greyscale_value;
		}
	}
	return;
}

// Reflect image horizontally
void reflect(int height, int width, RGBTRIPLE image[height][width])
{
	for (int i = 0; i < height; ++i)
	{
		for (int j = 0; j < width / 2; ++j)
		{
			swap_pixels(&image[i][j], &image[i][width-1-j]);
		}
	}
	return;
}

// Blur image
void blur(int height, int width, RGBTRIPLE image[height][width])
{
	int offsets[3] = { -1, 0, 1 };
	RGBTRIPLE new_image[height][width];

	for (int i = 0; i < height; ++i) {
		for (int j = 0; j < width; ++j)
		{
			int red_value = 0;
			int green_value = 0;
			int blue_value = 0;
			int pixel_count = 0;
			for (int x = 0; x < 3; x++)
			{
				for (int y = 0; y < 3; y++)
				{
					if ((i+offsets[x] >= 0) && (i+offsets[x] < height) && (j+offsets[y] >=0) && (j+offsets[y] < width))
					{
						++pixel_count;
						red_value += image[i+offsets[x]][j+offsets[y]].rgbtRed;
						green_value += image[i+offsets[x]][j+offsets[y]].rgbtGreen;
						blue_value += image[i+offsets[x]][j+offsets[y]].rgbtBlue;
					}
				}
			}
			new_image[i][j].rgbtRed = (int)round((float)red_value / pixel_count);
			new_image[i][j].rgbtGreen = (int)round((float)green_value / pixel_count);
			new_image[i][j].rgbtBlue = (int)round((float)blue_value / pixel_count);
		}
	}
	for (int i = 0; i < height; ++i)
	{
		for (int j = 0; j < width; ++j)
		{
			swap_pixels(&image[i][j], &new_image[i][j]);
		}
	}
	return;
}

// Detect edges
void edges(int height, int width, RGBTRIPLE image[height][width])
{
	RGBTRIPLE new_image[height][width];

	for (int i = 0; i < height; ++i) {
		for (int j = 0; j < width; ++j)
		{
			new_image[i][j] = sobel(i, j, height, width, image);
		}
	}
	for (int i = 0; i < height; ++i)
	{
		for (int j = 0; j < width; ++j)
		{
			swap_pixels(&image[i][j], &new_image[i][j]);
		}
	}
	return;
}
