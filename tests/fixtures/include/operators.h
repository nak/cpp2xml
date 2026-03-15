// Header with operator overloading
#ifndef OPERATORS_H
#define OPERATORS_H

class Complex {
private:
    double real;
    double imag;

public:
    Complex(double r = 0, double i = 0);

    // Arithmetic operators
    Complex operator+(const Complex& other) const;
    Complex operator-(const Complex& other) const;
    Complex operator*(const Complex& other) const;

    // Comparison operators
    bool operator==(const Complex& other) const;
    bool operator!=(const Complex& other) const;

    // Unary operators
    Complex operator-() const;

    // Assignment operator
    Complex& operator=(const Complex& other);

    // Stream operators (must be friends or free functions)
    friend Complex operator/(const Complex& a, const Complex& b);
};

// Free function operator
Complex operator/(const Complex& a, const Complex& b);

class Array {
private:
    int* data;
    int size;

public:
    // Subscript operator
    int& operator[](int index);
    const int& operator[](int index) const;

    // Function call operator
    int operator()(int x, int y) const;
};

#endif // OPERATORS_H
