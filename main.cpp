//
//  main.cpp
//  Big Booty
//
//  Created by Elijah Busse on 9/27/25.
//

#include <iostream>
#include <string>
#include <cstring>

using namespace std;

void hasabooty(string);

int main() {
    
    
    string name;
    
    while(true){
        
        cout << "Provide thine name: ";
        
        getline(cin, name);
        
        hasabooty(name);
        
    }
   
      
    
    
}

void hasabooty(string name){
    
    if(name != "lev"){
        
        cout << name << " has been positively blessed with a dumper." << endl;
        
    }else{
        
        cout << "fuck u lev" << endl;
        
    }
    
    
};
