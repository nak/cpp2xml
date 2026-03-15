// Header with structs
#ifndef STRUCTS_H
#define STRUCTS_H

struct Point {
    double x;
    double y;
    double z;
};

struct Vector {
    double x, y, z;

    // Struct can have methods too
    double magnitude() const;
    void normalize();
};

#endif // STRUCTS_H
