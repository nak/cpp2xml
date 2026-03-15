# C++ Features Support

## Overview

This document outlines which C++ language features are currently supported by cpp2xml and which features could be added in future versions.

## Currently Supported Features

### Core Elements
- ✅ **Functions** - Free functions with all parameters and return types
- ✅ **Classes** - Full class definitions with members
- ✅ **Structs** - Struct definitions with fields and methods
- ✅ **Methods** - Member functions including constructors/destructors
- ✅ **Fields** - Class/struct data members
- ✅ **Templates** - Class templates and function templates
- ✅ **Namespaces** - Including nested namespaces (e.g., `outer::inner`)
- ✅ **Enums** - Traditional C enums and C++11 scoped enums (enum class)
- ✅ **Unions** - Union types with fields and methods
- ✅ **Operator Overloading** - Both member and free function operators

### Type Information
- ✅ **Return types** - For functions and methods
- ✅ **Parameter types** - Including anonymous parameters
- ✅ **Default parameter values** - Default arguments captured
- ✅ **Field types** - For class/struct members
- ✅ **Template parameters** - Type and non-type template parameters
- ✅ **Variadic templates** - Parameter pack detection (C++11)

### Object-Oriented Features
- ✅ **Inheritance** - Base class tracking
- ✅ **Access specifiers** - public, private, protected
- ✅ **Virtual methods** - Virtual and pure virtual functions
- ✅ **Static members** - Static methods and fields
- ✅ **Const methods** - Const-qualified member functions

### Class Features
- ✅ **Nested classes** - Classes defined within classes
- ✅ **Nested structs** - Structs defined within classes/structs
- ✅ **Nested enums** - Enums defined within classes/structs
- ✅ **Friend declarations** - Friend functions and classes

### Special Cases
- ✅ **Anonymous parameters** - With unique ID generation
- ✅ **Include filtering** - Only direct declarations, not #included content
- ✅ **Location tracking** - Line and column numbers for declarations

## C++ Standard Compliance

The parser uses libclang, which supports:
- **C++98/03** - Full support
- **C++11** - Full support
- **C++14** - Full support
- **C++17** - Full support (when using `-std=c++17` flag)
- **C++20** - Partial support (when using `-std=c++20` flag)
- **C++23** - Partial support (depending on clang version)

You can specify the C++ standard using clang arguments:
```bash
cpp2xml -I ./include -o output -- -std=c++20
```

## Features NOT Currently Supported

### Type Aliases and Typedefs
- ❌ **typedef** - Traditional type aliases
- ❌ **using declarations** - Modern type aliases (C++11)
- ❌ **Type aliases for templates**

### Advanced Templates (C++11+)
- ❌ **Variable templates** (C++14)
- ❌ **Template specializations**
- ❌ **Alias templates**

### Modern C++ (C++20+)
- ❌ **Concepts** - Template constraints
- ❌ **Requires clauses**
- ❌ **Coroutines** - co_await, co_yield, co_return
- ❌ **Modules** - import/export
- ❌ **Ranges**

### Function Features
- ❌ **constexpr functions** - Compile-time evaluation
- ❌ **consteval functions** (C++20) - Immediate functions
- ❌ **constinit variables** (C++20)
- ❌ **Lambda expressions** - As class members or standalone
- ❌ **Function try blocks**
- ❌ **noexcept specifications** - Exception guarantees
- ❌ **Deleted functions** - `= delete`
- ❌ **Defaulted functions** - `= default`

### Inheritance Features
- ❌ **Multiple inheritance details** - Only single-level inheritance tracked
- ❌ **Virtual inheritance**
- ❌ **Abstract classes** - Not explicitly marked

### Attributes (C++11+)
- ❌ **[[nodiscard]]**
- ❌ **[[deprecated]]**
- ❌ **[[maybe_unused]]**
- ❌ **[[noreturn]]**
- ❌ **Custom attributes**

### Other Types
- ❌ **Bit fields** - In structs/classes
- ❌ **Anonymous unions/structs**

### Preprocessor
- ❌ **Macro definitions** - #define directives
- ❌ **Conditional compilation** - #if/#ifdef tracking

## Adding Support for New Features

The project is designed to be extensible. To add support for a new C++ feature:

### 1. Extend Data Classes (parser.py)

Add a new dataclass or extend existing ones:
```python
@dataclass
class Enum:
    name: str
    values: list[str]
    is_scoped: bool  # For enum class
    namespace: str | None = None
    location: str | None = None
```

### 2. Add Parsing Logic (parser.py)

Add detection in `_traverse_cursor`:
```python
elif cursor.kind == CursorKind.ENUM_DECL:
    result.enums.append(self._parse_enum(cursor))
```

Implement the parsing method:
```python
def _parse_enum(self, cursor) -> Enum:
    values = []
    for child in cursor.get_children():
        if child.kind == CursorKind.ENUM_CONSTANT_DECL:
            values.append(child.spelling)

    return Enum(
        name=cursor.spelling,
        values=values,
        is_scoped=cursor.is_scoped_enum(),
        namespace=self._get_namespace(cursor),
        location=f"{cursor.location.line}:{cursor.location.column}"
    )
```

### 3. Add XML Generation (xml_generator.py)

Create XML element method:
```python
def _create_enum_element(self, enum: Enum) -> ET.Element:
    enum_elem = ET.Element("enum" if not enum.is_scoped else "enum_class")
    enum_elem.set("name", enum.name)

    if enum.namespace:
        enum_elem.set("namespace", enum.namespace)

    values_elem = ET.SubElement(enum_elem, "values")
    for value in enum.values:
        val_elem = ET.SubElement(values_elem, "value")
        val_elem.set("name", value)

    return enum_elem
```

### 4. Add Tests

Create test fixtures and test cases.

## Recommendations for Production Use

Most common C++ features are now supported! For additional coverage, consider adding:

1. **Type aliases** - Important for understanding type relationships
2. **Concepts** (C++20) - For codebases using modern C++
3. **Attributes** - Useful for API documentation (e.g., [[nodiscard]])
4. **constexpr** - Important for understanding compile-time computation
5. **Template specializations** - For complete template coverage
6. **Lambda expressions** - If used as class members

## libclang Reference

The parser uses libclang's `CursorKind` enum. Available cursor kinds include:

- `NAMESPACE` - Namespace declarations
- `CLASS_DECL` - Class declarations
- `STRUCT_DECL` - Struct declarations
- `ENUM_DECL` - Enum declarations
- `TYPEDEF_DECL` - Typedef declarations
- `TYPE_ALIAS_DECL` - Using declarations (C++11)
- `VAR_DECL` - Variable declarations
- `FUNCTION_DECL` - Function declarations
- `CXX_METHOD` - C++ method declarations
- `CONSTRUCTOR` - Constructor declarations
- `DESTRUCTOR` - Destructor declarations
- `CONVERSION_FUNCTION` - Conversion operators
- `TEMPLATE_TYPE_PARAMETER` - Template type parameters
- `TEMPLATE_NON_TYPE_PARAMETER` - Template non-type parameters
- `CLASS_TEMPLATE` - Class template declarations
- `FUNCTION_TEMPLATE` - Function template declarations
- `CONCEPT_DECL` - Concept declarations (C++20)

See [libclang documentation](https://clang.llvm.org/doxygen/group__CINDEX.html) for complete reference.

## Contributing

If you need support for specific C++ features, contributions are welcome! Please:
1. Open an issue describing the feature
2. Provide example C++ code that should be parsed
3. Describe the expected XML output format
4. Submit a PR with tests
