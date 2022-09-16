import regex as re
import sys
import os
import pydgin as p

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

def translate(objects, destination):
    out_objects = []
    for object in objects:
        comp = p.Compiler(object, destination)
        out_objects.append(comp.compile())
    return out_objects

def compile(compiler, tags, objects, destination):
    for object in objects:
        command = compiler + ' -c ' + ' '.join(tags) + ' ' + object + ' -o ' + destination + '/' + re.sub(r'\.cpp', r'.o', object)
        os.system(command)
    return [re.sub(r'\.cpp', r'.o', item) for item in objects]

if __name__ == '__main__':
    args = sys.argv[1:]
    
    to_cpp = True
    to_obj = True
    to_exe = True

    compiler = 'clang++'
    tags = []
    destination = '.'
    
    objects = []

    if len(args) == 0:
        print('-----Pydgin translator-----')
        print('Translates Python-like code to C++.')
        print('Aims to marry a Python-like developer experience')
        print('with the speed, low-level functionality and wide')
        print('array of libraries of C++.')
        print('Turns .pdg files into .cpp, .o, or .exe files.')
    else:
        i = -1
        while i + 1 < len(args):
            i += 1
            item = args[i]
            
            if item[-4:] == '.pdg':
                objects.append(item)
            
            elif item == '-o':
                i += 1
                destination = args[i]
            
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
                compiler = args[i]
            
            elif item == '-args':
                i += 1
                num = args[i]
                for i in num:
                    i += 1
                    tags.append(args[i])
        
        if to_cpp:
            objects = translate(objects, destination)

        if to_obj:
            objects = compile(compiler, tags, objects, destination)

        if to_exe:
            command = compiler + ' ' + ' '.join(tags) + ' ' + ' '.join(objects) + ' -o pdgmain.exe'
            os.system(command)
