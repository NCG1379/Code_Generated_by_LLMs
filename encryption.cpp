#include <iostream>
#include <fstream>
#include <cstdlib>
#include <cstring>
#include <vector>

using namespace std;

// Function to encrypt the file
void encrypt(const string& infile, const string& outfile, const string& password) {
    
    // Open the input file in binary mode
    ifstream in(infile, ios::binary);

    // Check if the input file was opened successfully
    if (!in.is_open()) {
       cerr << "Error: Unable to open input file: " << infile << endl;
       exit(1);
    }

    // Open the output file in binary mode
    ofstream out(outfile, ios::binary);

    // Check if the output file was opened successfully
    if (!out.is_open()) {
       cerr << "Error: Unable to open output file: " << outfile << endl;
       exit(1);
    }

    // Convert the password to a vector of characters
    vector<char> password_vec(password.begin(), password.end());

    // Loop through the input file and encrypt each byte
    char ch;
    while (in.get(ch)) {
        // XOR each byte with the corresponding byte in the password
        ch ^= password_vec[in.tellg() % password_vec.size()];
        out.put(ch);
    }

    // Close the input and output files
    in.close();
    out.close();
}

int main() {
    // Ask the user for the input file, output file, and password to use for encryption
    string infile, outfile, password;
    // cout << "Enter the input file: ";
    // cin >> infile;
    // cout << "Enter the output file: ";
    // cin >> outfile;
    // cout << "Enter the password to use for encryption: ";
    // cin >> password;

    infile = "C:\\Users\\hack1379\\Documents\\WizardCode_encrypt_file_cpp\\texto.txt";
    outfile = "C:\\Users\\hack1379\\Documents\\WizardCode_encrypt_file_cpp\\texto_encriptado.txt";
    password = "pass123";

    // cout << infile << "\n" << outfile << "\n" << password << "\n";

    // Encrypt the file and save the result to a new file
    encrypt(infile, outfile, password);

    // Display a success message
    // cout << "File successfully encrypted to " << outfile << endl;

    return 0;
}
