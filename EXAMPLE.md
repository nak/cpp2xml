# Example

This example demonstrates how cpp2xml parses C++ headers and generates XML.

## Sample Header File

`example.h`:
```cpp
#ifndef EXAMPLE_H
#define EXAMPLE_H

// Simple function
int add(int a, int b);

// Function with anonymous parameter
void process(int, double value);

// Struct with fields
struct Point {
    double x;
    double y;
    double distance() const;
};

// Class with inheritance
class Shape {
public:
    virtual void draw() = 0;
    virtual ~Shape() {}
};

class Circle : public Shape {
private:
    double radius;
    Point center;

public:
    Circle(double r);
    void draw() override;
    double getRadius() const;
    void setRadius(double r);

    static int getShapeCount();
};

// Template class
template<typename T>
class Container {
private:
    T* data;
    int size;

public:
    Container(int s);
    T& get(int index);
    void set(int index, const T& value);
};

// Template function
template<typename T>
T max(T a, T b) {
    return (a > b) ? a : b;
}

#endif
```

## Running cpp2xml

```bash
cpp2xml -I .:mylib -f example.h -o output
```

## Generated XML

`output/mylib/example.xml`:
```xml
<?xml version="1.0" ?>
<header file="example.h" path="/full/path/to/example.h">
  <functions>
    <function name="add" return_type="int" location="5:5">
      <parameters>
        <parameter name="a" type="int"/>
        <parameter name="b" type="int"/>
      </parameters>
    </function>
    <function name="process" return_type="void" location="8:6">
      <parameters>
        <parameter name="anonymous_param_1" type="int" is_anonymous="true" anonymous_id="anonymous_param_1">
          <type_definition id="anonymous_param_1" underlying_type="int"/>
        </parameter>
        <parameter name="value" type="double"/>
      </parameters>
    </function>
  </functions>

  <structs>
    <struct name="Point" location="11:8">
      <fields>
        <field name="x" type="double"/>
        <field name="y" type="double"/>
      </fields>
      <methods>
        <method name="distance" return_type="double" access="public" const="true" location="14:12"/>
      </methods>
    </struct>
  </structs>

  <classes>
    <class name="Shape" location="18:7">
      <base_classes/>
      <fields/>
      <methods>
        <method name="draw" return_type="void" access="public" virtual="true" location="20:18"/>
        <method name="~Shape" return_type="void" access="public" virtual="true" location="21:18"/>
      </methods>
    </class>

    <class name="Circle" location="24:7">
      <base_classes>
        <base name="Shape"/>
      </base_classes>
      <fields>
        <field name="radius" type="double" access="private"/>
        <field name="center" type="Point" access="private"/>
      </fields>
      <methods>
        <method name="Circle" return_type="void" access="public" location="30:5">
          <parameters>
            <parameter name="r" type="double"/>
          </parameters>
        </method>
        <method name="draw" return_type="void" access="public" location="31:10"/>
        <method name="getRadius" return_type="double" access="public" const="true" location="32:12"/>
        <method name="setRadius" return_type="void" access="public" location="33:10">
          <parameters>
            <parameter name="r" type="double"/>
          </parameters>
        </method>
        <method name="getShapeCount" return_type="int" access="public" static="true" location="35:16"/>
      </methods>
    </class>
  </classes>

  <templates>
    <template name="Container" kind="class" location="39:7">
      <template_parameters>
        <template_parameter name="T"/>
      </template_parameters>
    </template>

    <template name="max" kind="function" return_type="T" location="52:2">
      <template_parameters>
        <template_parameter name="T"/>
      </template_parameters>
      <parameters>
        <parameter name="a" type="T"/>
        <parameter name="b" type="T"/>
      </parameters>
    </template>
  </templates>
</header>
```

## Key Features Demonstrated

1. **Function parsing**: Both `add` with named parameters and `process` with an anonymous parameter
2. **Anonymous parameters**: The anonymous `int` parameter in `process` is given a unique ID
3. **Struct parsing**: `Point` struct with fields and a method
4. **Class inheritance**: `Circle` derives from `Shape`, shown in `<base_classes>`
5. **Access specifiers**: Private fields, public methods
6. **Method attributes**: `const`, `virtual`, `static`, `override`
7. **Constructors**: Special handling for constructor methods
8. **Templates**: Both class templates (`Container<T>`) and function templates (`max<T>`)
9. **Location tracking**: Line and column numbers for each declaration

## Integration Example

You can parse the XML and use it for:
- **Documentation generation**: Convert XML to HTML/Markdown docs
- **API analysis**: Extract all public APIs from a codebase
- **Code generation**: Generate bindings for other languages
- **Dependency analysis**: Track what types are used where
- **IDE integration**: Provide code completion and navigation
