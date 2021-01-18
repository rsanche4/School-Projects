/*******************************************************************************
 * Name    : unique.cpp
 * Author  : Rafael Sanchez
 * Version : 1.0
 * Date    : September 25, 2020
 * Description : Finds if input has all unique lower case letters.
 * Pledge : I pledge my honor that I have abided by the Stevens Honor System.
 ******************************************************************************/
#include <iostream>
#include <cctype>
#include <string>

using namespace std;

bool is_all_lowercase(const string &s) {
    // TODO: returns true if all characters in string are lowercase
    // letters in the English alphabet; false otherwise.
	for (int i = 0; i < s.size(); i++) {

		if (isupper(s[i]) || isdigit(s[i])) {
			return false;
		}
		else {
			return true;
		}
	}

}

bool all_unique_letters(const string &s) {
    // TODO: returns true if all letters in string are unique, that is
    // no duplicates are found; false otherwise.
    // You may use only a single int for storage and work with bitwise
    // and bitshifting operators.
    // No credit will be given for other solutions.
	unsigned int vector = 0;
	unsigned int setter;
	unsigned int result;


	for (int i = 0; i < s.size(); i++) {

		setter = 1 << (s[i] - s[0]);

		result = vector & setter;
		if (result != 0) {
			return false;
		}

		vector = vector | setter;

	}
	return true;

}

int main(int argc, char * const argv[]) {
    // TODO: reads and parses command line arguments.
    // Calls other functions to produce correct output.

	if (argc == 1 || argc > 2) {
		cerr << "Usage: ./unique <string>" << endl;
	}
	else if (!is_all_lowercase(argv[1])) {
		cerr << "Error: String must contain only lowercase letters." << endl;
	}
	else if (all_unique_letters(argv[1])) {
		cout << "All letters are unique." << endl;
	}
	else {
		cout << "Duplicate letters found." << endl;
	}

}
