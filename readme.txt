------------------------
Pydgin translator
------------------------

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

------------------------
Example:
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

------------------------
pdg command in terminal:
------------------------
Move 'pdg.exe' (which can be found in ../exes) to a more permanent
folder, then add it to your system PATH variable. You can then use
the 'pdg' command from anywhere to translate Pydgin files.

------------------------
pdg.exe, and terminal.py
------------------------
A terminal translator/compiler for pydgin. Can translate to .cpp,
compile to .o, and link to .exe. By default sits on top of clang++,
but can use others by -use <compiler>. Can pass arguments directly
to compiler by -args <number of args> <arg 1> <arg 2> ... <arg n>.

pydgin a.pdg b.pdg c.pdg -o main.exe
    a.pdg b.pdg c.pdg -> a.cpp b.cpp c.cpp -> a.o b.o c.o
    -> main.exe

pydgin a.pdg b.pdg c.pdg
    -> out.exe

pydgin -translate a.pdg
    -> a.cpp

pydgin -c a.pdg -o main.o
    a.pdg -> a.cpp -> main.o
    -> main.o

pydgin -c a.pdg
    -> a.o

pydgin -use clang++ -args 3 -pedantic -Werror -c a.pdg
    clang++ -pedantic -Werror -c a.pdg
    -> a.o

------------------------
editor.exe and main.py
------------------------
A basic graphical user interface for Pydgin writing and
translation. Uses the tkinter module.

------------------------
pydgin/makefile
------------------------
This make file is used to update the exes after changing the source
.py files. The commands "make" or "make update" can be used while
in this folder to do so.

------------------------
pydgin/tests
------------------------
Various tests for ensuring the translator is working properly.
A makefile is also included for an example of using the pdg terminal
command.
