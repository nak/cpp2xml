// Header with classes and methods
#ifndef CLASSES_H
#define CLASSES_H

class Base {
public:
    virtual void doSomething();
    virtual ~Base();
};

class Derived : public Base {
private:
    int value;
    static int count;

public:
    Derived();
    explicit Derived(int v);

    void doSomething() override;
    int getValue() const;
    void setValue(int v);

    static int getCount();

protected:
    void helperMethod();
};

#endif // CLASSES_H
