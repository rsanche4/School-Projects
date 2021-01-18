/*******************************************************************************
 * Name    : quickselect.cpp
 * Author  : Rafael Sanchez
 * Version : 1.0
 * Date    : 10/23/2020
 * Description : Implements Quickselect
 * Pledge : I pledge my honor that I have abided by the Stevens Honor System.
 ******************************************************************************/
#include <iostream>
#include <sstream>
#include <algorithm>
#include <vector>
#include <iostream>

using namespace std;

void swap(int & a, int & b)
{
    int temp = a;
    a = b;
    b = temp;
}

size_t lomuto_partition(int array[], size_t left, size_t right) {
	int p = array[left];
	size_t s = left;
	for (size_t i = left + 1; i <= right; i++) {
		if (array[i] < p) {
			s += 1;
			swap(array[s], array[i]);
		}
	}
	swap(array[left], array[s]);
    return s;
}

int quick_select(int array[], size_t left, size_t right, size_t k) {
	size_t s;
	while (left <= right) {
		s = lomuto_partition(array, left, right);
		if (s == k - 1) {
			return array[s];
		} else if (s < k - 1) {
			left = s + 1;
		} else if (s > k - 1) {
			right = s - 1;
		}
	}
    return 0;
}

int quick_select(int array[], const size_t length, size_t k) {
    return quick_select(array, 0, length - 1, k);
}

int main(int argc, char *argv[]) {
    if (argc != 2) {
        cerr << "Usage: " << argv[0] << " <k>" << endl;
        return 1;
    }

    int k;
    istringstream iss;
    iss.str(argv[1]);
    if ( !(iss >> k) || k <= 0 ) {
        cerr << "Error: Invalid value '" << argv[1] << "' for k." << endl;
        return 1;
    }

    cout << "Enter sequence of integers, each followed by a space: " << flush;
    int value, index = 0;
    vector<int> values;
    string str;
    str.reserve(11);
    char c;
    iss.clear();
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

    int num_values = values.size();
    if (num_values == 0) {
        cerr << "Error: Sequence of integers not received." << endl;
        return 1;
    }

    // Error checking k against the size of the input
    if (values.size() < (unsigned)k) {
    	if (values.size() == 1) {
    		cerr << "Error: Cannot find smallest element " << k << " with only " << values.size() << " value." << endl;
    	} else {
    		cerr << "Error: Cannot find smallest element " << k << " with only " << values.size() << " values." << endl;
    	}
    	return 1;
    }
    // Calls the quick_select function and displays the result
    int *array = new int[num_values];
    for (int i = 0; i < num_values; i++) {
    	array[i] = values[i];
    }
    cout << "Smallest element " << k << ": " << quick_select(array, num_values, k) << endl;
    delete [] array;
    return 0;
}
