// Header with default parameters
#ifndef DEFAULTS_H
#define DEFAULTS_H

#include <string>

// Function with default parameters
void configure(int port = 8080, bool secure = true);

// Multiple defaults
void connect(const char* host, int port = 80, int timeout = 30, bool retry = false);

class Server {
public:
    // Constructor with defaults
    Server(int port = 8080, int threads = 4);

    // Method with defaults
    void start(bool background = false, int priority = 0);

    // Mix of default and non-default
    void send(const char* data, int length, bool compressed = true, int retries = 3);
};

// Template with default parameter
template<typename T = int>
class Buffer {
public:
    void resize(int size = 1024);
};

#endif // DEFAULTS_H
