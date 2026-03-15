// Header with unions
#ifndef UNIONS_H
#define UNIONS_H

// Simple union
union Data {
    int i;
    float f;
    char str[20];
};

// Union with methods (C++ feature)
union Value {
    int intVal;
    double doubleVal;

    Value() : intVal(0) {}
    void setInt(int v) { intVal = v; }
    void setDouble(double v) { doubleVal = v; }
};

namespace storage {
    union Variant {
        long longVal;
        void* ptrVal;
    };
}

#endif // UNIONS_H
