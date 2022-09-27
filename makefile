ifndef OS
	EXECUTABLE_SUFFIX = 
	RM = rm -f
else
	EXECUTABLE_SUFFIX = .exe
	RM = del
endif

PRECOMP_SOURCE = .cpp
CC = clang++
ARGS = -pedantic -Werror
DEPS = -lboost_regex

# Update executables
setup: update bin/pdg$(EXECUTABLE_SUFFIX) bin/cpp_pdg$(EXECUTABLE_SUFFIX)

update:
	sudo apt-get install libboost-all-dev
bin/pdg$(EXECUTABLE_SUFFIX):	bin source/terminal$(PRECOMP_SOURCE)
	$(CC) $(ARGS) source/terminal$(PRECOMP_SOURCE) -o bin/pdg$(EXECUTABLE_SUFFIX) $(DEPS)
bin:
	mkdir bin

pclean:
	$(RM) bin/*$(EXECUTABLE_SUFFIX)