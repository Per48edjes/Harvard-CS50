#include <cs50.h>
#include <stdio.h>

#define LUHN_CHECKSUM 0
#define LENGTH 1
#define FIRST_TWO_DIGITS 2

#define AMEX_LENGTH 15
#define AMEX_FIRST_DIGITS_1 34
#define AMEX_FIRST_DIGITS_2 37
#define MASTERCARD_LENGTH 16
#define MASTERCARD_FIRST_DIGITS_LOWER 51
#define MASTERCARD_FIRST_DIGITS_UPPER 55
#define VISA_LENGTH_1 MASTERCARD_LENGTH
#define VISA_LENGTH_2 13
#define VISA_FIRST_DIGIT 4

void cc_profile(long cc_number, int *cc_info);
bool is_amex(int *cc_info);
bool is_mastercard(int *cc_info);
bool is_visa(int *cc_info);

int main(void)
{
	long cc_number = get_long("Number: ");
	if (cc_number > 0)
	{
		// Use array to store info about `cc_number`
		int cc_info[3];
		cc_profile(cc_number, cc_info);

		// Check if valid card
		if (is_amex(cc_info) || is_mastercard(cc_info) || is_visa(cc_info))
		{
			return 0;
		}
	}
	printf("INVALID\n");
	return 0;
}

void cc_profile(long cc_number, int *cc_info)
{
	int len = 0;
	int first_two_digits;
	bool is_doubled_digit = false;
	int sum_doubled_digits = 0;
	int sum_single_digits = 0;
	for (int digit; cc_number > 0; cc_number /= 10, is_doubled_digit = !is_doubled_digit, ++len)
	{
		digit = cc_number % 10;
		if (is_doubled_digit)
		{
			digit *= 2;
			sum_doubled_digits += (digit / 10) + (digit % 10);
		}
		else
		{
			sum_single_digits += digit;
		}
		if (cc_number >= 10 && cc_number < 100)
		{
			first_two_digits = cc_number;
		}
	}

	cc_info[LENGTH] = len;
	cc_info[FIRST_TWO_DIGITS] = first_two_digits;
	cc_info[LUHN_CHECKSUM] = (sum_single_digits + sum_doubled_digits) % 10;
}

bool is_amex(int *cc_info)
{
	if  ((cc_info[LENGTH] == AMEX_LENGTH) &&
	     ((cc_info[FIRST_TWO_DIGITS] == AMEX_FIRST_DIGITS_1) || (cc_info[FIRST_TWO_DIGITS] == AMEX_FIRST_DIGITS_2)) &&
	     (cc_info[LUHN_CHECKSUM] == LUHN_CHECKSUM))
	{
		printf("AMEX\n");
		return true;
	}
	return false;
}

bool is_mastercard(int *cc_info)
{
	if  ((cc_info[LENGTH] == MASTERCARD_LENGTH) &&
	     (cc_info[FIRST_TWO_DIGITS] >= MASTERCARD_FIRST_DIGITS_LOWER) &&
	     (cc_info[FIRST_TWO_DIGITS] <= MASTERCARD_FIRST_DIGITS_UPPER) &&
	     (cc_info[LUHN_CHECKSUM] == LUHN_CHECKSUM))
	{
		printf("MASTERCARD\n");
		return true;
	}
	return false;
}

bool is_visa(int *cc_info)
{
	if  ((cc_info[LENGTH] == VISA_LENGTH_1 || cc_info[LENGTH] == VISA_LENGTH_2) &&
	     (cc_info[FIRST_TWO_DIGITS] / 10 == VISA_FIRST_DIGIT) &&
	     (cc_info[LUHN_CHECKSUM] == LUHN_CHECKSUM))
	{
		printf("VISA\n");
		return true;
	}
	return false;
}
