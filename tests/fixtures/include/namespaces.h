// Header with namespaces
#ifndef NAMESPACES_H
#define NAMESPACES_H

namespace outer {

void outerFunction();

class OuterClass {
public:
    void method();
};

namespace inner {

void innerFunction();

class InnerClass {
public:
    void method();
};

template<typename T>
class TemplateClass {
    T value;
};

} // namespace inner

} // namespace outer

// Global namespace
void globalFunction();

class GlobalClass {
public:
    void method();
};

#endif // NAMESPACES_H
