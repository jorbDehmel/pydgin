
#include <iostream>
#include <fstream>
#include <boost/regex.hpp>
#include <string>
#include <vector>
using namespace std;

// Splits text along deliminator, returns vector<string>
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

string translate(const string inp_filepath, const string out_dir) {
    string out_filepath = out_dir + '/';
    out_filepath += boost::regex_search(inp_filepath, boost::regex("[^/\\.]+(?=\\.(pdg)|(txt))"));

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
    if (text.substr(0, 7) == "@header") {
        text = text.substr(8);
        out_filepath += ".hpp";
    } else {
        out_filepath += ".cpp";
    }

    // Temporarily turn all scope resolution to get keyword
    text = boost::regex_replace(text, boost::regex("::"), " get ");

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
    text = boost::regex_replace(text, boost::regex("(?<!private):(?!=[a-zA-Z0-9:])"), "");
    text = boost::regex_replace(text, boost::regex("(?<!public):(?!=[a-zA-Z0-9:])"), "");
    text = boost::regex_replace(text, boost::regex("(?<!protected):(?!=[a-zA-Z0-9:])"), "");
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

    return out_filepath;
}

int main(const int argc, char* argv[]) {
    bool to_exe = true;
    string compiler = "clang++";
    vector<string> tags;
    string destination = "./out";
    vector<string> objects;
    string command;

    if (argc == 0) {
        cout << "Invalid translator call.\n";
    } else {
        int i = -1;
        while (i + 1 < argc) {
            i += 1;
            command = argv[i];
            
            if (boost::regex_match(argv[i], boost::regex(".*\\.pdg"))) {
                objects.push_back(argv[i]);
            } else if (command == "--translate" || command == "-t") {
                to_exe = false;
            } else if (command == "--use" || command == "-u") {
                i++;
                compiler = argv[i];
            } else if (command == "--argv" || command == "-a") {
                i++;
                for (int a = 0; a < stoi(string(argv[i])); a++) {
                    i++;
                    tags.push_back(argv[i]);
                }
            } else if (command == "-o") {
                i++;
                destination = argv[i];
            } else {
                cout << "INVALID ARGUMENT";
                return -1;
            }
        }

        for (int i = 0; i < objects.size(); i++) {
            objects[i] = translate(objects[i], ".");
        }
        if (to_exe) {
            string command = compiler + ' ';
            for (string tag : tags) {
                command += ' ' + tag;
            }
            for (string object : objects) {
                command += ' ' + object;
            }
            command += " -o " + destination;
            cout << command << '\n';
            system(command.c_str());
        }
    }

    return 0;
}
