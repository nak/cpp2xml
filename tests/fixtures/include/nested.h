// Header with nested types
#ifndef NESTED_H
#define NESTED_H

class Outer {
public:
    // Nested class
    class Inner {
    public:
        void innerMethod();

        // Doubly nested
        class DeepInner {
        public:
            void deepMethod();
        };
    };

    // Nested struct
    struct Config {
        int value;
        bool enabled;
    };

    // Nested enum
    enum Status {
        READY,
        BUSY,
        ERROR
    };

    void outerMethod();
};

struct Container {
    // Nested enum class
    enum class Type {
        SMALL,
        MEDIUM,
        LARGE
    };

    class Item {
    public:
        Type type;
    };
};

#endif // NESTED_H
