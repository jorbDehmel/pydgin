import sys
import os
import source.pydgin as p

"""
The terminal command source code for pydgin.
Compiled into pdg.exe, then placed on user's
PATH to be callable as a command.
"""

if __name__ == '__main__':
    args = sys.argv[1:]
    
    to_exe = True
    compiler = 'clang++'
    tags = []
    destination = './out'
    objects = []

    if len(args) == 0:
        print('Invalid translator call.')
    else:
        i = -1
        while i + 1 < len(args):
            i += 1
            item = args[i]
            
            if item[-4:] == '.pdg':
                objects.append(item)

            elif item == '--translate' or item == '-t':
                to_exe = False

            elif item == '--use' or item == '-u':
                i += 1
                compiler = args[i]
            
            elif item == '--args' or item == '-a':
                i += 1
                num = args[i]
                for a in range(int(num)):
                    i += 1
                    tags.append(args[i])
            
            elif item == '-o':
                i += 1
                destination = args[i]

            else:
                raise "INVALID ARGUMENT";
        
        objects = [p.translate(object, '.') for object in objects]
        if to_exe:
            command = compiler + ' ' + ' '.join(tags) + ' ' + ' '.join(objects) + ' -o ' + destination
            print(command)
            os.system(command)
