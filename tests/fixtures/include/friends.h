// Header with friend declarations
#ifndef FRIENDS_H
#define FRIENDS_H

class Box;  // Forward declaration

class Container {
private:
    int value;

public:
    Container(int v);

    // Friend function
    friend void setValue(Container& c, int v);

    // Friend class
    friend class Box;

    // Friend member function
    friend void helper();
};

class Box {
private:
    int width;
    int height;

public:
    // Can access Container's private members due to friend
    void packContainer(Container& c);

    // Friend operator
    friend bool operator==(const Box& a, const Box& b);
};

// Friend function definition
void setValue(Container& c, int v);
bool operator==(const Box& a, const Box& b);

#endif // FRIENDS_H
