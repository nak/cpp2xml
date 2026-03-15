# Project Structure

## Overview

cpp2xml is a Python tool that parses C++ header files using libclang and generates structured XML documentation.

## Directory Structure

```
cpp2xml/
├── src/
│   └── cpp2xml/
│       ├── __init__.py          # Package initialization
│       ├── parser.py            # C++ header parser using libclang
│       ├── xml_generator.py     # XML generation from parsed headers
│       └── cli.py               # Command-line interface
│
├── tests/
│   ├── __init__.py
│   ├── run_tests.py             # Test runner
│   ├── test_parser.py           # Parser tests
│   ├── test_xml_generator.py   # XML generator tests
│   ├── test_cli.py              # CLI tests
│   └── fixtures/
│       └── include/             # Test header files
│           ├── simple.h         # Basic functions
│           ├── classes.h        # Classes with inheritance
│           ├── structs.h        # Structs with fields
│           ├── templates.h      # Template classes/functions
│           ├── anonymous.h      # Anonymous parameters
│           └── subdir/
│               └── nested.h     # Nested directory test
│
├── setup.py                     # Package setup configuration
├── requirements.txt             # Python dependencies
├── README.md                    # Quick start guide
├── USAGE.md                     # Detailed usage instructions
├── EXAMPLE.md                   # Complete example with output
└── PROJECT_STRUCTURE.md         # This file
```

## Core Components

### parser.py

The heart of the project. Contains:

- **Data Classes**: `Parameter`, `Function`, `Field`, `Struct`, `Class`, `Template`, `ParsedHeader`
- **CppParser**: Main parser class that uses libclang to:
  - Parse C++ headers and extract declarations
  - Handle anonymous function parameters with unique IDs
  - Filter declarations to only those directly in the target file
  - Support multiple include paths
  - Track access specifiers, const/static/virtual attributes
  - Parse templates (classes, functions, methods)

### xml_generator.py

Responsible for XML output:

- **XmlGenerator**: Converts parsed C++ structures to XML
  - Generates well-formed, pretty-printed XML
  - Preserves directory structure from source headers
  - Includes special handling for anonymous parameters
  - Outputs location information for each declaration

### cli.py

Command-line interface:

- Argument parsing (include paths, output directory, specific files)
- Integration with clang arguments
- Error handling and verbose output
- Entry point for the `cpp2xml` command

## Data Flow

```
C++ Header Files
       ↓
    [CppParser]
   (uses libclang)
       ↓
  ParsedHeader objects
   (in-memory representation)
       ↓
  [XmlGenerator]
       ↓
   XML Files
  (mirroring directory structure)
```

## Key Features

### 1. Anonymous Parameter Handling

Functions with anonymous parameters:
```cpp
void callback(int, double);
```

Are given unique identifiers:
```xml
<parameter name="anonymous_param_1" type="int" is_anonymous="true">
  <type_definition id="anonymous_param_1" underlying_type="int"/>
</parameter>
```

### 2. Include Filtering

Only declarations **directly in the target header** are included. Elements from `#include` files are excluded by checking file locations.

### 3. Directory Structure Preservation

Output XML files maintain the same directory structure as source headers relative to include paths.

### 4. Comprehensive Type Support

- Functions (with all parameter details)
- Structs (with fields and methods)
- Classes (with inheritance, access specifiers)
- Templates (class templates, function templates)
- Methods (constructors, destructors, virtual, const, static)

## Testing

Test suite includes:
- **test_parser.py**: Tests for parsing various C++ constructs
- **test_xml_generator.py**: Tests for XML generation and output
- **test_cli.py**: Tests for command-line interface

Fixtures provide comprehensive test coverage:
- Simple functions
- Anonymous parameters
- Classes with inheritance
- Structs with methods
- Templates
- Nested directory structures

## Requirements

- Python 3.10+ (for modern type hints with `|` operator)
- libclang 16.0+
- Standard library only (no external dependencies except libclang)

## Installation

```bash
pip install -r requirements.txt
pip install -e .
```

## Usage

```bash
# Parse all headers in include path
cpp2xml -I /path/to/headers -o xml_output

# Parse specific files
cpp2xml -I /path/to/headers -f header1.h -f header2.h -o xml_output

# With clang arguments
cpp2xml -I ./include -o xml_output -- -std=c++20 -DDEBUG
```

## Extension Points

The project is designed to be extensible:

1. **Add new C++ constructs**: Extend `CppParser` with new parsing methods
2. **Customize XML format**: Modify `XmlGenerator` element creation methods
3. **Add output formats**: Create new generator classes (e.g., JSON, Markdown)
4. **Custom filters**: Add filtering logic in `_traverse_cursor`
5. **Additional metadata**: Extend data classes with more attributes

## Code Style

- Modern Python 3.10+ type hints (using `|` instead of `Union`, `list` instead of `List`)
- Dataclasses for structured data
- Comprehensive docstrings
- Clear separation of concerns (parsing, generation, CLI)
- Well-organized test suite with fixtures
