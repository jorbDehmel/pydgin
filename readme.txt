Pydgin translator

Goal:
Translate Python-like code to C++
Readability over line efficiency! Python style!

Language:
Uses standard Python notation generally.
Typing - Uses C++ style compilertime rather than Python's runtime. Uses explicit typing when declaring variables, etc
Domains - Uses tabs to denote domains, rather than C++'s brackets + tabs
#include - Uses @import "" / @import <> rather than #include "" / #include <>
Preprocessor directives - Start with @ instead of # (# means comment)
Semicolons - Uses newline to denote end of statement
Comments - Uses Python notation (Note: both kinds are discarded at compiletime, unlike Python)
Blank newlines - These are totally removed at compiletime, rather than being interpretted as ';'
Loops - Eliminates unnecessary parenthasis
For loops - for int i, i < j, i += 1:
++ optimization - Eliminates ++, replaces with += 1. Optimizes replacement as a prefix in this case

What it does:
Translates Pydgin .pgn files into .cpp files

Example:
------------------------
Pydgin code
------------------------
@import <iostream>
using namespace std

'''
A demonstration
of the Pydgin translator
'''

string to_print ("Hello World!")

int main():
	cout << to_print << endl
	for int i, i < 5, i += 1:
	    cout << i << endl

------------------------
Compiles to: (All comments and empty lines are removed at compiletime)
------------------------
#include <iostream>
using namespace std;
string to_print ("Hello World!");
int main() {
	cout << to_print << endl;
	for (int i; i < 5; ++i) {
	    cout << i << endl;}}