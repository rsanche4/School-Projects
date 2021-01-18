/*******************************************************************************
 * Name    : waterjugpuzzle.cpp
 * Author  : Rafael Sanchez & Nidhi Parekh
 * Version : 1.0
 * Date    : October 20 2020
 * Description : Solves the famous Water Jug Puzzle using Breadth-first search.
 * Pledge : I pledge my honor that I have abided by the Stevens Honor System.
 ******************************************************************************/

#include <iostream>
#include <sstream>
#include <string>
#include <vector>
#include <queue>
#include <cstring>
#include <string>
#include <cstdlib>

using namespace std;

	// Struct to represent state of water in the jugs.

struct State {

    int a, b, c;
    string directions;
    State *parent;
    
    State(int _a, int _b, int _c, string _directions) : 
        a{_a}, b{_b}, c{_c}, directions{_directions}, parent{nullptr} { }

    // String representation of state in tuple form.
    string to_string() {
        ostringstream oss;
        oss << "(" << a << ", " << b << ", " << c << ")";
        return oss.str();

    }
};

	// This is the BFS algorithm that outputs order to complete the puzzle
void bfs(int a, int b, int c, int CAP_A, int CAP_B, int CAP_C, int GOAL_A, int GOAL_B, int GOAL_C) {

	// Initializing the Queue
	vector<string> outputStack;
	int found_solution = 0;
	queue<State *> queue;


	State * initial = new State(0, 0, 0, " ");
	initial->a = a;
	initial->b = b;
	initial->c = c;
	initial->directions = "Initial state.";
	initial->parent = nullptr;


	int ROWS = CAP_A + 1;
	int COLS = CAP_B + 1;


	// Creating a 2D array interwoven with a linked list
	State*** visited = new State**[ROWS];
	for (int i = 0; i < ROWS; ++i) {
	  visited[i] = new State*[COLS];
	}
	for (int i = 0; i < ROWS; ++i) {
	  for (int j = 0; j < COLS; ++j) {
	    visited[i][j] = nullptr;
	  }
	}

	queue.push(initial);

	// Start of the BFS algorithm
	while (!(queue.empty())) {

		State * current = queue.front();
		queue.pop();

		// If current State meets the goal, then you output the order in which to pour water into each jug to reach that goal State.
		if (current->a == GOAL_A && current->b == GOAL_B && current->c == GOAL_C) {
			cout << State(a, b, c, "Initial state.").directions << " " << State(a, b, c, "Initial state.").to_string() << endl;
			State * temp = current;
			string outputString;
			while (current->parent != nullptr) {
				outputString = current->directions + " " + current->to_string();
				outputStack.push_back(outputString);
				current = current->parent;
			}

			while (!(outputStack.empty())) {
				cout << outputStack.back() << endl;
				outputStack.pop_back();
			}
			found_solution =  1;
			delete temp;
			break;
		}
		// If State already seen, then continue to the next iteration of the loop.
		if (visited[current->a][current->b] != nullptr) {
				delete current;
				continue;
			}

				// Set the current to visited
				visited[current->a][current->b] = current;

				// Pour from Jug C to Jug A
				State * ca = new State(0, 0, 0, " ");
				ca->a = current->a;
				ca->b = current->b;
				ca->c = current->c;
				if (ca->c != 0 && ca->a != CAP_A) {
					while (ca->c != 0 && ca->a != CAP_A) {
						ca->c = ca->c - 1;
						ca->a = ca->a + 1;


					}
					// Setting the parent of the state CA to the current
					ca->parent = current;
					if (current->c - ca->c == 1) {
						ca->directions = "Pour " + to_string(current->c - ca->c) + " gallon from C to A.";
					} else {
					ca->directions = "Pour " + to_string(current->c - ca->c) + " gallons from C to A.";

					}
					queue.push(ca);
				} else {
					delete ca;
				}

				// Pour from Jug B to Jug A
				State * ba = new State(0, 0, 0, " ");
				ba->a = current->a;
				ba->b = current->b;
				ba->c = current->c;
				if (ba->b != 0 && ba->a != CAP_A) {
					while (ba->b != 0 && ba->a != CAP_A) {
						ba->b = ba->b - 1;
						ba->a = ba->a + 1;
					}

					// Setting the parent of the state BA to the current
					ba->parent = current;
					if (current->b - ba->b == 1) {
						ba->directions = "Pour " + to_string(current->b - ba->b) + " gallon from B to A.";
					} else {
					ba->directions = "Pour " + to_string(current->b - ba->b) + " gallons from B to A.";

					}
					queue.push(ba);

				} else {
					delete ba;
				}
				// Pour from Jug C to Jug B
				State * cb = new State(0, 0, 0, " ");
				cb->a = current->a;
				cb->b = current->b;
				cb->c = current->c;
				if (cb->c != 0 && cb->b != CAP_B) {
					while (cb->c != 0 && cb->b != CAP_B) {
						cb->c = cb->c - 1;
						cb->b = cb->b + 1;
					}
					// Setting the parent of the state CB to the current
					cb->parent = current;
					if (current->c - cb->c == 1) {
						cb->directions = "Pour " + to_string(current->c - cb->c) + " gallon from C to B.";
					} else {
					cb->directions = "Pour " + to_string(current->c - cb->c) + " gallons from C to B.";

					}
					queue.push(cb);
				} else {
					delete cb;
				}

				// Pour from Jug A to Jug B
				State * ab = new State(0, 0, 0, " ");
				ab->a = current->a;
				ab->b = current->b;
				ab->c = current->c;
				if (ab->a != 0 && ab->b != CAP_B) {
					while (ab->a != 0 && ab->b != CAP_B) {
						ab->a = ab->a - 1;
						ab->b = ab->b + 1;
					}
					// Setting the parent of the state AB to the current
					ab->parent = current;
					if (current->a - ab->a == 1) {
						ab->directions = "Pour " + to_string(current->a - ab->a) + " gallon from A to B.";
					} else {
					ab->directions = "Pour " + to_string(current->a - ab->a) + " gallons from A to B.";

					}
					queue.push(ab);
				} else {
					delete ab;
				}

				// Pour from Jug B to Jug C
				State * bc = new State(0, 0, 0, " ");
				bc->a = current->a;
				bc->b = current->b;
				bc->c = current->c;
				if (bc->b != 0 && bc->c != CAP_C) {
					while (bc->b != 0 && bc->c != CAP_C) {
						bc->b = bc->b - 1;
						bc->c = bc->c + 1;
					}
					// Setting the parent of the state BC to the current
					bc->parent = current;
					if (current->b - bc->b == 1) {
						bc->directions = "Pour " + to_string(current->b - bc->b) + " gallon from B to C.";
					} else {
					bc->directions = "Pour " + to_string(current->b - bc->b) + " gallons from B to C.";

					}
					queue.push(bc);
				} else {
					delete bc;
				}


				// Pour from Jug A to Jug C
				State * ac = new State(0, 0, 0, " ");
				ac->a = current->a;
				ac->b = current->b;
				ac->c = current->c;
				if (ac->a != 0 && ac->c != CAP_C) {
					while (ac->a != 0 && ac->c != CAP_C) {
						ac->a = ac->a - 1;
						ac->c = ac->c + 1;
						}

					// Setting the parent of the state AC to the current
					ac->parent = current;
					if (current->a - ac->a == 1) {
						ac->directions = "Pour " + to_string(current->a - ac->a) + " gallon from A to C.";
					} else {
					ac->directions = "Pour " + to_string(current->a - ac->a) + " gallons from A to C.";

					}
					queue.push(ac);
				} else {
					delete ac;
				}

			}


	// If there is no solution, print that.
	if (found_solution == 0) {
		cout << "No solution." << endl;
	}

	// If the queue is not empty, delete whatever is in it
	while (!queue.empty()) {
		delete queue.front();
		queue.pop();
	}

	// Delete the 2d Array (visited)
	for (int i = 0; i < ROWS; ++i) {
		for (int j = 0; j < COLS; ++j) {
			delete visited[i][j];
		}
	}

	// Delete the visited
	for (int i = 0; i < ROWS; ++i) {
		delete [] visited[i];
	}
	// Also deleting the visited
	delete [] visited;



}


// Checks if letters or negative numbers were given
bool invalid_capacity_for_jug_x(string cap_a, string cap_b, string cap_c, string goal_a, string goal_b, string goal_c) {

	istringstream issA;
	int mA;

	istringstream issB;
	int mB;

	istringstream issC;
	int mC;

	istringstream issGA;
	int mGA;

	istringstream issGB;
	int mGB;

	istringstream issGC;
	int mGC;


	issA.str(cap_a);
	if (!(issA >> mA) || mA <= 0) {
		cout << "Error: Invalid capacity '" << cap_a << "' for jug A." << endl;
		return true;
	}

	issB.str(cap_b);
	if (!(issB >> mB) || mB <= 0) {
			cout << "Error: Invalid capacity '" << cap_b << "' for jug B." << endl;
			return true;
		}

	issC.str(cap_c);
	if (!(issC >> mC) || mC <= 0) {
			cout << "Error: Invalid capacity '" << cap_c << "' for jug C." << endl;
			return true;
			}


	issGA.str(goal_a);
		if (!(issGA >> mGA) || mGA < 0) {
				cout << "Error: Invalid goal '" << goal_a << "' for jug A." << endl;
				return true;
				}

	issGB.str(goal_b);
		if (!(issGB >> mGB) || mGB < 0) {
				cout << "Error: Invalid goal '" << goal_b << "' for jug B." << endl;
				return true;
				}

	issGC.str(goal_c);
		if (!(issGC >> mGC) || mGC < 0) {
				cout << "Error: Invalid goal '" << goal_c << "' for jug C." << endl;
				return true;
				}

		return false;



}



int main(int argc, char * const argv[]) {

	// Checking for the right input
	bool invalid_cap = true;

	if (argc == 1) {
		cout << "Usage: ./waterjugpuzzle <cap A> <cap B> <cap C> <goal A> <goal B> <goal C>" << endl;
	} else if (argc != 7) {
		cout << "Usage: ./waterjugpuzzle <cap A> <cap B> <cap C> <goal A> <goal B> <goal C>" << endl;
	} else {
		invalid_cap = invalid_capacity_for_jug_x(string(argv[1]), string(argv[2]), string(argv[3]), string(argv[4]), string(argv[5]), string(argv[6]) );

	}


	if (invalid_cap == false) {

		State initial(0, 0, stoi(argv[3]), "Initial state.");

		if (stoi(argv[4]) > stoi(argv[1]) ) {
			cout << "Error: Goal cannot exceed capacity of jug A." << endl;
		} else if (stoi(argv[5]) > stoi(argv[2])) {
			cout << "Error: Goal cannot exceed capacity of jug B." << endl;
		} else if (stoi(argv[6]) > stoi(argv[3])) {
			cout << "Error: Goal cannot exceed capacity of jug C." << endl;
		} else if (stoi(argv[3]) != stoi(argv[4]) + stoi(argv[5]) + stoi(argv[6]) ) {
			cout << "Error: Total gallons in goal state must be equal to the capacity of jug C." << endl;
		} else if (initial.a == stoi(argv[4]) && initial.b == stoi(argv[5]) && initial.c == stoi(argv[6])) {
			cout << initial.directions << " " << initial.to_string() << endl;
		} else {

			bfs(0, 0, stoi(argv[3]), stoi(argv[1]), stoi(argv[2]), stoi(argv[3]), stoi(argv[4]), stoi(argv[5]), stoi(argv[6]));


		}

	}
	   return 0;
}
