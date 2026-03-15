// Header with enums and enum classes
#ifndef ENUMS_H
#define ENUMS_H

// Traditional enum
enum Color {
    RED,
    GREEN,
    BLUE
};

// Enum with explicit values
enum StatusCode {
    OK = 200,
    NOT_FOUND = 404,
    SERVER_ERROR = 500
};

// Scoped enum (enum class)
enum class Direction {
    NORTH,
    SOUTH,
    EAST,
    WEST
};

// Enum class with explicit underlying type
enum class Priority : int {
    LOW = 0,
    MEDIUM = 1,
    HIGH = 2
};

namespace config {
    enum class LogLevel {
        DEBUG,
        INFO,
        WARNING,
        ERROR
    };
}

#endif // ENUMS_H
