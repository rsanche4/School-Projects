/*******************************************************************************
 * Name    : sqrt.cpp
 * Author  : Rafael Sanchez
 * Version : 1.0
 * Date    : September 3, 2020
 * Description : To approximate the square root of a number using Newton's method.
 * Pledge : I pledge my honor that I have abided by the Stevens Honor System.
 ******************************************************************************/
#include <iostream>
#include <limits>
#include <iomanip>
#include <cstring>
#include <stdlib.h>

using namespace std;

double sqrt(double num, double epsilon) {
	double next_guess, last_guess;
	last_guess = num;
	next_guess = (last_guess + num/last_guess) / 2;


	while ( abs(last_guess - next_guess) > epsilon) {
		last_guess = next_guess;
		next_guess = (last_guess + num/last_guess) / 2;
	}

	return next_guess;

}

int main(int argc, char *argv[]) {
	double num;
	num = atof(argv[1]);


	istringstream iss;
	//This checks that the right amount of arguments was given.
	if (argc > 3) {
		cerr << "Usage: ./sqrt <value> [epsilon]" << endl;
		return 1;
	}
	else if (argc == 1) {
		cerr << "Usage: ./sqrt <value> [epsilon]" << endl;
		return 1;
	}

	//Checks that you give it a double value.
	iss.str(argv[1]);
		if ( !(iss >> num) ) {
			cerr << "Error: Value argument must be a double." << endl;
			return 1;
		}



	//Checks that: 1) You don't give a negative input, 2) That it's not 0 or 1,
	//and 3) if Epsilon is given.
	if (atof(argv[1]) < 0.0) {
		cout << numeric_limits<double>::quiet_NaN();
		return 1;
	}
	else if (strcmp(argv[1], "0") == 0 || strcmp(argv[1], "1") == 0) {
		cout << fixed << setprecision(8) << atof(argv[1]) << endl;
		return 1;
	}

	else {
		if (argc == 2) {
			cout << fixed << setprecision(8) << sqrt(num, 1e-7) << endl;
			return 1;
		}
		else {
			double epsilon = atof(argv[2]);
			//Checks that your epsilon is a positive double.
			iss.clear();
			iss.str(argv[2]);
				if ( !(iss >> epsilon ) || (epsilon < 0) || (epsilon == 0)) {
				cerr << "Error: Epsilon argument must be a positive double." << endl;
				return 1;
				}
			cout << fixed << setprecision(8) << sqrt(num, epsilon) << endl;
			return 1;
		}
	}


	return 1;
}




