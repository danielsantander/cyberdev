#include <iostream>
#include <vector>
using namespace std;

/*
Compile code:      g++ ValidateDomains.cpp
Generates file:    a.out
Run compiled code: `./a.out`
*/

vector<string> target_domains_;

bool AllAlpha(const string &str) {
    bool ret=false;
    if (str.size() > 0) { //empty strings => false
        ret=true;
        for (unsigned int i=0;i<str.size();i++) {
            if ((str[i] >= 'a' && str[i] <= 'z') || (str[i] >= 'A' && str[i] <= 'Z')) {
                continue;
            } else {
                ret = false;
                break;
            }
        }
    }
    return ret;
}

void Split(const string &str, const string &seperator, vector<string> *output) {
    string::size_type left = 0;
    string::size_type right = 0;
    while(left < str.size() && right != string::npos) {
        //right = str.find_first_of(seperator, left);
        right = str.find(seperator,left);
        output->push_back(str.substr(left,right-left));
        left = right+seperator.length();
    }
}

bool AllValidDomainChars(const string &str) {
    bool ret=false;
    if (str.size() > 0) { //empty strings => false
        ret=true;
        for (unsigned int i=0;i<str.size();i++) {
            if ((str[i] >= 'a' && str[i] <= 'z') || (str[i] >= 'A' && str[i] <= 'Z') ||
                    (str[i] >= '0' && str[i] <= '9') || str[i] == '-' || str[i] == '_' || str[i] == '.') {
                continue;
            } else {
                ret = false;
                break;
            }
        }
    }
    cout << "AllValidDomainChars -- returning value: " + std::string(ret ? "true" : "false") + "\n";
    return ret;
}

bool ValidDomain(const string &domain) {
    cout << "ValidDomain -- " + domain + "\n";
    bool ret = false;

    // The 4 is arbitrary, 255 is the max for a valid DNS name
    if(domain.size() > 4 && domain.size() <= 255 && AllValidDomainChars(domain)){
        vector<string> parts;
        Split(domain,".", &parts);

        // DEBUG: print out the contents of a vector
        // cout << "ValidDomain -- parts: \n";
        // for (int i = 0; i < parts.size(); i++) {
        //     cout << parts[i] << " ";     //bruce_wayne-east-1_example com
        // }
        // cout << "\n";
        // END DEBUG

        // bruce_wayne-east-1_example com
        if(parts.size() >= 2) {
            // Need this to prevent IPs from being detected as domains
            string ext = parts[parts.size()-1];     // com
            if(ext.size() >= 2 && AllAlpha(ext)) {  // true
                // cout << "ValidDomain -- AllAlpha: true\n";
                ret = true;
                for(unsigned int i=0;i<parts.size();i++)
                {
                    // 0 prevents empty parts and 63 is max for a valid DNS name part
                    if(parts[i].size() > 0 && parts[i].size() <= 63){
                        if(parts[i][0] == '-'){
                            ret = false;
                            break;
                        }
                    } else {
                        cout << "ValidDomain -- empty or too many parts\n";
                        ret = false;
                        break;
                    }
                }

            }
            else
            {
                cout << "ValidDomain -- AllAlpha: false\n";
            }
        }

        cout << "ValidDomain -- returning value: " + std::string(ret ? "true" : "false") + "\n";
        return ret;
    }
    cout << "ValidDomain -- returning value: " + std::string(ret ? "true" : "false") + "\n";
    return ret;
}

bool AddTargetDomain(const string &domain) {
    cout << "AddTargetDomain -- " + domain + "\n";
    bool ret = false;
    if(ValidDomain(domain)) {
        ret = true;
        target_domains_.push_back(domain);
    }
    cout << "AddTargetDomain -- returning value: " + std::string(ret ? "true" : "false") + "\n";
    return ret;
}

bool AddTargets(const string &targets_str){
    cout << "AddTargets -- " + targets_str + "\n";
    bool ret = true;
    vector<string> ranges;
    Split(targets_str,",", &ranges);
    for(unsigned int i=0;i<ranges.size();i++)
    {
        vector<string> parts;
        Split(ranges[i],":", &parts);

        // DEBUG: print out the contents of a vector
        // cout << "parts: \n";
        // for (int i = 0; i < parts.size(); i++) {
        //     cout << parts[i] << " ";     // bruce_wayne-east-1_example.com dns
        // }
        // cout << "\n";
        // END DEBUG

        if(parts.size() == 2 && parts[1] == "dns"){
            // cout << "\nHAS DNS!\n";
            if(AddTargetDomain(parts[0])){
                cout << "AddTargets -- Valid domain: " + parts[0] + "\n";
                continue;
            }else{
                cout << "AddTargets -- Invalid domain: " + parts[0] + "\n";
            }
        }
    }
    return ret;
}


// main() is where program execution begins.
int main() {
    cout << "---------------\n";
    cout << "Hello World!\n";
    cout << "---------------\n\n";
    std::string domain="bruce_wayne-east-1_example.com";
    std::string target="bruce_wayne-east-1_example.com:dns";

    vector<string> parts;
    AddTargets(target);

    cout << "\n";

    return 0;
    cout << "\n";
    cout << "verifying domain name \'" + domain + "\'...\n";
    AllValidDomainChars(domain);
    return 0;
}
