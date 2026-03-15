// Header with templates
#ifndef TEMPLATES_H
#define TEMPLATES_H

// Template class
template<typename T>
class Container {
private:
    T data;

public:
    Container(T value) : data(value) {}
    T getValue() const { return data; }
    void setValue(T value) { data = value; }
};

// Template function
template<typename T>
T max(T a, T b) {
    return (a > b) ? a : b;
}

// Template with multiple parameters
template<typename K, typename V>
class Pair {
public:
    K key;
    V value;

    Pair(K k, V v) : key(k), value(v) {}
};

// Template struct
template<typename T>
struct Node {
    T data;
    Node<T>* next;
};

#endif // TEMPLATES_H
