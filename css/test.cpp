#include <cmath>
#include <iostream>

using namespace std;
int main(int argc, char const *argv[])
{
    int in;
    while(true)
    {
        cout << "enter: ";
        cin >> in;
        cout << sin(in) << ", " << cos(in) << endl;
    }
    return 0;
}
