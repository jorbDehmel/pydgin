/*
Script for converting pdg to cpp, this time written in cpp.
*/

#include <iostream>
#include <fstream>
#include <boost/regex>
#include <string>
using namespace std;

int main(int argc, char **argv) {
    // Takes in input filepath, output filepath
    if (argc < 3) {
        cout << "Invalid translator call.\n";
        return -1;
    }
    string inp_filepath = argv[1];
    string out_filepath = argv[2];

    // Get text from file
    ifstream file;
    file.open(inp_filepath, ifstream::in);
    string text, temp;
    text = "";
    while (getline(file, temp)) {
        text += temp;
    }
    file.close();

    // Semicolons
    text = boost::regex_replace(text, boost::regex("(?<![>:])\n"), ";\n");

    // Replace spaces with tabs
    text = boost::regex_replace(text, boost::regex("    "), "\t");

    // Tab pub/priv/restr
    text = boost::regex_replace(text, boost::regex("private"), "\\tprivate");
    text = boost::regex_replace(text, boost::regex("public"), "\\tpublic");
    text = boost::regex_replace(text, boost::regex("protected"), "\\tprotected");

    // Loop stuff
    text = boost::regex_replace(text, regex("while (?=[^\\(])"), "while (");
    text = boost::regex_replace(text, regex("for (?=[^\\(])"), "");
    text = boost::regex_replace(text, regex("if (?=[^\\(])"), "");
    text = boost::regex_replace(text, regex("else if (?=[^\\(])"), "");

    // Brackets, end parenthesis, for loop semicoloning
    /*
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
            print('became', temp[line_num])
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
    */

    // Misc housekeeping
    text = boost::regex_replace(text, boost::regex("(?<=\\n).*#.*\\n"), "");
    text = boost::regex_replace(text, boost::regex("@import"), "#include");
    text = boost::regex_replace(text, boost::regex("(?<!(private)|(public)):(?!=[a-zA-Z0-9:])"), "");
    text = boost::regex_replace(text, boost::regex("['\"]{3}[^'\"]*['\"]{3}"), "");
    text = boost::regex_replace(text, boost::regex("\n"), "");
    text = boost::regex_replace(text, boost::regex(" in "), " : ");
    text = boost::regex_replace(text, boost::regex("\\); {"), ") {");
    text = boost::regex_replace(text, boost::regex("(?<=else);"), "");
    text = boost::regex_replace(text, boost::regex("@"), "#");

    // Fix classes
    /*
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
    */

    // Untab pub/priv/prot
    text = boost::regex_replace(text, boost::regex("\\tprivate"), "private");
    text = boost::regex_replace(text, boost::regex("\\tpublic"), "public");
    text = boost::regex_replace(text, boost::regex("\\tprotected"), "protected");

    // Trim trailing whitespace
    while (text[text.length() - 1] == '\n' || text[text.length() - 1] == ' ') {
        text = text.substr(0, text.length() - 1);
    }
    text += '\n';

    // Fix scope resolution operator
    text = boost::regex_replace(text, boost::regex(" get "), "::");

    // Write to output
    ofstream out_file;
    out_file.open(out_filepath, ios::out);
    out_file.seekp(ios::beg);
    out_file.write(text);
    out_file.close();

    return 0;
}
