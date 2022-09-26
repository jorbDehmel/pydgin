import regex as re
import os

"""
A translator for Pydgin
Used in the terminal commmand and the GUI translator.
"""

class Translator:
    def __init__(self, inp_path, out_dir):
        self.replace = {
            r'(?<=\n).*#.*\n': r'',
            r'@import': r'#include',
            r'(?<!(private)|(public)):(?!=[a-zA-Z0-9:])': r'',
            r'[\'"]{3}[^\'"]*[\'"]{3}': r'',
            r'\n;': r'',
            r' in ': r' : ',
            r'\); {': r') {',
            r'(?<=else);': r'',
            r'@': r'#'
        }
        self.filename = out_dir + '/' + re.search(r'[^/\\.]+(?=\.(pdg)|(txt))', inp_path).group()
        self.header = False
        with open(inp_path, 'r') as file:
            self.text = file.read()

        return

    def _line_fix(self):
        temp = re.split(r'\n', self.text)
        temp = [i + '\n' for i in temp]
        self.text = ''

        # Do tab replacement
        tab_count_prev = 0
        for line_num, line in enumerate(temp):
            # Get current tab count
            if len(line) == 0:
                continue

            # Fix for loop semicoloning
            if re.search(r'(?<!\w)for ', line):
                line = re.sub(r',', r';', line)

            # Balance loop parenthesis
            if re.search(r'(for )|(while )|(if )|(else if )', line):
                opens = 0
                prefix = ""
                for i, char in enumerate(line):
                    if char == '(':
                        opens += 1
                    if char == ')':
                        opens -= 1
                    prefix += char
                    if i + 1 == len(line) or line[i + 1] == ':':
                        for j in range(opens):
                            prefix += ')'
                        prefix += line[i + 1:]
                        break
                temp[line_num] = prefix
                
            line = temp[line_num]

            # Balance tabs with brackets
            tab_count_cur = 0
            while line[tab_count_cur] == '\t':
                tab_count_cur += 1

            # Compare tabs and adjust brackets
            if tab_count_cur > tab_count_prev:
                for i in range(tab_count_prev, tab_count_cur):
                    self.text = self.text[:-1]
                    self.text += ' {\n'
            elif tab_count_cur < tab_count_prev:
                for i in range(tab_count_prev, tab_count_cur, -1):
                    self.text += ('\t' * (i - 1)) + '}' + '\n'

            # Reappend line to text
            self.text += line
            tab_count_prev = tab_count_cur

        return

    def _fix_classes(self):
        temp = re.split(r'\n', self.text)
        self.text = ''
        to_semicolon = -1
        for i, line in enumerate(temp):
            tabs = 0
            while tabs + 1 < len(line) and line[tabs] == '\t':
                tabs += 1
            if re.search(r'(struct )|(class )', line):
                to_semicolon = tabs
            elif to_semicolon == tabs:
                temp[i] += ';'
                to_semicolon = -1
        self.text = '\n'.join(temp)

        return

    def compile(self):
        # Try to compile using executables
        if os.path.exists('cpp_pdg.exe'):
            try:
                os.system('cpp_pdg.exe ' + self.filename)
                return
            except Exception as e:
                print(e)
        elif os.path.exists('cpp_pdg_lin'):
            try:
                os.system('cpp_pdg_lin ' + self.filename)
                return
            except Exception as e:
                print(e)

        # Determine if header
        self.header = ('@header' in self.text)
        if self.header:
            self.text = self.text[8:]

        # Semicolons
        self.text = re.sub(r'(?<![>:])\n', r';\n', self.text)

        # Replace spaces with tabs
        self.text = re.sub(r'    ', r'\t', self.text)

        # Tab pub/priv/prot
        self.text = re.sub(r'private', r'\tprivate', self.text)
        self.text = re.sub(r'public', r'\tpublic', self.text)
        self.text = re.sub(r'protected', r'\tprotected', self.text)

        # Insert opening parenthesis in loops
        loop_subs = {
            r'while (?=[^\(])': r'while (',
            r'for (?=[^\(])': r'for (',
            r'if (?=[^\(])': r'if (',
            r'else if (?=[^\(])': r'else if ('
        }
        for pat in loop_subs:
            self.text = re.sub(pat, loop_subs[pat], self.text)

        # Brackets, end parenthesis, for loop semicoloning
        self._line_fix()

        # Do RegEx replacements
        for pat in self.replace:
            self.text = re.sub(pat, self.replace[pat], self.text)

        # Fix struct/class semicoloning
        self._fix_classes()

        # Untab public/private/restricted
        self.text = re.sub(r'\tprivate', r'private', self.text)
        self.text = re.sub(r'\tpublic', r'public', self.text)
        self.text = re.sub(r'\tprotected', r'protected', self.text)

        # Trim trailing whitespace
        while self.text[-1] == ' ' or self.text[-1] == '\n':
            self.text = self.text[:-1]
        self.text += '\n'
        
        # Fix get kw
        self.text = re.sub(r' get ', r'::', self.text)

        # Write to output
        suffix = '.h' if self.header else '.cpp'
        with open(self.filename + suffix, 'w') as file:
            file.write(self.text)

        # Return filename
        return self.filename
    
    def run(self, name='main'):
        os.system('clang++ -Werror -std=c++11 -pedantic ' + self.filename + ' -o ' + name + '.exe')
        os.system('./' + name + '.exe')

        return
