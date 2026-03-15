# Changelog

## [0.2.0] - 2026-03-15

### Added
- **Mapping of include paths to package to generat**
  - cli arg interface updated to force specification of detaintion package to each include path
  - XML generation is broken down by package at top level output directory


## [0.2.0] - 2026-02-16

### Added
- **Enum Support**
  - Traditional C-style enums
  - Scoped enums (enum class) - C++11
  - Enums with explicit values
  - Enums with underlying type specification
  - Namespace tracking for enums

- **Union Support**
  - Union type declarations
  - Unions with fields
  - Unions with methods (C++ feature)
  - Namespace tracking for unions

- **Operator Overloading**
  - Member operator overloads
  - Free function operator overloads
  - All operator types (arithmetic, comparison, subscript, etc.)
  - Access specifiers for member operators
  - Const qualification tracking

- **Variadic Templates**
  - Detection of template parameter packs
  - Support for variadic template classes
  - Support for variadic template functions
  - `variadic="true"` attribute in XML output

- **Nested Types**
  - Nested classes within classes/structs
  - Nested structs within classes/structs
  - Nested enums within classes/structs
  - Multi-level nesting support
  - Full parsing of nested type members

- **Friend Declarations**
  - Friend functions
  - Friend classes
  - Friend member functions
  - Tracking within class definitions

- **Default Parameter Values**
  - Extraction of default parameter values
  - Support for all default types (literals, constants, expressions)
  - XML `default` attribute on parameters

- **Namespace Support**
  - Full namespace tracking for all declaration types
  - Nested namespace support with `::` separator
  - `namespace` attribute in XML output

### Enhanced
- **Parameter Parsing**
  - Now extracts default values
  - Better handling of complex parameter types

- **Template Parsing**
  - Variadic template detection
  - Improved parameter pack handling

- **XML Output**
  - New elements: `<enums>`, `<enum>`, `<enum_class>`, `<unions>`, `<union>`, `<operators>`, `<operator>`
  - New nested elements: `<nested_classes>`, `<nested_structs>`, `<nested_enums>`, `<friends>`, `<friend>`
  - New attributes: `variadic`, `default`, `namespace`, `underlying_type`, `member`

### Test Coverage
- Added comprehensive test fixtures for all new features
- New test file: `test_new_features.py` with 100+ test cases
- Test headers: `enums.h`, `unions.h`, `operators.h`, `variadic.h`, `nested.h`, `friends.h`, `defaults.h`

### Documentation
- Updated README.md with new feature list
- Updated CPP_FEATURES.md with implementation status
- Added CHANGELOG.md (this file)
- Enhanced USAGE.md with examples of new features

## [0.1.0] - Initial Release

### Features
- C++ header file parsing using libclang
- Function declarations with parameters
- Class and struct definitions
- Template classes and functions
- Method parsing (constructors, destructors, regular methods)
- Access specifiers (public, private, protected)
- Virtual, static, and const method tracking
- Inheritance tracking
- Anonymous parameter handling with unique IDs
- Include path filtering
- XML generation with directory structure preservation
- Command-line interface
- Comprehensive test suite
