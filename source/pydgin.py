import regex as re
import os

"""
Single-function translation of Pydgin.
"""

def translate(inp_path: str, out_dir: str) -> str:
    with open(inp_path, 'r') as file:
        text = file.read()
    
    # Determine if header
    filename = out_dir + '/' + re.search(r'[^/\\.]+(?=\.(pdg)|(txt))', inp_path).group()
    if text[:8] == '@header':
        text = text[8:]
        filename += '.hpp'
    else:
        filename += '.cpp'

    # Try precompiled translators
    if os.path.exists('../bin/cpp_pdg.exe'):
        os.system('../bin/cpp_pdg.exe ' + inp_path + ' -o ' + filename)
    elif os.path.exists('../bin/cpp_pdg'):
        os.system('../bin/cpp_pdg ' + inp_path + ' -o  ' + filename)
    else:
        print('NO PRECOMPILED TRANSLATOR EXISTS.')
        print('Full Pydgin setup can be run with \'make setup\' in the pydgin folder.')
    
    if os.path.exists(filename):
        print('Successfull precompiled translator call')
        return filename
    else:
        print('FAILED PRECOMPILED TRANSLATOR CALL')
    
    text = re.sub(r'::', r' get ', text)
    text = re.sub(r'(?<![>:])\n', r';\n', text)
    text = re.sub(r'    ', r'\t', text)
    text = re.sub(r'private', r'\tprivate', text)
    text = re.sub(r'public', r'\tpublic', text)
    text = re.sub(r'protected', r'\tprotected', text)

    # Fix loop parethesizing
    loop_subs = {
        r'while (?=[^\(])': r'while (',
        r'for (?=[^\(])': r'for (',
        r'if (?=[^\(])': r'if (',
        r'else if (?=[^\(])': r'else if ('
    }
    for pat in loop_subs:
        text = re.sub(pat, loop_subs[pat], text)
    del loop_subs;

    # Brackets, end parenthesis, for loop semicoloning
    temp = re.split(r'\n', text)
    temp = [i + '\n' for i in temp]
    text = ''

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
                text = text[:-1]
                text += ' {\n'
        elif tab_count_cur < tab_count_prev:
            for i in range(tab_count_prev, tab_count_cur, -1):
                text += ('\t' * (i - 1)) + '}' + '\n'

        # Reappend line to text
        text += line
        tab_count_prev = tab_count_cur

    # Do RegEx replacements
    replace = {
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
    for pat in replace:
        text = re.sub(pat, replace[pat], text)
    del replace

    # Fix struct/class semicoloning
    temp = re.split(r'\n', text)
    text = ''
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
    text = '\n'.join(temp)

    # Untab public/private/restricted
    text = re.sub(r'\tprivate', r'private', text)
    text = re.sub(r'\tpublic', r'public', text)
    text = re.sub(r'\tprotected', r'protected', text)

    # Trim trailing whitespace
    while text[-1] == ' ' or text[-1] == '\n':
        text = text[:-1]
    text += '\n'
    
    text = re.sub(r' get ', r'::', text)
    text = re.sub(r'\t', r'    ', text)

    # Write to output
    with open(filename, 'w') as file:
        file.write(text)

    return filename