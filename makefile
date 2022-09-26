ifndef OS
	EXECUTABLE_SUFFIX = 
	RM = rm -f
else
	EXECUTABLE_SUFFIX = .exe
	RM = del
endif

CC = g++
ARGS = -pedantic -Werror
DEPS = -lboost_regex

# Update production EXEs
setup: exes/prerecCheck exes/editor$(EXECUTABLE_SUFFIX) exes/pdg$(EXECUTABLE_SUFFIX) exes/cpp_pdg$(EXECUTABLE_SUFFIX)
	echo Updated

exes/prerecCheck:
	echo Checking dependancies...
	pip install pyinstaller
	sudo apt-get install $(CC)
	sudo apt-get install libboost-all-dev
exes/editor$(EXECUTABLE_SUFFIX):	source/main.py source/main.py
	pyinstaller --noconfirm --onefile --windowed --distpath "exes" -n editor$(EXECUTABLE_SUFFIX)  "source/main.py"
	$(RM) *.spec
exes/pdg$(EXECUTABLE_SUFFIX):	source/terminal.py source/main.py
	pyinstaller --noconfirm --onefile --console --distpath "exes" -n pdg$(EXECUTABLE_SUFFIX)  "source/terminal.py"
	$(RM) *.spec
exes/cpp_pdg$(EXECUTABLE_SUFFIX):	source/pydgin.cpp
	$(CC) $(ARGS) source/pydgin.cpp -o exes/cpp_pdg$(EXECUTABLE_SUFFIX) $(DEPS)

pclean:
	$(RM) exes/*$(EXECUTABLE_SUFFIX)