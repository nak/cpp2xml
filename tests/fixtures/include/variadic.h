// Header with variadic templates
#ifndef VARIADIC_H
#define VARIADIC_H

// Variadic template class
template<typename... Args>
class Tuple {
    // Implementation omitted
};

// Variadic template function
template<typename... Args>
void print(Args... args);

// Mix of regular and variadic template parameters
template<typename T, typename... Rest>
class TypeList {
    // Implementation omitted
};

namespace util {
    // Variadic template with return type
    template<typename R, typename... Args>
    R invoke(R (*func)(Args...), Args... args);
}

#endif // VARIADIC_H
