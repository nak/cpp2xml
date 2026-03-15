# cpp2xml

A tool to parse C++ header files and generate structured XML documentation.

## Features

- Parses C++ header files using libclang
- Generates XML files with directory structure matching source files
- Extracts functions, structs, classes, methods, and templates
- **NEW:** Enums and enum classes (C++11)
- **NEW:** Union types
- **NEW:** Operator overloading (member and free functions)
- **NEW:** Variadic templates (C++11)
- **NEW:** Nested classes, structs, and enums
- **NEW:** Friend declarations
- **NEW:** Default parameter values
- Tracks namespace information (including nested namespaces)
- Handles anonymous function parameters with unique type definitions
- Only includes elements directly declared in each header (excludes #include content)

## Installation

```bash
pip install -r requirements.txt
pip install -e .
```

## Usage

```bash
cpp2xml --include-path /path/to/headers:mypkg --output-dir ./xml_output
```

## Requirements

- Python 3.10+
- libclang 16.0+
