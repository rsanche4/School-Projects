/*******************************************************************************
 * Name    : stairclimber.cpp
 * Author  : Rafael Sanchez
 * Date    : September 26, 2020
 * Description : Finds ways to climb stairs.
 * Pledge : I pledge my honor that I have abided by the Stevens Honor System.
 ******************************************************************************/
#include <iostream>
#include <vector>
#include <algorithm>
#include <sstream>
#include <iomanip>
#include <string>
#include <cstring>

using namespace std;

vector< vector<int> > get_ways(int num_stairs) {
    // Returns a vector of vectors of ints representing
    // the different combinations of ways to climb num_stairs
    // stairs, moving up either 1, 2, or 3 stairs at a time.
	vector <vector <int>> ways;
	vector <vector <int>> result;

	if (num_stairs <= 0) {


		return ways = { {} };

	} else {
		for (int i = 1; i < 4; i++) {
			if (num_stairs >= i) {

				result = get_ways(num_stairs - i);

					for (unsigned int j = 0; j < result.size(); j++) {
						result.at(j).insert(result.at(j).begin(), i);

				}
				ways.insert(ways.end(), result.begin(), result.end());
			}
		}
	}
	return ways;

}

void display_ways(const vector< vector<int> > &ways) {
    // Displays the ways to climb stairs by iterating over
    // the vector of vectors and printing each combination.
	string ways_size_str = to_string(ways.size());

	if (ways.size() == 1) {
		cout << "1 way to climb 1 stair." << endl;
		cout << "1. [1]" << endl;
	}
	else {
		//output in the right format
		cout << ways.size() << " ways to climb " << ways.at(0).size() << " stairs." <<  endl;

		for (unsigned int i = 1; i <= ways.size(); i++) {

			cout << setw(ways_size_str.length());
			cout << i << ". ";
				for (unsigned int j = 0; j < ways.at(i-1).size(); j++) {
					if (j == 0 && j == ways.at(i-1).size() - 1) {
						cout << "[" << ways.at(i-1).at(0) << "]" << endl;
					}
					else if (j == 0) {
						cout << "[" << ways.at(i-1).at(0) << ", ";
					} else if (j == ways.at(i-1).size() - 1) {
						cout << ways.at(i-1).at(j) << "]" << endl;
					}
					else { cout << ways.at(i-1).at(j) << ", ";


					}
				}
		}


	}

}

int main(int argc, char * const argv[]) {

	istringstream iss;
	int m;

	if (argc == 2) {
	iss.str(argv[1]); }


	if (argc != 2) {
		cout << "Usage: ./stairclimber <number of stairs>" << endl;
	}
	else if (!(iss >> m)) {
		cout << "Error: Number of stairs must be a positive integer." << endl;
	}
	else if (stoi(argv[1]) < 1) {
		cout << "Error: Number of stairs must be a positive integer." << endl;
	}
	else {
		display_ways(get_ways(stoi(argv[1])));
	}

	return 0;
}
