#!/usr/bin/env python3
"""Demo script showing all new features of cpp2xml."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent / "src"))

from cpp2xml.parser import CppParser
from cpp2xml.xml_generator import XmlGenerator


def demo():
    """Demonstrate all features."""
    parser = CppParser(include_paths=['tests/fixtures/include'])

    print("=" * 70)
    print("CPP2XML - New Features Demo")
    print("=" * 70)

    # 1. Enums and Enum Classes
    print("\n1. ENUMS AND ENUM CLASSES")
    print("-" * 70)
    result = parser.parse_header('tests/fixtures/include/enums.h')
    print(f"   Found {len(result.enums)} enums:")
    for enum in result.enums:
        scope = "enum class" if enum.is_scoped else "enum"
        print(f"   • {scope} {enum.name} ({len(enum.values)} values)")
        if enum.namespace:
            print(f"     namespace: {enum.namespace}")

    # 2. Unions
    print("\n2. UNIONS")
    print("-" * 70)
    result = parser.parse_header('tests/fixtures/include/unions.h')
    print(f"   Found {len(result.unions)} unions:")
    for union in result.unions:
        print(f"   • union {union.name}")
        print(f"     - {len(union.fields)} fields, {len(union.methods)} methods")

    # 3. Operator Overloading
    print("\n3. OPERATOR OVERLOADING")
    print("-" * 70)
    result = parser.parse_header('tests/fixtures/include/operators.h')
    total_operators = len(result.operators)
    for cls in result.classes:
        total_operators += len(cls.operators)
    print(f"   Found {total_operators} operator overloads:")
    for cls in result.classes:
        if cls.operators:
            print(f"   • class {cls.name}:")
            for op in cls.operators:
                print(f"     - operator{op.operator_kind}")
    if result.operators:
        print(f"   • Free function operators: {len(result.operators)}")

    # 4. Variadic Templates
    print("\n4. VARIADIC TEMPLATES")
    print("-" * 70)
    result = parser.parse_header('tests/fixtures/include/variadic.h')
    variadic_count = sum(1 for t in result.templates if t.is_variadic)
    print(f"   Found {variadic_count} variadic templates:")
    for template in result.templates:
        if template.is_variadic:
            params = ', '.join(template.template_parameters)
            print(f"   • template<{params}> {template.kind} {template.name}")

    # 5. Nested Types
    print("\n5. NESTED TYPES")
    print("-" * 70)
    result = parser.parse_header('tests/fixtures/include/nested.h')
    print(f"   Found classes with nested types:")
    for cls in result.classes:
        total_nested = len(cls.nested_classes) + len(cls.nested_structs) + len(cls.nested_enums)
        if total_nested > 0:
            print(f"   • class {cls.name}:")
            if cls.nested_classes:
                print(f"     - {len(cls.nested_classes)} nested classes")
            if cls.nested_structs:
                print(f"     - {len(cls.nested_structs)} nested structs")
            if cls.nested_enums:
                print(f"     - {len(cls.nested_enums)} nested enums")

    # 6. Friend Declarations
    print("\n6. FRIEND DECLARATIONS")
    print("-" * 70)
    result = parser.parse_header('tests/fixtures/include/friends.h')
    total_friends = sum(len(c.friends) for c in result.classes)
    print(f"   Found {total_friends} friend declarations:")
    for cls in result.classes:
        if cls.friends:
            print(f"   • class {cls.name}:")
            for friend in cls.friends:
                print(f"     - friend {friend.friend_type}: {friend.name}")

    # 7. Default Parameters
    print("\n7. DEFAULT PARAMETERS")
    print("-" * 70)
    result = parser.parse_header('tests/fixtures/include/defaults.h')
    functions_with_defaults = [f for f in result.functions if any(p.default_value for p in f.parameters)]
    print(f"   Found {len(functions_with_defaults)} functions with default parameters:")
    for func in functions_with_defaults[:3]:  # Show first 3
        print(f"   • {func.name}(")
        for param in func.parameters:
            if param.default_value:
                print(f"       {param.name}: {param.type_name} = {param.default_value}")
            else:
                print(f"       {param.name}: {param.type_name}")
        print(f"     )")

    # 8. Namespaces
    print("\n8. NAMESPACES")
    print("-" * 70)
    result = parser.parse_header('tests/fixtures/include/namespaces.h')
    namespaced_items = []
    for func in result.functions:
        if func.namespace:
            namespaced_items.append(f"function {func.namespace}::{func.name}")
    for cls in result.classes:
        if cls.namespace:
            namespaced_items.append(f"class {cls.namespace}::{cls.name}")
    print(f"   Found {len(namespaced_items)} items in namespaces:")
    for item in namespaced_items[:5]:
        print(f"   • {item}")

    print("\n" + "=" * 70)
    print("Demo complete! All features working correctly.")
    print("=" * 70)

    # Generate sample XML
    print("\nGenerating sample XML output...")
    generator = XmlGenerator(output_dir="/tmp/cpp2xml_demo")
    generator.write_xml(parser.parse_header('tests/fixtures/include/enums.h'))
    print("✓ Generated: /tmp/cpp2xml_demo/enums.xml")
    print("\nRun 'cat /tmp/cpp2xml_demo/enums.xml' to see the XML output!")


if __name__ == "__main__":
    demo()
