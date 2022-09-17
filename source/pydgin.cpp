/*
Script for converting pdg to cpp, this time written in cpp.

Pretty much a line-for-line translation (ironically) of the .py.

Note: Should work, but my boost files aren't set up right lol
*/

#include <iostream>
#include <fstream>
#include "boost/regex.hpp"
#include <string>
#include <vector>
using namespace std;

vector<string> split(const string& text, const char& deliminator) {
    vector<string> vect;
    string temp;
    for (int i = 0; i < text.length(); i++) {
        if (text[i] == deliminator) {
            vect.push_back(temp);
            temp = "";
            continue;
        }
        temp += text[i];
    }
    return vect;
}

int main(int argc, char **argv) {
    // Takes in input filepath, output filepath
    if (argc < 3) {
        cout << "Invalid translator call.\n";
        return -1;
    }
    char* inp_filepath = argv[1];
    char* out_filepath = argv[2];

    // Get text from file
    ifstream file;
    file.open(inp_filepath, ios::in);
    string text, temp_s;
    text = "";
    while (getline(file, temp_s)) {
        text += temp_s;
    }
    file.close();

    // Determine if header
    bool header = text.substr(0, 7) == "@header";
    if (header) {
        text = text.substr(8);
    }

    // Semicolons
    text = boost::regex_replace(text, boost::regex("(?<![>:])\n"), ";\n");

    // Replace spaces with tabs
    text = boost::regex_replace(text, boost::regex("    "), "\t");

    // Tab pub/priv/restr
    text = boost::regex_replace(text, boost::regex("private"), "\\tprivate");
    text = boost::regex_replace(text, boost::regex("public"), "\\tpublic");
    text = boost::regex_replace(text, boost::regex("protected"), "\\tprotected");

    // Loop stuff
    text = boost::regex_replace(text, boost::regex("while (?=[^\\(])"), "while (");
    text = boost::regex_replace(text, boost::regex("for (?=[^\\(])"), "");
    text = boost::regex_replace(text, boost::regex("if (?=[^\\(])"), "");
    text = boost::regex_replace(text, boost::regex("else if (?=[^\\(])"), "");

    // Brackets, end parenthesis, for loop semicoloning
    vector<string> temp = split(text, '\n');
    for (int i = 0; i < temp.size(); i++) {
        temp[i] += '\n';
    }
    text = "";

    int tab_count_prev = 0;
    int tab_count_cur;
    string line, prefix;
    int opens;
    char character;
    for (int line_num = 0; line_num < temp.size(); line_num++) {
        line = temp[line_num];

        if (line.length() == 0) {
            continue;
        }

        // Fix for loop semicoloning
        if (boost::regex_search(line, boost::regex("(?<!\\w)for "))) {
            line = boost::regex_replace(line, boost::regex(","), ";");
        }

        // Balance loop parenthesis
        if (boost::regex_search(line, boost::regex("(for )|(while )|(if )|(else if )"))) {
            opens = 0;
            prefix = "";
            for (int i = 0; i < line.length(); i++) {
                character = line[i];
                if (character == '(') {
                    opens++;
                } else if (character == ')') {
                    opens--;
                }
                prefix += character;
                if (i + 1 == line.length() || line[i + 1] == ':') {
                    for (int j = 0; j < opens; j++) {
                        prefix += ')';
                    }
                    prefix += line.substr(i + 1);
                    break;
                }
            }
            temp[line_num] = prefix;
        }
        line = temp[line_num];

        tab_count_cur = 0;
        while (line[tab_count_cur] == '\t') {
            tab_count_cur++;
        }

        if (tab_count_cur > tab_count_prev) {
            for (int i = tab_count_prev; i < tab_count_cur; i++) {
                text = text.substr(0, text.size() - 2);
                text += " {\n";
            }
        } else if (tab_count_cur < tab_count_prev) {
            for (int i = tab_count_prev; i < tab_count_cur; i--) {
                for (int j = 0; j < i - 1; j++) {
                    text += '\t';
                }
                text += "}\n";
            }
        }

        text += line;
        tab_count_prev = tab_count_cur;
    }

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
    temp = split(text, '\n');
    text = "";
    int to_semicolon = -1;
    int tabs;
    for (int i = 0; i < temp.size(); i++) {
        line = temp[i];
        tabs = 0;
        while (tabs + 1 < line.length() && line[tabs] == '\t') {
            tabs++;
        }
        if (boost::regex_search(line, boost::regex("(struct )|(class )"))) {
            to_semicolon = tabs;
        } else if (to_semicolon == tabs) {
            temp[i] += ';';
            to_semicolon = -1;
        }
    }
    for (int i = 0; i < temp.size(); i++) {
        text += temp[i] + '\n';
    }

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
    out_file.write((char*)&text, sizeof(text));
    out_file.close();

    return 0;
}
