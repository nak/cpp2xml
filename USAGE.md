# Usage Guide

## Installation

First, install the required dependencies:

```bash
pip install -r requirements.txt
pip install -e .
```

## Basic Usage

### Parse all headers in an include directory

```bash
cpp2xml -I /path/to/include:pkg_name -o xml_output
```

This will:
1. Find all `.h`, `.hpp`, `.hxx`, and `.hh` files in the include directory
2. Parse each header file
3. Generate corresponding XML files in `xml_output/<mapped_pkg>` with the same directory structure


### Multiple include paths

```bash
cpp2xml -I /usr/include:core_os -I /usr/local/include:local_os -I ./include:mylib -o xml_output
```

### Pass additional clang arguments

Use `--` to separate cpp2xml arguments from clang arguments:

```bash
cpp2xml -I ./include:mylib -o xml_output -- -std=c++20 -DDEBUG -DFEATURE_X
```

### Verbose output

```bash
cpp2xml -I ./include:mylib -o xml_output -v
```

## XML Output Format

The generated XML files follow this structure:

```xml
<?xml version="1.0" ?>
<header file="relative/path/to/header.h" path="/absolute/path/to/header.h">
  <functions>
    <function name="functionName" return_type="int" namespace="mylib" location="10:5">
      <parameters>
        <parameter name="x" type="int"/>
        <parameter name="anonymous_param_1" type="double" is_anonymous="true" anonymous_id="anonymous_param_1">
          <type_definition id="anonymous_param_1" underlying_type="double"/>
        </parameter>
      </parameters>
    </function>
  </functions>

  <structs>
    <struct name="Point" namespace="geometry" location="15:1">
      <fields>
        <field name="x" type="double"/>
        <field name="y" type="double"/>
      </fields>
      <methods>
        <method name="distance" return_type="double" access="public" const="true"/>
      </methods>
    </struct>
  </structs>

  <classes>
    <class name="MyClass" namespace="mylib" location="25:1">
      <base_classes>
        <base name="BaseClass"/>
      </base_classes>
      <fields>
        <field name="value" type="int" access="private"/>
        <field name="count" type="int" access="private" static="true"/>
      </fields>
      <methods>
        <method name="getValue" return_type="int" access="public" const="true"/>
        <method name="doWork" return_type="void" access="public" virtual="true"/>
      </methods>
    </class>
  </classes>

  <templates>
    <template name="Container" kind="class" namespace="containers" location="50:1">
      <template_parameters>
        <template_parameter name="T"/>
      </template_parameters>
    </template>

    <template name="max" kind="function" return_type="T" namespace="util" location="60:1">
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

## Features

### Namespace Support

The parser extracts namespace information for all declarations. Nested namespaces are represented using `::` separator:

```cpp
namespace outer {
    namespace inner {
        void func();  // Will have namespace="outer::inner"
    }
}
```

Functions, classes, structs, and templates all include namespace information in their XML output.

### Anonymous Parameters

When a function has anonymous parameters (no name), cpp2xml automatically generates unique identifiers:

```cpp
void callback(int, double);
```

Generates:

```xml
<function name="callback" return_type="void">
  <parameters>
    <parameter name="anonymous_param_1" type="int" is_anonymous="true" anonymous_id="anonymous_param_1">
      <type_definition id="anonymous_param_1" underlying_type="int"/>
    </parameter>
    <parameter name="anonymous_param_2" type="double" is_anonymous="true" anonymous_id="anonymous_param_2">
      <type_definition id="anonymous_param_2" underlying_type="double"/>
    </parameter>
  </parameters>
</function>
```

### Include Filtering

Only declarations directly in the target header file are included in the XML output. Elements from `#include` files are excluded.

### Directory Structure Preservation

The output XML files mirror the directory structure of the source headers:

```
include/
  foo.h
  bar/
    baz.h

xml_output/
  foo.xml
  bar/
    baz.xml
```

### Template Support

Both template classes and template functions are parsed and represented in the XML:

```cpp
template<typename T>
class Container {
    T data;
};

template<typename T>
T max(T a, T b);
```

## Programmatic Usage

You can also use cpp2xml as a Python library:

```python
from cpp2xml import CppParser, XmlGenerator

# Initialize parser
parser = CppParser(
    include_paths=["/path/to/include"],
    clang_args=["-std=c++17"]
)

# Parse a single header
parsed = parser.parse_header("/path/to/include/header.h")

# Or parse all headers
all_parsed = parser.parse_all_headers()

# Generate XML
generator = XmlGenerator(output_dir="./xml_output")
generator.write_xml(parsed)

# Or generate all
generator.generate_all(all_parsed)
```

## Testing

Run the test suite:

```bash
cd tests
python run_tests.py
```

Or use unittest directly:

```bash
python -m unittest discover tests
```
