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
    return out_objects

def compile(compiler, tags, objects, destination):
    for object in objects:
        command = compiler + ' -c ' + ' '.join(tags) + ' ' + object + ' -o ' + re.sub(r'\.cpp', r'.o', object)
        print(command)
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
        print('Translates Python-like Pydgin code to C++.')
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

            elif item == '-translate' or item == '-t':
                to_cpp = True
                to_obj = False
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
        
        if to_cpp:
            objects = translate(objects)

        if to_obj:
            objects = compile(compiler, tags, objects, '.')

        if to_exe:
            command = compiler + ' ' + ' '.join(tags) + ' ' + ' '.join(objects) + ' -o ' + re.sub(r'\.o', r'.exe', objects[-1])
            print(command)
            os.system(command)
