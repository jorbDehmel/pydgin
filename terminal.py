import regex as re
import sys
import os

"""
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
"""

def translate():
    cpp_path
    return cpp_path

if __name__ == '__main__':
    args = sys.argv

    to_cpp = True
    to_obj = True
    to_exe = True

    compiler = 'clang++'
    tags = []
    destination = '.'
    
    pdgs = []
    cpps = []
    objects = []

    i = -1
    while i < len(sys.argv):
        i += 1
        item = sys.argv[i]
        
        if item[-4:] == '.pdg':
            objects.append(item)
        
        elif item == '-o':
            i += 1
            destination = sys.argv[i]
        
        elif item == '-c':
            to_cpp = True
            to_obj = True
            to_exe = False

        elif item == '-translate':
            to_cpp = True
            to_obj = False
            to_exe = False

        elif item == '-use':
            i += 1
            compiler = sys.argv[i]
        
        elif item == '-args':
            i += 1
            num = sys.argv[i]
            for i in num:
                i += 1
                tags.append(sys.argv[i])
    
    if to_cpp:
        print('Translating...')
        translate()
        pass

    if to_obj:
        print('Compiling...')
        os.system(compiler + ' -c ' + ' '.join(tags) + ' ' + ' '.join(objects) + ' -o ' + destination)

    if to_exe:
        print('Linking...')
        os.system(compiler + ' ' + ' '.join(tags) + ' ' + ' '.join(objects) + ' -o ' + destination)
        pass

    print('Finished.')
