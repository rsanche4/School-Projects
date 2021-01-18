/*******************************************************************************
 * Name    : sieve.cpp
 * Author  : Rafael Sanchez
 * Date    : September 18, 2020
 * Description : Algorithm for the Sieve of Eratosthenes.
 * Pledge : I pledge my honor that I have abided by the Stevens Honor System.
 ******************************************************************************/
#include <cmath>
#include <iomanip>
#include <iostream>
#include <sstream>
#include <string>

using namespace std;

class PrimesSieve {
public:
    PrimesSieve(int limit);

    ~PrimesSieve() {
        delete [] is_prime_;
    }

    int num_primes() const {
        return num_primes_;
    }

    void display_primes() const;

private:
    // Instance variables
    bool * const is_prime_;
    const int limit_;
    int num_primes_, max_prime_;

    // Method declarations
    int count_num_primes() const;
    void sieve();
    static int num_digits(int num);
};

PrimesSieve::PrimesSieve(int limit) :
        is_prime_{new bool[limit + 1]}, limit_{limit} {
    sieve();

}

void PrimesSieve::display_primes() const {
	cout << endl;
	cout << "Number of primes found: " << num_primes() << endl;
	cout << "Primes up to " << limit_ << ":" << endl;


	const int max_prime_width = num_digits(max_prime_),
	 primes_per_row = 80 / (max_prime_width + 1);


    // Wrote code to display the primes in the format specified in the
    // requirements document.


			if (num_primes_ <= primes_per_row) {
				for (int i = 0; i <= limit_; i++) {

					if (is_prime_[i]) {

						if (i == max_prime_) {
								cout << i;
							}
						else {
							cout << i << " ";
							}
					}
				}
			}
			 else {
				 int count = 1;
				 for (int i = 0; i <= limit_; i++) {
					 if (is_prime_[i]) {

					 cout << setw(max_prime_width);

					 if(max_prime_ == i && count == primes_per_row) {
						 cout << i;
						 cout << endl;
					 }
					 else if (max_prime_ == i) {
						 cout << i;
						 cout << endl;
					 }
					 else if (count == primes_per_row) {
						 cout << i << endl;
						 count = 1;
					 }
					 else {
						 cout << i << " ";
						 count += 1;
					 }
					}
				 }

			}


		}



int PrimesSieve::count_num_primes() const {
	//Returns number of primes found.
	int count = 0;
	for (int i = 0; i <= limit_; i++) {
		if (is_prime_[i]) {
		count = count + 1;
		}
	}
    return count;
}

void PrimesSieve::sieve() {
	is_prime_[0] = false;
	is_prime_[1] = false;

	for (int k = 2; k <= limit_; k++) {
		is_prime_[k] = true;
	}

	int sqrt_n = sqrt(limit_);
	for (int i = 2; i <= sqrt_n; i++) {
		if (is_prime_[i] == true) {
			for (int j = pow(i, 2); j <= limit_; j = j + i) {
				is_prime_[j] = false;
			}
		}
	}

	num_primes_ = count_num_primes();

		int k = limit_;
	    if (is_prime_[k])
	    {
	    	max_prime_ = k;
	    }
	    else {
	    for (int i = limit_; is_prime_[i] == false; i--) {
	        if (is_prime_[i-1]) {
	            max_prime_ = i-1;
	        }
	    }
	    }

    //The sieve algorithm
	//num_primes_ and max_prime_ are initialized in sieve()
}

int PrimesSieve::num_digits(int num) {
    // Determines how many digits are in an integer.
    // No strings were needed. Kept dividing by 10.

	    int count = 0;
		if ((num/10) == 0) {
		    count += 1;
			return count;
		}
		else {
		   count += 1;
		return count + num_digits(num/10);
		}
}

int main() {
    cout << "**************************** " <<  "Sieve of Eratosthenes" <<
            " ****************************" << endl;
    cout << "Search for primes up to: ";
    string limit_str;
    cin >> limit_str;
    int limit = 0;

    // Used stringstream for conversion. Didn't forget to #include <sstream>
    istringstream(limit_str) >> limit;

    // Check for error.
    if ( !(istringstream(limit_str) >> limit) ) {
        cerr << "Error: Input is not an integer." << endl;
        return 1;
    }
    if (limit < 2) {
        cerr << "Error: Input must be an integer >= 2." << endl;
        return 1;
    }
    //But if there is no error:
    else {
    	PrimesSieve sieve(limit);
    	sieve.display_primes();

    }


    return 0;
}




