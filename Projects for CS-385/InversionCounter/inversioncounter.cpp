/*******************************************************************************
 * Name    : inversioncounter.cpp
 * Author  : Rafael Sanchez & Nidhi Parekh
 * Version : 1.0
 * Date    : 10/25/2020
 * Description : Counts the number of inversions in an array.
 * Pledge : I pledge my honor that I have abided by the Stevens Honor System.
 ******************************************************************************/
#include <iostream>
#include <algorithm>
#include <sstream>
#include <vector>
#include <cstdio>
#include <cctype>
#include <cstring>
#include <string>
#include <array>

using namespace std;

// Function prototype.
static long mergesort(int array[], int scratch[], int low, int high);
/**
 * Counts the number of inversions in an array in theta(n^2) time.
 */
long count_inversions_slow(int array[], int length) {
    long count = 0;
	for (int i = 0; i < length; i++) {
    	for (int j = i + 1; j < length; j++) {
    		if (array[i] > array[j]) {
    			count++;
    		}
    	}
    }
	return count;
}

/**
 * Counts the number of inversions in an array in theta(n lg n) time.
 */
long count_inversions_fast(int array[], int length) {
    int *scratch = new int[length];
	for (int i = 0; i < length; i++) {
		scratch[i] = 0;
	}
	long result = mergesort(array, scratch, 0, length-1);
	delete [] scratch;
	return result;
}

static long mergesort(int array[], int scratch[], int low, int high) {
	long count = 0;
	if (low < high) {
		int middle = low + ((high - low) / 2);
		count = count + mergesort(array, scratch, low, middle);
		count = count + mergesort(array, scratch, middle + 1, high);
		int L = low;
		int H = middle + 1;
		for (int k = low; k <= high; k++) {
			if (L <= middle && (H > high || array[L] <= array[H])) {
				scratch[k] = array[L];
				L += 1;
			} else {
				count = count + (middle - L + 1);
				scratch[k] = array[H];
				H += 1;
			}
		}
		for (int k = low; k <= high; k++) {
			array[k] = scratch[k];
		}
	}
	return count;
}

int main(int argc, char *argv[]) {

	if (argc == 2 && strcmp(argv[1], "slow") != 0) {
		cerr << "Error: Unrecognized option '" << argv[1] << "'." << endl;
		return 1;
	} else if (argc > 2) {
		cerr << "Usage: ./inversioncounter [slow]" << endl;
		return 1;
	}

    cout << "Enter sequence of integers, each followed by a space: " << flush;

    istringstream iss;
    int value, index = 0;
    vector<int> values;
    string str;
    str.reserve(11);
    char c;
    while (true) {
        c = getchar();
        const bool eoln = c == '\r' || c == '\n';
        if (isspace(c) || eoln) {
            if (str.length() > 0) {
                iss.str(str);
                if (iss >> value) {
                    values.push_back(value);
                } else {
                    cerr << "Error: Non-integer value '" << str
                         << "' received at index " << index << "." << endl;
                    return 1;
                }
                iss.clear();
                ++index;
            }
            if (eoln) {
                break;
            }
            str.clear();
        } else {
            str += c;
        }
    }
    if (values.size() == 0) {
    	cerr << "Error: Sequence of integers not received." << endl;
    	return 1;
    }

    // This outputs our number of inversions in the given array
    if (argc == 2 && strcmp(argv[1], "slow") == 0) {
    	int *array = new int[values.size()];
    	for (size_t i = 0; i < values.size(); i++) {
    		array[i] = values[i];
    	}
    	cout << "Number of inversions: " << count_inversions_slow(array, values.size()) << endl;
    	delete [] array;
    	return 1;
    }
    	int *array = new int[values.size()];
       	for (size_t i = 0; i < values.size(); i++) {
       		array[i] = values[i];
       	}
       	cout << "Number of inversions: " << count_inversions_fast(array, values.size()) << endl;
       	delete [] array;
       	return 1;

    return 0;
}
