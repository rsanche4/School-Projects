/*******************************************************************************
 * Name    : shortestpaths.cpp
 * Author  : Rafael Sanchez & Nidhi Parekh
 * Version : 1.0
 * Date    : December 6, 2020
 * Description : This computes the shortest path using Floyd's Algorithm
 * Pledge : I pledge my honor that I have abided by the Stevens Honor System.
 ******************************************************************************/
#include <stdio.h>
#include <string.h>
#include <iostream>
#include <sstream>
#include <fstream>
#include <string>
#include <cstring>
#include <istream>
#include <vector>
#include <iterator>
#include <algorithm>
#include <array>
#include <limits>
#include <iomanip>

using namespace std;

long** letter_array;
long** distanceMatrixArray;

vector<char> branch_rec(int from, int to, long INF, int num_vert, long** path, vector<string> alphabet) {
	vector<char> base_case_vec;
	vector<char> null_vector;
	if (letter_array[from][to] == INF) {
		char first = static_cast<char>(from + 'A');
		char second = static_cast<char>(to + 'A');
		if (first == second) {
			base_case_vec.push_back(first);
		} else {
			//if they are not equal, then push both of them
			base_case_vec.push_back(first);
			base_case_vec.push_back(second);
		}
		return base_case_vec;

	} else if (letter_array[from][to] != INF) {
		vector<char> left_rec = branch_rec(from, letter_array[from][to], INF, num_vert, path, alphabet);
		vector<char> right_rec = branch_rec(letter_array[from][to], to, INF, num_vert, path, alphabet);
		left_rec.insert(left_rec.end(), right_rec.begin()+1, right_rec.end());
		return left_rec;
	}
	//This never runs, but I had to return something out of the if statements and I was unsure what
	return null_vector;
}

void recursing_path(long INF, int num_vert, long** path, vector<string> alphabet) {


	if (alphabet.size() == 1) {
		cout << "A -> A, distance: 0, path: A" << endl;
	} else {

		vector<char> THE_TRUTH_OF_HUMANKIND;
		int real_path;
		for (int i = 0; i < num_vert; i++) {
			for (int j = 0; j < num_vert; j++) {
				real_path = 0;
				if (path[i][j] != INF) {
					real_path = 1;
				}

				cout << alphabet[i+1] << " -> " << alphabet[j+1] << ", distance: ";
				//If there is a real path, then just output path
				if (real_path == 1) {
					cout << to_string(path[i][j]) << ", path: ";
				} else {
					cout << "infinity, path: none" << endl;
				}
				//Continue from where we left off if there is a path and perform recursion
				if (real_path == 1) {
					THE_TRUTH_OF_HUMANKIND = branch_rec(i, j, INF, num_vert, path, alphabet);
					for (unsigned int k = 0; k < THE_TRUTH_OF_HUMANKIND.size(); k++) {
						if (k == 0) {
							cout << THE_TRUTH_OF_HUMANKIND[0];
						} else {
							cout <<  " -> " << THE_TRUTH_OF_HUMANKIND[k];
						}
					}
					//Put the new line only after we are done with the for loop
					cout << endl;
				}
			}
		}
	}
}

long** floyd_algo(long** twoDarray, int num_vertices, long INF) {

	//The meat of Floyd's algorithm
	for (int k = 0; k < num_vertices; k++) {
		for (int i = 0; i < num_vertices; i++) {
			for (int j = 0; j < num_vertices; j++) {
				//Checking that there is no way to get an answer
				bool no_way = (twoDarray[i][k] == INF);
				bool no_way2 = (twoDarray[k][j] == INF);
				if (no_way) {
					continue;
				} else if (no_way2) {
					continue;
				} else {
					//The meat of Floyd's algorithm
					if (twoDarray[i][k] + twoDarray[k][j] < twoDarray[i][j]) {
						twoDarray[i][j] = twoDarray[i][k] + twoDarray[k][j];
						//update the intermediate array
						letter_array[i][j] = k;
					}
				}
			}
		}
	}
	return twoDarray;
}

int len(long val) {
	string valstring = to_string(val);
	return valstring.length();
}

/**
 * Displays the matrix on the screen formatted as a table.
 */
void display_table(long** matrix, string label, bool use_letters, int num_vertices, long INF) {
	cout << label << endl;
	long max_val = 0;
	for (int i = 0; i < num_vertices; i++) {
		for (int j = 0; j < num_vertices; j++) {
			long cell = matrix[i][j];
			if (cell < INF && cell > max_val) {
				max_val = matrix[i][j];
			}
		}
	}
	int max_cell_width = use_letters ? len(max_val) :
			len(max(static_cast<long>(num_vertices), max_val));
	cout << ' ';
	for (int j = 0; j < num_vertices; j++) {
		cout << setw(max_cell_width + 1) << static_cast<char>(j + 'A');
	}
	cout << endl;
	for (int i = 0; i < num_vertices; i++) {
		cout << static_cast<char>(i + 'A');
		for (int j = 0; j < num_vertices; j++) {
			cout << " " << setw(max_cell_width);
			if (matrix[i][j] == INF) {
				cout << "-";
			} else if (use_letters) {
				cout << static_cast<char>(matrix[i][j] + 'A');
			} else {
				cout << matrix[i][j];
			}
		}
		cout << endl;
	}
	cout << endl;
}

int main(int argc, const char *argv[]) {

	vector<string> ALPHABET{"NULL", "A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z"};

	//Create INFINITY AND BEYOND
	long INF = numeric_limits<long>::max();
	vector<string> alphabet_valid{"NULL"};

	// Make sure the right number of command line arguments exist.
	if (argc != 2) {
		cerr << "Usage: " << argv[0] << " <filename>" << endl;
		return 1;
	}
	// Create an ifstream object.
	ifstream input_file(argv[1]);
	// If it does not exist, print an error message.
	if (!input_file) {
		cerr << "Error: Cannot open file '" << argv[1] << "'." << endl;
		return 1;
	}
	// Add read errors to the list of exceptions the ifstream will handle.
	input_file.exceptions(ifstream::badbit);
	string line;
	istringstream iss;
	int m;
	try {
		unsigned int line_number = 1;

		//check for vertices
		getline(input_file, line);
		if (line_number == 1) {
			iss.str(line);
			if (!(iss >> m) || m > 26 || m < 1) {
				cerr << "Error: Invalid number of vertices '" << iss.str() << "' on line " << line_number << "." << endl;
				return 1;
			}
			++line_number;
		}

		//If there is no problem with this line, then go ahead and intialize the long array in the HEAP
		distanceMatrixArray = new long*[m];
		for (int i = 0; i < m; i++) {
			distanceMatrixArray[i] = new long[m];
		}

		//Fill this 2d array with INF
		for (int i = 0; i < m; i++) {
			for (int j = 0; j < m; j++) {
				distanceMatrixArray[i][j] = INF;
			}
		}

		//Fill in zeroes in the diagonal for the array from before
		for (int i = 0; i < m; i++) {
			distanceMatrixArray[i][i] = 0;
		}

		//On top of that, initialize our intermediate array in the HEAP as well
		letter_array = new long*[m];
		for (int i = 0; i < m; i++) {
			letter_array[i] = new long[m];
		}

		//fill the letter array with INF
		for (int i = 0; i < m; i++) {
			for (int j = 0; j < m; j++) {
				letter_array[i][j] = INF;
			}
		}

		// Use getline to read in a line.
		// See http://www.cplusplus.com/reference/string/string/getline/
		while (getline(input_file, line)) {

			istringstream iss(line);
			vector<string> line_contents((istream_iterator<string>(iss)), istream_iterator<string>());


			if (line_contents.size() < 3) {
				cerr << "Error: Invalid edge data '" << line << "' on line " << line_number << "." << endl;
				for (int i = 0; i < m; i++) {
					delete[] distanceMatrixArray[i];
					delete[] letter_array[i];
				}
				delete[] distanceMatrixArray;
				delete[] letter_array;
				return 1;
			}

			//check for correct naming of vertices using alphabet vector

			for (int i = 1; i <= m; i++) {
				alphabet_valid.push_back(ALPHABET[i]);
			}

			//checking for starting vertex
			for (unsigned int k = 1; k < alphabet_valid.size(); k++) {
				if (k == alphabet_valid.size()-1 && (line_contents[0].compare(alphabet_valid[k]) != 0)) {
					cerr << "Error: Starting vertex '" << line_contents[0] << "' on line " << line_number << " is not among valid values " << alphabet_valid[1] << "-" << alphabet_valid.back() << "." << endl;
					for (int i = 0; i < m; i++) {
						delete[] distanceMatrixArray[i];
						delete[] letter_array[i];
					}
					delete[] distanceMatrixArray;
					delete[] letter_array;
					return 1;
				}
				if (alphabet_valid[k].compare(line_contents[0]) == 0) {
					break;
				}
				if (alphabet_valid[k].compare(line_contents[0]) != 0) {
					continue;
				}
			}

			//checking for ending vertex
			for (unsigned int k = 1; k < alphabet_valid.size(); k++) {
				if (k == alphabet_valid.size()-1 && (line_contents[1].compare(alphabet_valid[k]) != 0)) {
					cerr << "Error: Ending vertex '" << line_contents[1] << "' on line " << line_number << " is not among valid values " << alphabet_valid[1] << "-" << alphabet_valid.back() << "." << endl;
					for (int i = 0; i < m; i++) {
						delete[] distanceMatrixArray[i];
						delete[] letter_array[i];
					}
					delete[] distanceMatrixArray;
					delete[] letter_array;
					return 1;
				}
				if (alphabet_valid[k].compare(line_contents[1]) == 0) {
					break;
				}
				if (alphabet_valid[k].compare(line_contents[1]) != 0) {
					continue;
				}

			}

			//check the edge weight is a positive integer
			istringstream iss2;
			iss2.str(line_contents[2]);
			int n;
			if (!(iss2 >> n) || (n < 1)) {
				cerr << "Error: Invalid edge weight '" << iss2.str() << "' on line " << line_number << "." << endl;
				for (int i = 0; i < m; i++) {
					delete[] distanceMatrixArray[i];
					delete[] letter_array[i];
				}
				delete[] distanceMatrixArray;
				delete[] letter_array;
				return 1;
			}


			//If everything is correct, we have an array with 0's in diagonal, and INF all the rest. Let's edit that and input our line contents
			long weight = (long)n;
			distanceMatrixArray[line_contents[0][0]-'A'][line_contents[1][0]-'A'] = weight;

			++line_number;
		}

		// Don't forget to close the file.
		input_file.close();
	} catch (const ifstream::failure &f) {
		cerr << "Error: An I/O error occurred reading '" << argv[1] << "'.";
		return 1;
	}

	//First display the distance Matrix as it is right now
	display_table(distanceMatrixArray, "Distance matrix:", false, m, INF);

	//Here do Floyd's algorithm on distanceMatrixArray and display it
	long** path = floyd_algo(distanceMatrixArray, m, INF);
	display_table(path, "Path lengths:", false, m, INF);
	display_table(letter_array, "Intermediate vertices:", true, m, INF);
	recursing_path(INF, m, path, alphabet_valid);

	//delete your heap and have a wonderful day sir
	for (int i = 0; i < m; i++) {
		delete[] distanceMatrixArray[i];
		delete[] letter_array[i];
	}
	delete[] distanceMatrixArray;
	delete[] letter_array;

	return 0;
}
