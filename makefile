# OS-proofing
ifndef OS
	EXECUTABLE_SUFFIX = 
	RM = rm -f
else
	EXECUTABLE_SUFFIX = .exe
	RM = del
endif

# Variables
PRECOMP_SOURCE = .cpp
CC = clang++
ARGS = -pedantic -Werror
DEPS = -lboost_regex

# Update executables
setup: update bin/pdg$(EXECUTABLE_SUFFIX)

# Get dependancies
update:
	sudo apt-get install libboost-all-dev

# Make needed junk
bin/pdg$(EXECUTABLE_SUFFIX):	bin source/terminal$(PRECOMP_SOURCE)
	$(CC) $(ARGS) source/terminal$(PRECOMP_SOURCE) -o bin/pdg$(EXECUTABLE_SUFFIX) $(DEPS)
bin:
	mkdir bin

# Housekeeping
pclean:
	$(RM) bin/*$(EXECUTABLE_SUFFIX)