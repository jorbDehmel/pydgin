#include <iostream>
using namespace std;
int main() {
	cout << "Hello World!" << endl;
	for (int i = 0; i < 5; i += 1) {
		cout << i << endl;
		if (i == 4) {
			cout << "i is four" << endl;
		}
	}
	return 0;
}
