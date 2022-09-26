# Example of a makefile using pygin scripts

# Generate exes
1:	pydgin_test.o
	clang++ pydgin_test.o -o pydgin_test.exe
2:	pydgin_test_2.o
	clang++ pydgin_test_2.o -o pydgin_test_2.exe
3:	pydgin_test_3.o
	clang++ pydgin_test_3.o -o pydgin_test_3.exe

# Generate object files
pydgin_test.o:	pydgin_test.cpp
	clang++ -c pydgin_test.cpp -o pydgin_test.o
pydgin_test_2.o:	pydgin_test_2.cpp
	clang++ -c -std=c++11pydgin_test_2.cpp -o pydgin_test_2.o
pydgin_test_3.o:	pydgin_test_3.cpp
	clang++ -c pydgin_test_3.cpp -o pydgin_test_3.o

# Generate cpp files
pydgin_test.cpp:	pydgin_test.pdg
	../exes/pdg.exe -translate pydgin_test.pdg
pydgin_test_2.cpp:	pydgin_test_2.pdg
	../exes/pdg.exe -translate pydgin_test_2.pdg
pydgin_test_3.cpp:	pydgin_test_3.pdg
	../exes/pdg.exe -translate pydgin_test_3.pdg

# Clean up
clean:
	del *.o
	del *.cpp
pclean:
	del *.o
	del *.cpp
	del *.exe