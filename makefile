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

# Update executables
setup: update bin/pdg$(EXECUTABLE_SUFFIX) bin/cpp_pdg$(EXECUTABLE_SUFFIX)

update:
	pip install pyinstaller
	sudo apt-get install $(CC)
	sudo apt-get install libboost-all-dev
bin/editor$(EXECUTABLE_SUFFIX):	bin source/gui.py
	pyinstaller --noconfirm --onefile --windowed --distpath "bin" -n editor$(EXECUTABLE_SUFFIX)  "source/gui.py"
	$(RM) *.spec
bin/pdg$(EXECUTABLE_SUFFIX):	bin source/terminal.py source/gui.py
	pyinstaller --noconfirm --onefile --console --distpath "bin" -n pdg$(EXECUTABLE_SUFFIX)  "source/terminal.py"
	$(RM) *.spec
bin/cpp_pdg$(EXECUTABLE_SUFFIX):	bin source/pydgin.cpp
	$(CC) $(ARGS) source/pydgin.cpp -o bin/cpp_pdg$(EXECUTABLE_SUFFIX) $(DEPS)
bin:
	mkdir bin

pclean:
	$(RM) bin/*$(EXECUTABLE_SUFFIX)