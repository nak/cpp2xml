// Header with anonymous parameters
#ifndef ANONYMOUS_H
#define ANONYMOUS_H

// Multiple anonymous parameters
void callback(int, void (*)(int, double), void*);

// Mix of named and anonymous
int compute(int x, int, double, float y);

// Function pointer with anonymous params
typedef void (*Handler)(int, char*);

#endif // ANONYMOUS_H
