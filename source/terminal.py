import regex as re
import sys
import os
import pydgin as p

"""
The terminal command source code for pydgin.
Compiled into pdg.exe, then placed on user's
PATH to be callable as a command.
"""

def translate(objects):
    out_objects = []
    for object in objects:
        comp = p.Translator(object, '.')
        out_objects.append(comp.compile())
    print('Completed translation.')
    return out_objects

if __name__ == '__main__':
    args = sys.argv[1:]
    
    to_exe = True

    compiler = 'clang++'
    tags = []
    destination = '.'
    
    objects = []

    if len(args) == 0:
        print('-----Pydgin translator-----')
        print('Translates Python-like Pydgin code to C++.')
        print('Aims to marry a Python-like developer experience')
        print('with the speed, low-level functionality and wide')
        print('array of libraries of C++.')
        print('Turns .pdg files into .cpp or .exe files.')
    else:
        i = -1
        while i + 1 < len(args):
            i += 1
            item = args[i]
            
            if item[-4:] == '.pdg':
                objects.append(item)
            
            elif item == '-c':
                to_exe = False

            elif item == '-translate' or item == '-t':
                to_exe = False

            elif item == '-use':
                i += 1
                compiler = args[i]
            
            elif item == '-args':
                i += 1
                num = args[i]
                for a in range(int(num)):
                    i += 1
                    tags.append(args[i])
            
            else:
                raise "Invalid argument"
        
        objects = translate(objects)
        if to_exe:
            command = compiler + ' ' + ' '.join(tags) + ' ' + ' '.join(objects) + ' -o ' + re.sub(r'\.cpp', r'', objects[-1])
            print(command)
            os.system(command)
