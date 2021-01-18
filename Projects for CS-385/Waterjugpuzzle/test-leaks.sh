#!/bin/bash

echo "Leak tester v0.1 by Justin O'Boyle"
echo "Make project..."
make

echo "Running tests. Run individual test with --verbose to debug."


echo ---------- CASE 1 2 3 4 5 6 7 ----------
valgrind -s --leak-check=full --show-leak-kinds=all --track-origins=yes ./waterjugpuzzle 1 2 3 4 5 6 7




echo ---------- CASE x 2 3 4 5 6 ----------
valgrind -s --leak-check=full --show-leak-kinds=all --track-origins=yes ./waterjugpuzzle x 2 3 4 5 6




echo ---------- CASE 1 -2 3 4 5 6 ----------
valgrind -s --leak-check=full --show-leak-kinds=all --track-origins=yes ./waterjugpuzzle 1 -2 3 4 5 6




echo ---------- CASE 1 2 0 4 5 6 ----------
valgrind -s --leak-check=full --show-leak-kinds=all --track-origins=yes ./waterjugpuzzle 1 2 0 4 5 6




echo ---------- CASE 1 2 3 y 5 6 ----------
valgrind -s --leak-check=full --show-leak-kinds=all --track-origins=yes ./waterjugpuzzle 1 2 3 y 5 6




echo ---------- CASE 1 2 3 4 -5 6 ----------
valgrind -s --leak-check=full --show-leak-kinds=all --track-origins=yes ./waterjugpuzzle 1 2 3 4 -5 6




echo ---------- CASE 1 2 3 4 5 -1 ----------
valgrind -s --leak-check=full --show-leak-kinds=all --track-origins=yes ./waterjugpuzzle 1 2 3 4 5 -1




echo ---------- CASE 3 5 8 4 0 4 ----------
valgrind -s --leak-check=full --show-leak-kinds=all --track-origins=yes ./waterjugpuzzle 3 5 8 4 0 4




echo ---------- CASE 3 5 8 0 6 2 ----------
valgrind -s --leak-check=full --show-leak-kinds=all --track-origins=yes ./waterjugpuzzle 3 5 8 0 6 2




echo ---------- CASE 3 5 8 0 0 9 ----------
valgrind -s --leak-check=full --show-leak-kinds=all --track-origins=yes ./waterjugpuzzle 3 5 8 0 0 9




echo ---------- CASE 3 5 8 2 1 4 ----------
valgrind -s --leak-check=full --show-leak-kinds=all --track-origins=yes ./waterjugpuzzle 3 5 8 2 1 4




echo ---------- CASE 6 7 10 5 5 0 ----------
valgrind -s --leak-check=full --show-leak-kinds=all --track-origins=yes ./waterjugpuzzle 6 7 10 5 5 0




echo ---------- CASE 30 45 50 25 25 0 ----------
valgrind -s --leak-check=full --show-leak-kinds=all --track-origins=yes ./waterjugpuzzle 30 45 50 25 25 0




echo ---------- CASE 3 5 8 2 1 5 ----------
valgrind -s --leak-check=full --show-leak-kinds=all --track-origins=yes ./waterjugpuzzle 3 5 8 2 1 5




echo ---------- CASE 5 7 10 3 3 4 ----------
valgrind -s --leak-check=full --show-leak-kinds=all --track-origins=yes ./waterjugpuzzle 5 7 10 3 3 4




echo ---------- CASE 6 7 10 0 0 10 ----------
valgrind -s --leak-check=full --show-leak-kinds=all --track-origins=yes ./waterjugpuzzle 6 7 10 0 0 10




echo ---------- CASE 3 5 8 0 5 3 ----------
valgrind -s --leak-check=full --show-leak-kinds=all --track-origins=yes ./waterjugpuzzle 3 5 8 0 5 3




echo ---------- CASE 3 5 8 0 3 5 ----------
valgrind -s --leak-check=full --show-leak-kinds=all --track-origins=yes ./waterjugpuzzle 3 5 8 0 3 5




echo ---------- CASE 1 3 4 0 2 2 ----------
valgrind -s --leak-check=full --show-leak-kinds=all --track-origins=yes ./waterjugpuzzle 1 3 4 0 2 2




echo ---------- CASE 3 5 8 0 2 6 ----------
valgrind -s --leak-check=full --show-leak-kinds=all --track-origins=yes ./waterjugpuzzle 3 5 8 0 2 6




echo ---------- CASE 3 5 8 0 4 4 ----------
valgrind -s --leak-check=full --show-leak-kinds=all --track-origins=yes ./waterjugpuzzle 3 5 8 0 4 4




echo ---------- CASE 4 7 10 0 5 5 ----------
valgrind -s --leak-check=full --show-leak-kinds=all --track-origins=yes ./waterjugpuzzle 4 7 10 0 5 5




echo ---------- CASE 8 17 20 0 10 10 ----------
valgrind -s --leak-check=full --show-leak-kinds=all --track-origins=yes ./waterjugpuzzle 8 17 20 0 10 10




echo ---------- CASE 4 17 22 2 5 15 ----------
valgrind -s --leak-check=full --show-leak-kinds=all --track-origins=yes ./waterjugpuzzle 4 17 22 2 5 15



